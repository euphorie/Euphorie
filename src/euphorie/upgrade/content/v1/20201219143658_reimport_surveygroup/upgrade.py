from ftw.upgrade import UpgradeStep
from plone import api


class ReImportSurveyGroup(UpgradeStep):
    """Re-import SurveyGroup type definition."""

    def __call__(self):
        # First, delete exisiting type registration for euphorie.surveygroup
        tt = api.portal.get_tool("portal_types")
        obj = tt.get("euphorie.surveygroup")
        if obj:
            api.content.delete(obj)
        self.install_upgrade_profile()
