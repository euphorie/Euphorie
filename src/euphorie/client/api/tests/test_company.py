import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import datetime
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import Company
        from euphorie.client.model import SurveySession
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        from Products.Five.testbrowser import Browser
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account,
                company=Company(country='nl',
                                employees='1-9',
                                referer='other'))
        Session.add(survey_session)
        browser = Browser()
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/company')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'company')


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.company import View
        return View(*a, **kw)

    def create_context(self):
        from euphorie.client.model import Company
        company = Company(
                country=u'nl',
                employees='1-9',
                conductor='both',
                referer='other',
                workers_participated=True)
        return company

    def test_GET_result(self):
        context = self.create_context()
        view = self.View(context, None)
        response = view.GET()
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(
                set(response),
                set(['type', 'country', 'employees', 'conductor', 'referer',
                     'workers-participated']))
        self.assertEqual(response['type'], 'company')

    def test_GET_no_company_data(self):
        # Company might not have been created yet
        from euphorie.client import model
        context = model.SurveySession()
        view = self.View(context, None)
        response = view.GET()
        self.assertEqual(response['country'], None)
        self.assertEqual(response['employees'], None)

    def test_POST_returns_info(self):
        import mock
        context = self.create_context()
        view = self.View(context, None)
        view.input = {}
        view.GET = mock.Mock(return_value='info')
        self.assertEqual(view.POST(), 'info')

    def test_POST_update_data(self):
        context = self.create_context()
        view = self.View(context, None)
        view.input = {'referer': 'trade-union'}
        response = view.POST()
        self.assertEqual(response['referer'], 'trade-union')
        self.assertEqual(context.referer, 'trade-union')

    def test_POST_bad_data(self):
        context = self.create_context()
        view = self.View(context, None)
        view.input = {'referer': 'jane'}
        response = view.POST()
        self.assertEqual(response['result'], 'error')

    def test_POST_do_not_clobber_mising_data(self):
        context = self.create_context()
        view = self.View(context, None)
        view.input = {}
        view.POST()
        self.assertEqual(context.country, u'nl')
        self.assertEqual(context.employees, u'1-9')
        self.assertEqual(context.workers_participated, True)
