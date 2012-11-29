import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class country_info_tests(unittest.TestCase):
    def country_info(self, *a, **kw):
        from ..country import country_info
        return country_info(*a, **kw)

    def test_data(self):
        from ...country import Country
        country = Country(id='nl', title=u'The Netherlands',
                          country_type='eu-member')
        info = self.country_info(country)
        self.assertEqual(set(info), set(['id', 'title', 'country-type']))
        self.assertEqual(info['id'], 'nl')
        self.assertEqual(info['title'], u'The Netherlands')
        self.assertEqual(info['country-type'], 'eu-member')


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from ..country import View
        return View(*a, **kw)

    def test_list_managers_ignore_other_children(self):
        from ...sector import Sector
        country = {'sector': Sector()}
        view = self.View(country, None)
        self.assertEqual(view.list_managers(), [])

    def test_list_managers_info(self):
        from ...countrymanager import CountryManager
        country = {'manager': CountryManager(id='manager', title=u'Jane Doe',
                                             login='manager',
                                             contact_email='jane@example.com',
                                             locked=True)}
        view = self.View(country, None)
        managers = view.list_managers()
        self.assertEqual(len(managers), 1)
        info = managers[0]
        self.assertEqual(
                set(info),
                set(['id', 'title', 'login', 'email', 'locked']))
        self.assertEqual(info['id'], 'manager')
        self.assertEqual(info['title'], u'Jane Doe')
        self.assertEqual(info['login'], 'manager')
        self.assertEqual(info['email'], 'jane@example.com')
        self.assertEqual(info['locked'], True)

    def test_list_sectors_ignore_other_children(self):
        from ...countrymanager import CountryManager
        country = {'manager': CountryManager()}
        view = self.View(country, None)
        self.assertEqual(view.list_sectors(), [])

    def test_list_sectors_info(self):
        from ...sector import Sector
        country = {}
        country['sector'] = Sector(id='sector', title=u'IT Development',
                    login='sector', locked=False)
        view = self.View(country, None)
        sectors = view.list_sectors()
        self.assertEqual(len(sectors), 1)
        info = sectors[0]
        self.assertEqual(
                set(info),
                set(['id', 'title', 'login', 'locked']))
        self.assertEqual(info['id'], 'sector')
        self.assertEqual(info['title'], u'IT Development')
        self.assertEqual(info['login'], 'sector')
        self.assertEqual(info['locked'], False)

    def test_do_GET_basic(self):
        import mock
        from zope.publisher.browser import TestRequest
        view = self.View('context', TestRequest())
        with mock.patch('euphorie.content.api.country.country_info',
                return_value={'foo': 'bar'}) as mock_country_info:
            self.assertEqual(view.do_GET(), {'type': 'country',
                                             'foo': 'bar'})
            mock_country_info.assert_called_once_with('context')

    def test_do_GET_details(self):
        import mock
        from zope.publisher.browser import TestRequest
        view = self.View('context', TestRequest())
        view.request.form['details'] = ''
        view.list_managers = mock.Mock(return_value='mgr-list')
        view.list_sectors = mock.Mock(return_value='sector-list')
        with mock.patch('euphorie.content.api.country.country_info',
                return_value={}):
            info = view.do_GET()
            self.assertEqual(info['managers'], 'mgr-list')
            self.assertEqual(info['sectors'], 'sector-list')


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_require_authentication(self):
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        import json
        from ...tests.utils import createSector
        from ..authentication import generate_token
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries/nl')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['type', 'id', 'title', 'country-type']))
        self.assertEqual(response['type'], u'country')
        self.assertEqual(response['id'], u'nl')
