# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient


class ReportTests(EuphorieFunctionalTestCase):
    def testUnicodeReportFilename(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/156
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser=Browser()
        survey_url=self.portal.client.nl["ict"]["software-development"].absolute_url()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value=u"Sessiøn".encode("utf-8")
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Download the report
        browser.handleErrors=False
        browser.open("%s/report/download" % survey_url)
        self.assertEqual(browser.headers.type, "application/msword")
        self.assertEqual(browser.headers.get("Content-Disposition"),
                'attachment; filename="Action plan Sessi\xc3\xb8n.doc"')
