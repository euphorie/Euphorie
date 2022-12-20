from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.testing import EuphorieFunctionalTestCase


class ReportTests(EuphorieFunctionalTestCase):
    def testInvalidDateDoesNotBreakRendering(self):
        from euphorie.client import model
        from euphorie.content.tests.utils import BASIC_SURVEY
        from z3c.saconfig import Session

        import datetime

        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey_url = self.portal.client.nl["ict"]["software-development"].absolute_url()
        browser = self.get_browser()
        browser.open(survey_url)
        registerUserInClient(browser)
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm(action="new-session").submit()
        browser.getControl(name="form.widgets.title").value = "Sessiøn".encode()  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        session_url = browser.url.replace("/@@identification", "")
        # Update the risk
        risk = Session.query(model.Risk).first()
        risk.identification = "no"
        risk.action_plans.append(
            model.ActionPlan(
                action_plan="Do something awesome",
                planning_start=datetime.date(1, 2, 3),
            )
        )
        # Render the report
        browser.handleErrors = False
        browser.open("%s/@@report_view" % session_url)
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
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm(action="new-session").submit()
        browser.getControl(name="form.widgets.title").value = "Sessiøn".encode()  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        session_url = browser.url.replace("/@@identification", "")
        # Check the company data
        browser.open("%s/@@report_company" % session_url)
        self.assertEqual(browser.getControl(name="form.widgets.country").value, ["nl"])

    def testCompanySettingsRoundTrip(self):
        from euphorie.content.tests.utils import BASIC_SURVEY

        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        survey_url = self.portal.client.nl["ict"]["software-development"].absolute_url()
        browser.open(survey_url)
        registerUserInClient(browser)
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        # Create a new survey session
        browser.getControl(name="survey").value = ["ict/software-development"]
        browser.getForm(action="new-session").submit()
        browser.getControl(name="form.widgets.title").value = "Sessiøn".encode()  # noqa
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        session_url = browser.url.replace("/@@identification", "")
        # Enter some company data
        browser.open("%s/@@report_company" % session_url)
        browser.getControl(name="form.widgets.country").value = ["be"]
        browser.getControl(name="form.widgets.employees").value = ["50-249"]
        browser.getControl(name="form.widgets.conductor").value = ["staff"]
        browser.getControl(name="form.widgets.referer").value = ["trade-union"]
        browser.getControl(name="form.widgets.workers_participated").value = ["True"]
        browser.getControl(name="form.buttons.next").click()
        # Make sure all fields validated
        self.assertEqual(browser.url, "%s/@@report_view" % session_url)
        # Verify entered data
        browser.open("%s/@@report_company" % session_url)
        self.assertEqual(browser.getControl(name="form.widgets.country").value, ["be"])
        self.assertEqual(
            browser.getControl(name="form.widgets.employees").value, ["50-249"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.conductor").value, ["staff"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.referer").value, ["trade-union"]
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.workers_participated").value, ["True"]
        )
