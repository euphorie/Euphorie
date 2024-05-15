from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.model import ActionPlan
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.client.model import SurveyTreeItem
from euphorie.content.countrymanager import ICountryManager
from euphorie.content.risk import EnsureInterface
from euphorie.content.risk import IRisk
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
from plone.memoize.instance import memoize
from plone.memoize.view import memoize_contextless
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.membrane.interfaces.user import IMembraneUser
from sqlalchemy import and_
from sqlalchemy import sql
from time import time
from zope.deprecation import deprecate
from zope.interface import alsoProvides

import logging


log = logging.getLogger(__name__)


class Frontpage(BrowserView):
    def __call__(self):
        user = getSecurityManager().getUser()
        if IMembraneUser.providedBy(user):
            mt = getToolByName(self.context, "membrane_tool")
            obj = mt.getUserObject(user_id=user.getUserId())
            if ICountryManager.providedBy(obj):
                return self.request.response.redirect(aq_parent(obj).absolute_url())
            return self.request.response.redirect(obj.absolute_url())
        portal = aq_inner(self.context)
        return self.request.response.redirect("%s/sectors/" % portal.absolute_url())


class EuphorieRefreshResourcesTimestamp(BrowserView):
    @property
    @memoize_contextless
    def resources_timestamp(self):
        return api.portal.get_registry_record(
            "euphorie.deployment.resources_timestamp", default=""
        )

    def refresh_timestamp(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        api.portal.set_registry_record(
            "euphorie.deployment.resources_timestamp", str(int(time()))
        )

    def __call__(self):
        """Refresh the registry record that adds a timestamp to the resources
        urls."""
        self.refresh_timestamp()
        return "OK"


class GetEuphorieResourcesTimestamp(EuphorieRefreshResourcesTimestamp):
    def __call__(self):
        """Get the resource timestamp."""
        return self.resources_timestamp


class ManageEnsureInterface(BrowserView):
    def set_evaluation_method_interfaces(self):
        def walk(node):
            for idx, sub_node in node.ZopeFind(node, search_sub=0):
                if IRisk.providedBy(sub_node):
                    yield sub_node
                if IDexterityContainer.providedBy(sub_node):
                    yield from walk(sub_node)

        count = 0
        walker = walk(self.context)
        for risk in walker:
            log.debug("Ensure interface for %s", "/".join(risk.getPhysicalPath()))
            EnsureInterface(risk)
            count += 1
        log.info("Ensured interface for %d risks", count)
        return count

    def __call__(self):
        """Iterate over all risks in the current context and ensure that they
        have the correct interface."""
        count = self.set_evaluation_method_interfaces()
        return "Handled %d risks" % count


class UpdateCompletionPercentage(WebHelpers):
    """Utility view to fill in missing values for completion_percentage."""

    flush_threshold = 50

    def log(self, entry):
        log.info(entry)
        self._log = "\n".join((getattr(self, "_log", ""), entry))

    def get_log(self):
        return getattr(self, "_log", "")

    def next_b_start(self):
        if "overwrite" in self.request.form:
            return self.request.get("b_start", 0) + self.request.get("b_size", 1000)
        else:
            return 0

    @deprecate(
        "Not needed anymore because the completion_percentage is now calculated. "
        "Deprecated in version 14.1.4.dev0"
    )
    def __call__(self):
        return self.index()


class RepairSolutionId(BrowserView):
    @memoize
    def get_tool(self, tool_path):
        return self.client.restrictedTraverse(str(tool_path))

    @memoize
    def get_risk(self, tool, risk_path):
        return tool.restrictedTraverse(str(risk_path))

    def __call__(self):
        site = api.portal.get()
        self.client = getattr(site, "client")
        query = (
            Session.query(ActionPlan, SurveyTreeItem, SurveySession)
            .filter(
                sql.and_(
                    ActionPlan.plan_type == "in_place_standard",
                    ActionPlan.solution_id == None,  # noqa: E711
                )
            )
            .join(SurveyTreeItem, ActionPlan.risk_id == SurveyTreeItem.id)
            .join(SurveySession, SurveyTreeItem.session_id == SurveySession.id)
            .order_by(SurveySession.zodb_path)
        )
        count = 0
        ret = "We have a total of %d measures\n" % query.count()

        for action_plan, risk, session in query.all():
            tool = self.get_tool(session.zodb_path)
            risk = self.get_risk(tool, risk.zodb_path)
            for solution in risk._solutions:
                if (
                    solution.action
                    and action_plan.action
                    and solution.action.strip() == action_plan.action.strip()
                ):
                    action_plan.solution_id = str(solution.id)
                    count += 1
                    break
        ret += "Updated %d measures" % count
        return ret


class FixOmegaPaths(BrowserView):
    def __call__(self):
        session = Session()

        custom_risks = session.query(SurveyTreeItem).filter(
            and_(
                SurveyTreeItem.zodb_path.notlike("custom-risks%"),
                SurveyTreeItem.zodb_path.like("%custom-risks%"),
                SurveyTreeItem.type == "risk",
            )
        )

        count = 0

        for risk in custom_risks:
            i = 1
            num = risk.zodb_path.split("/")[-1]
            while i < 100:
                new_zodb_path = f"custom-risks/{num}"
                conflict = session.query(SurveyTreeItem).filter(
                    and_(
                        SurveyTreeItem.session_id == risk.session_id,
                        SurveyTreeItem.zodb_path == new_zodb_path,
                    )
                )
                if conflict.count():
                    num = num = str(int(num) + i)
                else:
                    risk.zodb_path = new_zodb_path
                    count += 1
                    break
                i += 1
        return "Fixed %d omega risks" % count
