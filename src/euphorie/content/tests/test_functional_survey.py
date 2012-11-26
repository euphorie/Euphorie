from euphorie.deployment.tests.functional import EuphorieTestCase


class SurveyTests(EuphorieTestCase):
    def createSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        sector = createSector(self.portal, login='sector')
        survey = addSurvey(sector)
        return survey

    def testSurveyWorkflow(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        chain = self.folder.portal_workflow.getChainFor(survey)
        self.assertEqual(chain, ('survey',))

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless('euphorie.survey' not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        types = [fti.id for fti in survey.allowedContentTypes()]
        self.assertEqual(set(types), set(['euphorie.module',
                                          'euphorie.profilequestion']))

    def testCanDeleteItemsWhenNotPublished(self):
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.SecurityManagement import newSecurityManager
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        sector = self.portal.acl_users.getUser('sector')
        newSecurityManager(None, sector)
        manager = getSecurityManager()
        self.assertTrue(manager.checkPermission('Delete objects', survey))

    def testCanNotBeCopied(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        self.assertFalse(survey.cb_isCopyable())
