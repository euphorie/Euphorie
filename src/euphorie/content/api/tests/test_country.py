# coding=utf-8
from ...country import Country
from ...tests.utils import createSector
from ..authentication import generate_token
from ..country import country_info
from ..country import View
from euphorie.testing import EuphorieFunctionalTestCase
from zope.publisher.browser import TestRequest

import json
import mock
import unittest


class country_info_tests(unittest.TestCase):

    def country_info(self, *a, **kw):
        return country_info(*a, **kw)

    def test_data(self):
        country = Country(
            id='nl', title=u'The Netherlands', country_type='eu-member'
        )
        info = self.country_info(country)
        self.assertEqual(set(info), set(['id', 'title', 'country-type']))
        self.assertEqual(info['id'], 'nl')
        self.assertEqual(info['title'], u'The Netherlands')
        self.assertEqual(info['country-type'], 'eu-member')


class ViewTests(unittest.TestCase):

    def test_do_GET_basic(self):
        view = View('context', TestRequest())
        with mock.patch(
            'euphorie.content.api.country.country_info',
            return_value={
                'foo': 'bar'
            }
        ) as mock_country_info:
            self.assertEqual(view.do_GET(), {'type': 'country', 'foo': 'bar'})
            mock_country_info.assert_called_once_with('context')

    def test_do_GET_details(self):
        view = View('context', TestRequest())
        view.request.form['details'] = ''
        with mock.patch(
            'euphorie.content.api.country.country_info', return_value={}
        ):
            with mock.patch(
                'euphorie.content.api.country.list_managers',
                return_value='mgr-list'
            ):
                with mock.patch(
                    'euphorie.content.api.country.list_sectors',
                    return_value='sector-list'
                ):
                    info = view.do_GET()
                    self.assertEqual(info['managers'], 'mgr-list')
                    self.assertEqual(info['sectors'], 'sector-list')


class ViewBrowserTests(EuphorieFunctionalTestCase):

    def test_require_authentication(self):
        browser = self.get_browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = self.get_browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries/nl')
        response = json.loads(browser.contents)
        self.assertEqual(
            set(response), set(['type', 'id', 'title', 'country-type'])
        )
        self.assertEqual(response['type'], u'country')
        self.assertEqual(response['id'], u'nl')
