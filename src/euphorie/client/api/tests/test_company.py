# coding=utf-8
from euphorie.client import model
from euphorie.client.api.authentication import generate_token
from euphorie.client.api.company import View
from euphorie.client.model import Company
from euphorie.client.model import SurveySession
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from z3c.saconfig import Session

import datetime
import json
import mock
import unittest


class ViewBrowserTests(EuphorieFunctionalTestCase):

    def test_get_no_company_data_present(self):
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
            title=u'Dummy session',
            created=datetime.datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
            zodb_path='nl/ict/software-development',
            account=account
        )
        Session.add(survey_session)
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open(
            'http://nohost/plone/client/api/users/1/sessions/1/company'
        )
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'company')

    def test_get(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
            title=u'Dummy session',
            created=datetime.datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
            zodb_path='nl/ict/software-development',
            account=account,
            company=Company(country='nl', employees='1-9', referer='other')
        )
        Session.add(survey_session)
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open(
            'http://nohost/plone/client/api/users/1/sessions/1/company'
        )
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'company')


class ViewTests(unittest.TestCase):

    def create_context(self):
        company = Company(
            country=u'nl',
            employees='1-9',
            conductor='both',
            referer='other',
            workers_participated=True,
            needs_met=False,
            recommend_tool=True,
        )
        return SurveySession(company=company)

    def test_do_GET_result(self):
        context = self.create_context()
        view = View(context, None)
        response = view.do_GET()
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(
            set(response),
            set([
                'type', 'country', 'employees', 'conductor', 'referer',
                'workers-participated', 'needs-met', 'recommend-tool'
            ])
        )
        self.assertEqual(response['type'], 'company')

    def test_do_GET_no_company_data(self):
        # Company might not have been created yet
        context = model.SurveySession()
        view = View(context, None)
        view.update()
        self.assertTrue(context.company is not None)
        response = view.do_GET()
        self.assertEqual(response['country'], None)
        self.assertEqual(response['employees'], None)

    def test_do_PUT_returns_info(self):
        context = self.create_context()
        view = View(context, None)
        view.input = {}
        view.do_GET = mock.Mock(return_value='info')
        self.assertEqual(view.do_PUT(), 'info')

    def test_do_PUT_update_data(self):
        context = self.create_context()
        view = View(context, None)
        view.input = {'referer': 'trade-union'}
        response = view.do_PUT()
        self.assertEqual(response['referer'], 'trade-union')
        self.assertEqual(context.company.referer, 'trade-union')

    def test_do_PUT_bad_data(self):
        context = self.create_context()
        view = View(context, None)
        view.input = {'referer': 'jane'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_do_not_clobber_mising_data(self):
        context = self.create_context()
        view = View(context, None)
        view.input = {}
        view.do_PUT()
        self.assertEqual(context.company.country, u'nl')
        self.assertEqual(context.company.employees, u'1-9')
        self.assertEqual(context.company.workers_participated, True)
        self.assertEqual(context.company.needs_met, False)
        self.assertEqual(context.company.recommend_tool, True)
