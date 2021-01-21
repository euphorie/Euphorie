# coding=utf-8
from AccessControl.SecurityManagement import newSecurityManager
from datetime import datetime
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase


class TestCloningViews(EuphorieIntegrationTestCase):
    def setUp(self):
        super(TestCloningViews, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password="secret")
        survey_session = model.SurveySession(
            title=u"Dummy session",
            created=datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime(2012, 4, 23, 11, 50, 30),
            zodb_path="nl/ict/software-development",
            account=account,
            company=model.Company(country="nl", employees="1-9", referer="other"),
        )
        module = survey_session.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        risk = module.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        model.ActionPlan(action_plan=u"This is the plan", risk=risk)
        model.Session.add(survey_session)

    def test_clone(self):
        country = self.portal.client.nl
        john = model.Account(loginname="john@example.com")
        model.Session.add(john)
        newSecurityManager(None, john)

        traversed_session = country.ict["software-development"].restrictedTraverse(
            "++session++1"
        )  # noqa: E501

        # Calling the view redirects to the cloned session
        with self._get_view("clone-session", traversed_session) as view:
            view()
            self.assertDictEqual(
                view.request.response.headers,
                {
                    "location": "http://nohost/plone/client/nl/ict/software-development/++session++2/@@start?new_clone=1"  # noqa: E501
                },
            )

        with self._get_view("clone-session", traversed_session) as view:
            original = model.Session.query(model.SurveySession).get(1)
            clone = view.get_cloned_session()
            # The cloned session has a lot in common with the original one
            # The title is prefixed with a COPY marker
            self.assertEqual(clone.title, u"COPY: {}".format(original.title))
            self.assertEqual(clone.company.country, original.company.country)
            # But is marked with the account that made the clone
            self.assertEqual(original.account.login, "jane@example.com")
            self.assertEqual(clone.account.login, "john@example.com")

            # Also all the tree is copied
            self.assertListEqual(
                [(x.id, x.title) for x in clone.children()], [(5, u"module 1")]
            )
            module = clone.children()[0]
            self.assertListEqual(
                [(x.id, x.title) for x in module.children()], [(6, u"question 1")]
            )
            risk = module.children()[0]
            self.assertListEqual(
                [(x.id, x.action_plan) for x in risk.action_plans],
                [(3, u"This is the plan")],
            )
            # Also verify that the cloned risk has
            # the cloned module as a parent
            self.assertEqual(risk.parent, module)
