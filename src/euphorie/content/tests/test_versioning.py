from euphorie.deployment.tests.functional import EuphorieTestCase


class VersioningTests(EuphorieTestCase):
    def createSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        return survey

    def publish(self, survey):
        # XXX: this should use the event system to give a more accurate test,
        # but for some reason the history is lost if we do that.
        from Products.CMFCore.WorkflowCore import ActionSucceededEvent
        from zope.event import notify
        notify(ActionSucceededEvent(survey, None, "publish", None))
#        from euphorie.content.versioning import handleSurveyPublish
#        handleSurveyPublish(survey, ActionSucceededEvent(survey, None,
#                    "publish", None))

    def testNewlyCreatedSurveyHasNoVersions(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        repository = self.portal.portal_repository
        self.assertEqual(repository.getHistoryMetadata(survey), [])

    def XtestPublishCreatesNewVersion(self):
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        repository = self.portal.portal_repository
        self.publish(survey)
        history = repository.getHistoryMetadata(survey)
        self.assertEqual(history.getLength(False), 1)

    def XtestBrowseOldVersion(self):
        from Products.CMFCore.WorkflowCore import ActionSucceededEvent
        from euphorie.content.survey import handleSurveyPublish
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        handleSurveyPublish(survey,
                ActionSucceededEvent(survey, None, "publish", None))
        self.assertEqual(
                self.portal.client["nl"]["sector"]["test-survey"]["1"].title,
                u"Module one")
        survey["1"].title = u"Module two"
        handleSurveyPublish(survey,
                ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(
                self.portal.client["nl"]["sector"]["test-survey"]["1"].title,
                u"Module two")
