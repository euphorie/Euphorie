from euphorie.deployment.tests.functional import EuphorieTestCase


class VersioningTests(EuphorieTestCase):
    def createSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        sector=createSector(self.portal)
        survey=addSurvey(sector)
        return survey

    def testNewlyCreatedSurveyHasNoVersions(self):
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        repository=self.portal.portal_repository
        self.assertEqual(repository.getHistoryMetadata(survey), [])

    def XtestPublishCreatesNewVersion(self):
        from zope.event import notify
        from Products.CMFCore.WorkflowCore import ActionSucceededEvent
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        repository=self.portal.portal_repository
        notify(ActionSucceededEvent(survey, None, "publish", None))
        notify(ActionSucceededEvent(survey, None, "publish", None))
        history=repository.getHistoryMetadata(survey)
        self.assertEqual(history.getLength(False), 1)

    def XtestBrowseOldVersion(self):
        from Products.CMFCore.WorkflowCore import ActionSucceededEvent
        from euphorie.content.survey import handleSurveyPublish
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        handleSurveyPublish(survey, ActionSucceededEvent(survey, None, "publish", None))
        self.assertEqual(self.portal.client["nl"]["sector"]["test-survey"]["1"].title, u"Module one")
        survey["1"].title=u"Module two"
        handleSurveyPublish(survey, ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(self.portal.client["nl"]["sector"]["test-survey"]["1"].title, u"Module two")
