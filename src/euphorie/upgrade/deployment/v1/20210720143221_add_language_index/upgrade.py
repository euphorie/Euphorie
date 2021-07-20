from ftw.upgrade import UpgradeStep
from plone import api


class AddLanguageIndex(UpgradeStep):
    """Add Language index."""

    def __call__(self):
        self.install_upgrade_profile()
        ct = api.portal.get_tool("portal_catalog")
        survey_results = ct(portal_type="euphorie.survey")
        for brain in survey_results:
            survey = brain.getObject()
            survey.reindexObject(idxs=["Language"])
