from zope.component.hooks import getSite
from euphorie.client import model
from euphorie.client import session
from euphorie.client import utils
from euphorie.client.tests.utils import testRequest
from euphorie.deployment.tests.functional import EuphorieTestCase


class handleSurveyUnpublishTests(EuphorieTestCase):
    def handleSurveyUnpublish(self, *a, **kw):
        from euphorie.client.unpublish import handleSurveyUnpublish
        return handleSurveyUnpublish(*a, **kw)

    def afterSetUp(self):
        super(handleSurveyUnpublishTests, self).afterSetUp()
        self.loginAsPortalOwner()
        self.client = self.portal.client

    def createSurvey(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        addSurvey(self.portal, BASIC_SURVEY)
        return (self.portal.sectors["nl"]["ict"]
                ["software-development"]["test-import"])

    def testUnpublishedSurvey(self):
        from euphorie.content.tests.utils import EMPTY_SURVEY
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        sector = createSector(self.portal)
        survey = addSurvey(sector, EMPTY_SURVEY)
        self.handleSurveyUnpublish(survey, None)

    def testPublishedSurvey(self):
        from OFS.SimpleItem import SimpleItem
        survey = self.createSurvey()
        clientsector = self.portal.client["nl"]["ict"]
        clientsector["other"] = SimpleItem("other")
        self.handleSurveyUnpublish(survey, None)
        self.assertEqual(self.portal.client["nl"]["ict"].keys(), ["other"])

    def testRemoveEmptySector(self):
        from OFS.SimpleItem import SimpleItem
        survey = self.createSurvey()
        clientcountry = self.portal.client["nl"]
        clientcountry["other"] = SimpleItem("other")
        self.handleSurveyUnpublish(survey, None)
        self.assertEqual(self.portal.client["nl"].keys(), ["other"])

    def testUnpublishWithActiveSession(self):
        """When a survey gets unpublished, while it's still in an active
        session, then WebHelpers.survey_url must return None, not fail.
        """
        survey = self.createSurvey()
        client_survey = getSite().client.nl.ict['software-development']
        request = testRequest()
        request.client = client_survey
        utils.setRequest(request)
        account = model.Account(loginname="jane", password=u"john")
        mgr = session.SessionManagerFactory()
        mgr.start(u"Test session", client_survey, account)
        mgr.session.zodb_path = '/'.join(client_survey.getPhysicalPath())

        helpers = utils.WebHelpers(survey, request)
        self.assertEqual(
                helpers.survey_url(),
                client_survey.absolute_url())

        self.handleSurveyUnpublish(survey, None)

        helpers = utils.WebHelpers(survey, request)
        self.assertEqual(
                helpers.survey_url(),
                None)
