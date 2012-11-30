import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from ..countrymanager import View
        return View(*a, **kw)

    def test_do_GET_basic(self):
        from ...countrymanager import CountryManager
        context = CountryManager(id='manager', title=u'Country Manager',
                contact_email='manager@example.com', login='mememe',
                locked=True)
        view = self.View(context, None)
        response = view.do_GET()
        self.assertEqual(
                set(response),
                set(['type', 'id', 'title', 'email', 'login', 'locked']))
        self.assertEqual(response['type'], 'countrymanager')
        self.assertEqual(response['id'], 'manager')
        self.assertEqual(response['title'], u'Country Manager')
        self.assertEqual(response['email'], 'manager@example.com')
        self.assertEqual(response['login'], 'mememe')
        self.assertEqual(response['locked'], True)

    def test_do_PUT_no_permission(self):
        import mock
        from zExceptions import Unauthorized
        view = self.View(None, None)
        view.input = {'email': 'other'}
        view.has_permission = mock.Mock(return_value=False)
        self.assertRaises(Unauthorized, view.do_PUT)

    def test_do_PUT_update_basics(self):
        import mock
        from ...countrymanager import CountryManager
        manager = CountryManager(id='id', login='login')
        view = self.View(manager, None)
        view.input = {'title': u'New title',
                      'email': 'email@example.com',
                      'password': u'Password',
                      'locked': True,
                      }
        view.has_permission = mock.Mock(return_value=True)
        view.do_PUT()
        self.assertEqual(manager.title, u'New title')
        self.assertEqual(manager.contact_email, 'email@example.com')
        self.assertEqual(manager.password, u'Password')
        self.assertEqual(manager.locked, True)

    def test_do_PUT_validate_fields(self):
        import mock
        from ...countrymanager import CountryManager
        manager = CountryManager(locked=False)
        view = self.View(manager, None)
        view.input = {'locked': 'oops'}
        view.has_permission = mock.Mock(return_value=True)
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')
        self.assertEqual(manager.locked, False)


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_require_authentication(self):
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory('euphorie.countrymanager', 'manager')
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl/managers/manager')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        import json
        from ...tests.utils import createSector
        from ..authentication import generate_token
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory('euphorie.countrymanager', 'manager')
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries/nl/managers/manager')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'countrymanager')

    def test_sector_can_not_modify_manager(self):
        import mock
        import json
        from ...tests.utils import createSector
        from ..authentication import generate_token
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory('euphorie.countrymanager', 'manager')
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        with mock.patch('mechanize._opener.Request.get_method', return_value='PUT'):
            browser.post('http://nohost/plone/api/countries/nl/managers/manager',
                    '{"title": "Hacked!"}')
            response = json.loads(browser.contents)
            self.assertEqual(response['type'], 'error')
