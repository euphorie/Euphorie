import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class list_managers_tests(unittest.TestCase):
    def list_managers(self, *a, **kw):
        from ..managers import list_managers
        return list_managers(*a, **kw)

    def test_ignore_other_children(self):
        from ...sector import Sector
        country = {'sector': Sector()}
        self.assertEqual(self.list_managers(country), [])

    def test_info(self):
        from ...countrymanager import CountryManager
        country = {'manager': CountryManager(id='manager', title=u'Jane Doe',
                                             login='manager',
                                             contact_email='jane@example.com',
                                             locked=True)}
        managers = self.list_managers(country)
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


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from ..managers import View
        return View(*a, **kw)

    def test_return(self):
        import mock
        view = self.View('context', 'request')
        with mock.patch('euphorie.content.api.managers.list_managers',
                return_value='mgr-list') as mock_list_managers:
            self.assertEqual(view.do_GET(), {'managers': 'mgr-list'})
            mock_list_managers.assert_called_once_with('context')


class ManagersTests(unittest.TestCase):
    def Managers(self, *a, **kw):
        from ..managers import Managers
        return Managers(*a, **kw)

    def test_getitem_unknown_key(self):
        country = {}
        managers = self.Managers('id', None, country)
        self.assertRaises(KeyError, managers.__getitem__, 'key')

    def test_getitem_not_a_country_manager(self):
        country = {'key': u'Sector'}
        managers = self.Managers('id', None, country)
        self.assertRaises(KeyError, managers.__getitem__, 'key')

    def test_getitem__country_manager(self):
        from Acquisition import aq_base
        from Acquisition import aq_parent
        from ...countrymanager import CountryManager
        country = {'key': CountryManager()}
        managers = self.Managers('id', None, country)
        mgr = managers['key']
        self.assertTrue(aq_base(mgr) is country['key'])
        self.assertTrue(aq_parent(mgr) is managers)


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_require_authentication(self):
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl/managers')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        import json
        from ...tests.utils import createSector
        from ..authentication import generate_token
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries/nl/managers')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['managers']))
        self.assertEqual(response['managers'], [])

    def test_add_new_manager(self):
        import json
        from ..authentication import generate_token
        self.loginAsPortalOwner()
        country = self.portal.sectors['nl']
        country.invokeFactory('euphorie.countrymanager', 'manager',
                login='manager', password=u'manager')
        browser = Browser()
        browser.handleErrors = False
        browser.raiseHttpErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(country['manager']))
        browser.post('http://nohost/plone/api/countries/nl/managers',
                json.dumps({'title': u'Jane Doe',
                            'login': 'jane',
                            'password': u'johny'}))
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'countrymanager')
        self.assertEqual(response['id'], 'jane-doe')
        self.assertTrue('jane-doe' in country)
        jane = country['jane-doe']
        self.assertEqual(jane.title, u'Jane Doe')
        self.assertEqual(jane.login, 'jane')
        self.assertEqual(jane.password, u'johny')
