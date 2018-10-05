# coding=utf-8
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.testing import EuphorieFunctionalTestCase


class ReportTests(EuphorieFunctionalTestCase):

    def testUnicodeReportFilename(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/156
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey_url = self.portal.client.nl["ict"][
            "software-development"
        ].absolute_url()  # noqa: E501
        browser = self.get_browser()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm().submit()
        browser.getControl(name="form.widgets.title").value = u"Sessiøn".encode("utf-8")  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        browser.getLink("Start Risk Identification").click()
        # Force creation of the company data
        browser.open("%s/report/company" % survey_url)
        # Download the report
        browser.handleErrors = False
        browser.open("%s/report/download" % survey_url)
        self.assertEqual(browser.headers.type, "application/rtf")
        self.assertEqual(
            browser.headers.get("Content-Disposition"),
            'attachment; filename="Action plan Sessi\xc3\xb8n.rtf"'
        )

    def testInvalidDateDoesNotBreakRendering(self):
        import datetime
        from euphorie.content.tests.utils import BASIC_SURVEY
        from z3c.saconfig import Session
        from euphorie.client import model
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey_url = self.portal.client.nl["ict"]["software-development"
                                                  ].absolute_url()
        browser = self.get_browser()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm().submit()
        browser.getControl(name="form.widgets.title").value = u"Sessiøn".encode("utf-8")  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        browser.getLink("Start Risk Identification").click()
        # Update the risk
        risk = Session.query(model.Risk).first()
        risk.identification = "no"
        risk.action_plans.append(
            model.ActionPlan(
                action_plan=u"Do something awesome",
                planning_start=datetime.date(1, 2, 3)
            )
        )
        # Render the report
        browser.handleErrors = False
        browser.open(
            "http://nohost/plone/client/nl/ict/"
            "software-development/report/view"
        )
        # No errors = success

    def testCountryDefaultsToCurrentCountry(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey_url = self.portal.client.nl["ict"][
            "software-development"
        ].absolute_url()  # noqa: E501
        browser = self.get_browser()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm().submit()
        browser.getControl(name="form.widgets.title").value = u"Sessiøn".encode("utf-8")  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        browser.getLink("Start Risk Identification").click()
        # Check the company data
        browser.open("%s/report/company" % survey_url)
        self.assertEqual(
            browser.getControl(name="form.widgets.country").value, ["nl"]
        )

    def testCompanySettingsRoundTrip(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        survey_url = self.portal.client.nl["ict"]["software-development"
                                                  ].absolute_url()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm().submit()
        browser.getControl(name="form.widgets.title").value = u"Sessiøn".encode("utf-8")  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        browser.getLink("Start Risk Identification").click()
        # Enter some company data
        browser.open("%s/report/company" % survey_url)
        browser.getControl(name="form.widgets.country").value = ["be"]
        browser.getControl(name="form.widgets.employees").value = ["50-249"]
        browser.getControl(name="form.widgets.conductor").value = ["staff"]
        browser.getControl(name="form.widgets.referer").value = ["trade-union"]
        browser.getControl(name="form.widgets.workers_participated").value = [
            'True'
        ]
        browser.getControl(name="form.buttons.next").click()
        # Make sure all fields validated
        self.assertEqual(browser.url, "%s/report/view" % survey_url)
        # Verify entered data
        browser.open("%s/report/company" % survey_url)
        self.assertEqual(
            browser.getControl(name="form.widgets.country").value, ["be"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.employees").value,
            ["50-249"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.conductor").value, ["staff"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.referer").value,
            ["trade-union"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.workers_participated").value,
            ["True"]
        )
