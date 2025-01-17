from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase


class RiskTests(EuphorieFunctionalTestCase):
    def testShowFrenchEvaluation(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey = self.portal.client.nl["ict"]["software-development"]
        survey.evaluation_algorithm = "french"
        survey["1"]["2"].type = "risk"
        browser = self.get_browser()
        browser.open(survey.absolute_url())
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
        # Identify the risk
        browser.open("%s/1/1/@@identification" % session_url)
        browser.getControl(name="answer").value = ["no"]
        # Verify number of options
        self.assertEqual(
            len(tuple(browser.getControl(name="frequency:int").controls)), 4
        )
        self.assertEqual(
            len(tuple(browser.getControl(name="severity:int").controls)), 4
        )
        # Enter some digits
        browser.getControl(name="frequency:int").value = ["7"]
        browser.getControl(name="severity:int").value = ["10"]
        browser.getControl("next").click()
        # Verify the result
        browser.open("%s/1/1/@@actionplan" % session_url)
        self.assertEqual(browser.getControl(name="priority").value, ["high"])

    def XtestPreventEarlyDate(self):
        """Deactivated until we decide what to do about this kind of validation
        error check."""
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        survey_url = self.portal.client.nl["ict"][
            "software-development"
        ].absolute_url()  # noqa: E501
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
        # Identify the risk
        browser.getControl("next").click()
        browser.getControl(name="answer").value = ["no"]
        browser.getControl("next").click()
        # Move on to the risk's action plan form
        browser.getLink("Create action plan").click()
        browser.getLink("Next").click()
        # Try an early year
        browser.getControl(
            name="measure.action_plan:utf8:ustring:records", index=0
        ).value = "Do something awesome"
        browser.getControl(name="measure.planning_start_day:records", index=0).value = (
            "1"
        )
        browser.getControl(
            name="measure.planning_start_month:records", index=0
        ).value = ["2"]
        browser.getControl(
            name="measure.planning_start_year:records", index=0
        ).value = "3"
        browser.getControl("next").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/" "software-development/actionplan/1/1",
        )
        self.assertTrue("Please enter a year between 2000 and 2100" in browser.contents)

    def Xtest_do_not_abort_on_far_future(self):
        """Deactivated, since such a far-future date can not be entered any
        more in modern browsers."""
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
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
        # Identify the risk
        browser.getControl("next").click()
        browser.getControl(name="answer").value = ["no"]
        browser.getControl("next").click()
        # Move on to the risk's action plan form
        browser.getLink("Create action plan").click()
        browser.getLink("Next").click()
        # Try an early year
        browser.getControl(
            name="measure.action_plan:utf8:ustring:records", index=0
        ).value = "Do something awesome"
        browser.getControl(name="measure.planning_start:records", index=0).value = (
            "12345/02/01"
        )
        browser.handleErrors = False
        browser.getControl("next").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/" "software-development/actionplan/1/1",
        )
        self.assertTrue("Please enter a year between 2000 and 2100" in browser.contents)

    def test_set_unknown_answer_if_skipped(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        # Register in the client
        browser = self.get_browser()
        survey_url = self.portal.client.nl["ict"][
            "software-development"
        ].absolute_url()  # noqa: E501
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
        # Identify the risk
        browser.open("%s/1/1/@@identification" % session_url)
        # No answer should be set on initial view
        self.assertEqual(browser.getControl(name="answer").value, [])
        # Do not give an identification answer
        risk_url = browser.url
        browser.getControl("next").click()
        # Go back and check the new answer
        browser.open(risk_url)
        self.assertTrue('class="current postponed' in browser.contents)
