# coding=utf-8
from ...countrymanager import CountryManager
from ...tests.utils import createSector
from ..authentication import generate_token
from ..countrymanager import View
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zExceptions import Unauthorized

import json
import mock


class ViewTests(EuphorieIntegrationTestCase):

    def test_do_GET_basic(self):
        context = CountryManager(
            id='manager',
            title=u'Country Manager',
            contact_email='manager@example.com',
            login='mememe',
            locked=True
        )
        view = View(context, None)
        response = view.do_GET()
        self.assertEqual(
            set(response),
            set(['type', 'id', 'title', 'email', 'login', 'locked'])
        )
        self.assertEqual(response['type'], 'countrymanager')
        self.assertEqual(response['id'], 'manager')
        self.assertEqual(response['title'], u'Country Manager')
        self.assertEqual(response['email'], 'manager@example.com')
        self.assertEqual(response['login'], 'mememe')
        self.assertEqual(response['locked'], True)

    def test_do_PUT_update_error(self):
        view = View(None, None)
        view.update_object = mock.Mock(side_effect=ValueError)
        view.input = {'email': 'other'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_response(self):
        view = View(None, None)
        view.update_object = mock.Mock()
        view.do_GET = mock.Mock(return_value='info')
        self.assertEqual(view.do_PUT(), 'info')

    def test_do_DELETE_no_permission(self):
        with api.env.adopt_user('admin'):
            container = self.portal.sectors['nl']
            container['manager'] = CountryManager(id='manager')
        with api.env.adopt_user('client'):
            view = View(container['manager'], None)
            self.assertRaises(Unauthorized, view.do_DELETE)

    def test_do_DELETE_with_permission(self):
        container = self.portal.sectors['nl']
        container['manager'] = CountryManager(id='manager')
        view = View(container['manager'], None)
        self.loginAsPortalOwner()
        view.do_DELETE()
        self.assertTrue('manager' not in container)


class ViewFunctionalTests(EuphorieFunctionalTestCase):

    def View(self, *a, **kw):
        return View(*a, **kw)

    def test_browser_require_authentication(self):
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory(
            'euphorie.countrymanager', 'manager'
        )
        browser = self.get_browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl/managers/manager')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_browser_authenticated_user(self):
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory(
            'euphorie.countrymanager', 'manager'
        )
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = self.get_browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries/nl/managers/manager')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'countrymanager')

    def test_browser_sector_can_not_modify_manager(self):
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory(
            'euphorie.countrymanager', 'manager'
        )
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = self.get_browser()
        browser.raiseHttpErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        with mock.patch(
            'mechanize._opener.Request.get_method', return_value='PUT'
        ):
            browser.post(
                'http://nohost/plone/api/countries/nl/managers/manager',
                '{"title": "Hacked!"}'
            )
            response = json.loads(browser.contents)
            self.assertEqual(response['type'], 'error')
