from euphorie.client import model
from euphorie.client.model import SurveySession
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api


class TestHistoryPopup(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        self.survey = self.portal.client.nl.ict["software-development"]
        survey_session = SurveySession(
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=self.account,
            company=model.Company(country="nl", employees="1-9", referer="other"),
        )
        model.Session.add(survey_session)

    def test_history_popup(self):
        with api.env.adopt_user(user=self.account):
            traversed_session = self.survey.restrictedTraverse("++session++1")
            with self._get_view("history_popup", traversed_session) as view:
                # By default there is no event registered but the history starts
                # using the creation date of the session
                self.assertEqual(len(view.events), 0)
                self.assertEqual(len(view.items), 1)
                item = view.items[0]
                self.assertEqual(item.email, "jane@example.com")
                self.assertEqual(item.message, "started assessment")
