from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from euphorie.content.tests.utils import addSurvey
from euphorie.content.tests.utils import createSector
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api


class SurveyTests(EuphorieIntegrationTestCase):
    def createSurvey(self):
        sector = createSector(self.portal, login="sector")
        survey = addSurvey(sector)
        return survey

    def testSurveyWorkflow(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        pw = api.portal.get_tool("portal_workflow")
        chain = pw.getChainFor(survey)
        self.assertEqual(chain, ("survey",))

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.assertTrue("euphorie.survey" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        types = [fti.id for fti in survey.allowedContentTypes()]
        self.assertEqual(set(types), {"euphorie.module", "euphorie.profilequestion"})

    def testCanDeleteItemsWhenNotPublished(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        sector = self.portal.acl_users.getUser("sector")
        newSecurityManager(None, sector)
        manager = getSecurityManager()
        self.assertTrue(manager.checkPermission("Delete objects", survey))
