from datetime import datetime
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api


class TestCloningViews(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.jane = addAccount("jane@example.com", password="secret")
        self.john = addAccount("john@example.com", password="secret")

        group = model.Group(group_id="1")
        model.Session.add(group)

        self.jane.group = group
        self.john.group = group
        model.Session.flush()

        survey_session = model.SurveySession(
            title="Dummy session",
            created=datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime(2012, 4, 23, 11, 50, 30),
            zodb_path="nl/ict/software-development",
            account=self.jane,
            group=group,
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

    def test_clone(self):
        country = self.portal.client.nl
        traversed_session = country.ict["software-development"].restrictedTraverse(
            "++session++1"
        )
        # Calling the view redirects to the client home page if we are not autenticated
        with self._get_view("clone-session", traversed_session) as view:
            view()
            self.assertDictEqual(
                view.request.response.headers,
                {"location": "http://nohost/plone/client"},
            )

        # Calling the view redirects to the cloned session if authenticated
        with api.env.adopt_user(user=self.john):
            with self._get_view(
                "clone-session", traversed_session, traversed_session.session
            ) as view:
                view()
                self.assertDictEqual(
                    view.request.response.headers,
                    {
                        "location": "http://nohost/plone/client/nl/ict/software-development/++session++2/@@start?new_clone=1"  # noqa: E501
                    },
                )

        with api.env.adopt_user(user=self.john):
            with self._get_view("clone-session", traversed_session) as view:
                original = model.Session.query(model.SurveySession).get(1)
                clone = view.get_cloned_session()
                # The cloned session has a lot in common with the original one
                # The title is prefixed with a COPY marker
                self.assertEqual(clone.title, f"COPY: {original.title}")
                self.assertEqual(clone.company.country, original.company.country)
                # But is marked with the account that made the clone
                self.assertEqual(original.account.login, "jane@example.com")
                self.assertEqual(clone.account.login, "john@example.com")

                # Also all the tree is copied
                self.assertListEqual(
                    [(x.id, x.title) for x in clone.children()], [(5, "module 1")]
                )
                module = clone.children()[0]
                self.assertListEqual(
                    [(x.id, x.title) for x in module.children()], [(6, "question 1")]
                )
                risk = module.children()[0]
                self.assertListEqual(
                    [(x.id, x.action_plan) for x in risk.action_plans],
                    [(3, "This is the plan")],
                )
                # Also verify that the cloned risk has
                # the cloned module as a parent
                self.assertEqual(risk.parent, module)
