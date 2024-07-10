from euphorie.client.model import Account
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from Products.Five import BrowserView

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
        for guest_user, assessment in obsolete_guest_users:
            assessment.last_modifier_id = assessment.account_id
            logger.info("Updated session %s", assessment.id)
        return "Done"
