from datetime import datetime
from datetime import timedelta
from euphorie.client import model
from euphorie.client.browser.company import Company
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from unittest import mock


class TestCompanyViews(EuphorieIntegrationTestCase):
    """"""

    @mock.patch.object(Company, "applyChanges")
    @mock.patch.object(Company, "render")
    def test_company_timestamp(self, mock_render, mock_applyChanges):
        with api.env.adopt_user("admin"):
            survey = addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password="secret")
        survey_session = model.SurveySession(
            id=456,
            title="Dummy session",
            created=datetime(2021, 4, 9, 9, 11, 31),
            modified=datetime(2021, 4, 9, 9, 11, 52),
            zodb_path="nl/ict/software-development",
            account=account,
        )
        model.Session.add(survey_session)
        survey = self.portal.client.nl.ict["software-development"]

        session_id = "++session++%d" % survey_session.id
        traversed_survey_session = survey.restrictedTraverse(session_id)

        with api.env.adopt_user(user=survey_session.account):
            with self._get_view(
                "report_company", traversed_survey_session, survey_session
            ) as view:
                view.request.form = {
                    "form.widgets.conductor": "staff",
                    "form.widgets.country": "nl",
                    "form.widgets.employees": "10-49",
                    "form.widgets.referer": "health-safety-experts",
                    "form.widgets.workers_participated": False,
                    "form.widgets.needs_met": True,
                    "form.widgets.recommend_tool": True,
                    "form.buttons.next": "",
                }
                view()
                timestamp = mock_applyChanges.call_args[0][0]["timestamp"]
                self.assertLess(datetime.now() - timestamp, timedelta(seconds=3))

                del view.request.form["form.buttons.next"]
                view.request.form["form.buttons.previous"] = ""
                view()
                self.assertEqual(mock_applyChanges.call_count, 2)
                timestamp = mock_applyChanges.call_args[0][0]["timestamp"]
                self.assertLess(datetime.now() - timestamp, timedelta(seconds=3))
