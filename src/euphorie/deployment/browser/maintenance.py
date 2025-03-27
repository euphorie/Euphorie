from euphorie.client.model import Account
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from plone import api
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFPlone.ActionsTool import ActionsTool
from Products.Five import BrowserView
from transaction import commit

import logging


logger = logging.getLogger(__name__)


class CleanUpLastModifierId(BrowserView):
    """Clean up last_modifier_id."""

    def __call__(self):
        logger.info("Cleaning up last_modifier_id")
        session = Session()
        obsolete_guest_users = (
            session.query(Account, SurveySession)
            .filter(Account.id == SurveySession.last_modifier_id)
            .filter(Account.id != SurveySession.account_id)
            .filter(Account.account_type == "guest")
        )

        with session.no_autoflush:
            for guest_user, assessment in obsolete_guest_users:
                assessment.last_modifier_id = assessment.account_id
                logger.info("Updated session %s", assessment.id)

                num_assessments = (
                    session.query(SurveySession)
                    .filter(SurveySession.account_id == guest_user.id)
                    .count()
                )
                if num_assessments == 0:
                    session.delete(guest_user)
                    logger.info("Deleted user %s", guest_user.id)
        commit()
        return "Done"


class AdminMaintenanceView(BrowserView):
    """View for maintenance tasks (@@admin-maintenance)."""

    @property
    def actions(self) -> tuple[ActionInfo]:
        """Return all the actions available in the `maintenance_actions` category."""
        portal_actions: ActionsTool = api.portal.get_tool("portal_actions")
        return portal_actions.listActionInfos(
            object=self.context, categories=["maintenance_actions"]
        )
