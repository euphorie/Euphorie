from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.testing import EuphorieFunctionalTestCase
from transaction import commit


class SurveyTests(EuphorieFunctionalTestCase):
    def test_policy_gets_high_priority(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/93
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <language>nl</language>
                        <evaluation-optional>false</evaluation-optional>
                        <module optional="false">
                          <title>Policy parent</title>
                          <description>&lt;p&gt;Een module met een beleidsrisico.&lt;/p&gt;</description>
                          <risk type="policy">
                            <title>Policy problem!</title>
                            <problem-description>There is a policy problem.</problem-description>
                            <description>&lt;p&gt;Random text.&lt;/p&gt;</description>
                            <show-not-applicable>false</show-not-applicable>
                          </risk>
                        </module>
                      </survey>
                    </sector>"""  # noqa: E501
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        commit()
        self.request.response.setHeader("X-Theme-Disabled", "1")
        browser = self.get_browser()
        url = self.portal.client.nl["sector-title"]["survey-title"].absolute_url()
        browser.open(url)
        registerUserInClient(browser)
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        # Create a new survey session
        browser.getControl(name="survey").value = ["sector-title/survey-title"]
        browser.getForm(action="new-session").submit()
        browser.getControl(name="form.widgets.title").value = "Test session"
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        session_url = browser.url.replace("/@@identification", "")
        # Identify the risk
        browser.open("%s/1/1/@@identification" % session_url)
        browser.getControl(name="answer").value = ["no"]
        browser.getControl(name="next", index=1).click()
        # Check priority in action plan
        browser.open("%s/1/1/@@actionplan" % session_url)
        self.assertEqual(browser.getControl(name="priority").value, ["high"])

    def test_top5_gets_high_priority(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/93
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <language>nl</language>
                        <evaluation-optional>false</evaluation-optional>
                        <module optional="false">
                          <title>Top5 parent</title>
                          <description>&lt;p&gt;Een module met een top-5 risico.&lt;/p&gt;</description>
                          <risk type="top5">
                            <title>Top-5 probleem!</title>
                            <problem-description>Er is een top-5 probleem.</problem-description>
                            <description>&lt;p&gt;Zomaar wat tekst.&lt;/p&gt;</description>
                            <show-not-applicable>false</show-not-applicable>
                          </risk>
                        </module>
                      </survey>
                    </sector>"""  # noqa: E501
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser = self.get_browser()
        browser.open(
            self.portal.client.nl["sector-title"]["survey-title"].absolute_url()
        )
        registerUserInClient(browser)
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        # Create a new survey session
        browser.getControl(name="survey").value = ["sector-title/survey-title"]
        browser.getForm(action="new-session").submit()
        browser.getControl(name="form.widgets.title").value = "Test session"
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        session_url = browser.url.replace("/@@identification", "")
        # Identify the top-5 risk
        browser.open("%s/1/1/@@identification" % session_url)
        browser.getControl(name="answer").value = ["no"]
        browser.getControl(name="next", index=1).click()
        # Check priority in action plan
        browser.open("%s/1/1/@@actionplan" % session_url)
        self.assertEqual(browser.getControl(name="priority").value, "high")

    def test_top5_skipped_in_evaluation(self):
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/105
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <language>nl</language>
                        <evaluation-optional>false</evaluation-optional>
                        <module optional="false">
                          <title>Top5 parent</title>
                          <description>&lt;p&gt;Een module met een top-5 risico.&lt;/p&gt;</description>
                          <risk type="top5">
                            <title>Top-5 probleem!</title>
                            <problem-description>Er is een top-5 probleem.</problem-description>
                            <description>&lt;p&gt;Zomaar wat tekst.&lt;/p&gt;</description>
                            <show-not-applicable>false</show-not-applicable>
                          </risk>
                        </module>
                      </survey>
                    </sector>"""  # noqa: E501
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser = self.get_browser()
        browser.open(
            self.portal.client.nl["sector-title"]["survey-title"].absolute_url()
        )
        registerUserInClient(browser)
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        # Create a new survey session
        browser.getControl(name="survey").value = ["sector-title/survey-title"]
        browser.getForm(action="new-session").submit()
        browser.getControl(name="form.widgets.title").value = "Test session"
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        session_url = browser.url.replace("/@@identification", "")
        # Identify the top-5 risk
        browser.open("%s/1/1/@@identification" % session_url)
        browser.getControl(name="answer").value = ["no"]
        # No evaluation is necessary
        self.assertIn(
            "De tool heeft automatisch een risico-evaluatie uitgevoerd",
            browser.contents,
        )
