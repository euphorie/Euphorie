from datetime import datetime
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zExceptions import Unauthorized

import json


class TestExport(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.jane = addAccount("jane@example.com", password="secret")
        self.john = addAccount("john@example.com", password="secret")

        survey_session = model.SurveySession(
            title="Dummy session",
            created=datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime(2012, 4, 23, 11, 50, 30),
            zodb_path="nl/ict/software-development",
            account=self.jane,
            company=model.Company(country="nl", employees="1-9", referer="other"),
        )
        module = survey_session.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        risk = module.addChild(
            model.Risk(title="question 1", risk_id="1", zodb_path="a/b")
        )
        model.ActionPlan(action_plan="This is the plan", risk=risk)
        model.Session.add(survey_session)
        self.logout()

    def test_export_json(self):
        country = self.portal.client.nl
        traversed_session = country.ict["software-development"].restrictedTraverse(
            "++session++1"
        )
        # Calling the view as anonymous raises an Unauthorized exception
        with self._get_view("export.json", traversed_session) as view:
            with self.assertRaises(Unauthorized):
                view()

        # Calling the view as John raises an Unauthorized exception
        with api.env.adopt_user(user=self.john):
            with self._get_view("export.json", traversed_session) as view:
                with self.assertRaises(Unauthorized):
                    view()

        # Calling the view as Jane returns a json
        with api.env.adopt_user(user=self.jane):
            with self._get_view("export.json", traversed_session) as view:
                self.assertEqual(json.loads(view())["data"]["title"], "Dummy session")

        # Calling the view as admin returns a json
        with api.env.adopt_user(username="admin"):
            with self._get_view("export.json", traversed_session) as view:
                output = json.loads(view())
                self.assertEqual(output["data"]["title"], "Dummy session")
                self.assertEqual(output["data"]["created"], "2012-04-22T23:05:12")
                self.assertSetEqual(
                    set(output["children"]), {"company", "training", "tree"}
                )
