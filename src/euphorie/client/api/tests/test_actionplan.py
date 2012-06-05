import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class plan_info_tests(unittest.TestCase):
    def plan_info(self, *a, **kw):
        from euphorie.client.api.actionplan import plan_info
        return plan_info(*a, **kw)

    def test_minimal(self):
        from euphorie.client.model import ActionPlan
        plan = ActionPlan(id=15, action_plan=u'This is the plan')
        info = self.plan_info(plan)
        self.assertEqual(
                set(info),
                set(['id', 'plan', 'prevention', 'requirements', 'responsible',
                    'budget', 'planning-start', 'planning-end', 'reference']))
        self.assertEqual(info['plan'], u'This is the plan')
        self.assertEqual(info['prevention'], None)
        self.assertEqual(info['requirements'], None)
        self.assertEqual(info['responsible'], None)
        self.assertEqual(info['budget'], None)
        self.assertEqual(info['planning-start'], None)
        self.assertEqual(info['planning-end'], None)

    def test_with_dates(self):
        import datetime
        from euphorie.client.model import ActionPlan
        plan = ActionPlan(
                planning_start=datetime.date(2012, 6, 3),
                planning_end=datetime.date(2012, 6, 4))
        info = self.plan_info(plan)
        self.assertEqual(info['planning-start'], '2012-06-03')
        self.assertEqual(info['planning-end'], '2012-06-04')


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.actionplan import View
        return View(*a, **kw)

    def test_do_GET_use_plan_info(self):
        import mock
        view = self.View('context', None)
        with mock.patch('euphorie.client.api.actionplan.plan_info') \
                as mock_plan_info:
            mock_plan_info.return_value = {'data': 'mock'}
            self.assertEqual(
                    view.do_GET(),
                    {'type': 'actionplan', 'data': 'mock'})
            mock_plan_info.assert_called_once_with('context')

    def test_do_PUT_returns_info(self):
        import mock
        from euphorie.client.model import ActionPlan
        view = self.View(ActionPlan(), None)
        view.input = {}
        view.do_GET = mock.Mock(return_value='info')
        self.assertEqual(view.do_PUT(), 'info')

    def test_do_PUT_update_data(self):
        import datetime
        from euphorie.client.model import ActionPlan
        context = ActionPlan()
        view = self.View(context, None)
        view.input = {'plan': 'Collect underpants',
                      'budget': 15,
                      'planning-start': '2012-06-04'}
        view.do_PUT()
        self.assertEqual(context.action_plan, u'Collect underpants')
        self.assertEqual(context.budget, 15)
        self.assertEqual(context.planning_start, datetime.date(2012, 6, 4))

    def test_do_PUT_bad_data(self):
        from euphorie.client.model import ActionPlan
        context = ActionPlan()
        view = self.View(context, None)
        view.input = {'budget': 'unlimited'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')


class BrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import datetime
        import json
        from sqlalchemy.orm import object_session
        from euphorie.client.model import Risk
        from euphorie.client.model import ActionPlan
        from euphorie.client.api.authentication import generate_token
        from euphorie.client.api.tests.test_risk import _setup_session
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = object_session(survey_session).query(Risk).one()
        risk.action_plans.append(ActionPlan(
            action_plan=u'This is the plan',
            planning_start=datetime.date(2012, 6, 3)))
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/'
                     'sessions/1/1/1/actionplans/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['plan'], u'This is the plan')
