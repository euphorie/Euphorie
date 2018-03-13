# coding=utf-8
from Acquisition import aq_base
from Acquisition import aq_parent
from euphorie.client.api.actionplans import RiskActionPlans
from euphorie.client.api.actionplans import View
from euphorie.client.api.authentication import generate_token
from euphorie.client.api.tests.utils import _setup_session
from euphorie.client.model import ActionPlan
from euphorie.client.model import Risk
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.client.tests.utils import addAccount
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME

import datetime
import json
import mock


class RiskActionPlansTests(EuphorieIntegrationTestCase):

    def RiskActionPlans(self, *a, **kw):
        return RiskActionPlans(*a, **kw)

    def _make_risk(self, login):
        account = addAccount(login=login)
        risk = Risk(
            risk_id='15',
            path='01',
            zodb_path='/foo/bar/1',
            session=SurveySession(account=account, zodb_path='/foo/bar')
        )
        Session.add(risk)
        return risk

    def test_getitem_id_from_other_risk(self):
        risk = self._make_risk('jane')
        plan = ActionPlan(action_plan=u'This is the plan')
        risk.action_plans.append(plan)
        plans = self.RiskActionPlans('actionplans', None, risk)
        wrapped_plan = plans['1']
        self.assertTrue(aq_base(wrapped_plan) is plan)
        self.assertTrue(aq_base(aq_parent(wrapped_plan)) is plans)
        # I am commenting this line because plans['1'] does the same
        # and does not raise.
        # Additionally this test was masked before by another one with the same
        # name...
        # self.assertRaises(KeyError, plans.__getitem__, '1')

    def test_getitem_bad_key(self):
        plans = self.RiskActionPlans('actionplans', None, None)
        self.assertRaises(KeyError, plans.__getitem__, 'xyz')

    def test_getitem_id_from_other_risk2(self):
        risk1 = self._make_risk('jane')
        risk1.action_plans.append(ActionPlan(action_plan=u'This is the plan'))
        risk2 = self._make_risk('cindy')
        plans = self.RiskActionPlans('actionplans', None, risk2)
        self.assertRaises(KeyError, plans.__getitem__, '1')


class ViewTests(EuphorieIntegrationTestCase):

    def _build_context(self, **kw):
        with api.env.adopt_user(SITE_OWNER_NAME):
            (account, survey, survey_session) = _setup_session(self.portal)
        risk = Session.query(Risk).one()
        return RiskActionPlans('actionplans', None, risk)

    def test_plans_no_plans_defined(self):
        context = self._build_context()
        view = View(context, self.request.clone())
        self.assertEqual(view.plans(), [])

    def test_with_plan(self):
        context = self._build_context()
        plan = ActionPlan(action_plan=u'This is the plan')
        context.risk.action_plans.append(plan)
        with mock.patch('euphorie.client.api.actionplans.plan_info') \
                as mock_plan_info:
            mock_plan_info.return_value = 'plan-info'
            view = View(context, self.request.clone())
            plans = view.plans()
            self.assertEqual(plans, ['plan-info'])
            mock_plan_info.assert_called_once_with(plan)

    def test_do_GET_response(self):
        view = View(None, None)
        view.plans = mock.Mock(return_value='plan-info')
        response = view.do_GET()
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(set(response), set(['action-plans']))
        self.assertEqual(response['action-plans'], 'plan-info')
        view.plans.assert_called_once_with()

    def test_do_POST_success(self):
        context = mock.Mock()
        context.risk.action_plans = []
        view = View(context, self.request.clone())
        with mock.patch(
            'euphorie.client.api.actionplan.View.do_PUT',
            return_value={
                'type': 'actionplan'
            }
        ):
            view.input = 'input'
            response = view.do_POST()
            self.assertEqual(response, {'type': 'actionplan'})
            self.assertEqual(len(context.risk.action_plans), 1)

    def test_do_POST_error(self):
        view = View(None, self.request.clone())
        with mock.patch(
            'euphorie.client.api.actionplan.View.do_PUT',
            return_value={
                'type': 'error'
            }
        ):
            view.input = 'input'
            response = view.do_POST()
            self.assertEqual(response, {'type': 'error'})


class BrowserTests(EuphorieFunctionalTestCase):

    def test_get(self):
        with api.env.adopt_user(SITE_OWNER_NAME):
            (account, survey, survey_session) = _setup_session(self.portal)
            Session.add(survey_session)
            risk = Session.query(Risk).one()
            risk.action_plans.append(
                ActionPlan(
                    action_plan=u'This is the plan',
                    planning_start=datetime.date(2012, 6, 3)
                )
            )
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open(
            'http://nohost/plone/client/api/users/1/'
            'sessions/1/1/1/actionplans'
        )
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertTrue('action-plans' in response)
