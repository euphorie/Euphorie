import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class list_sectors_tests(unittest.TestCase):
    def list_sectors(self, *a, **kw):
        from ..sectors import list_sectors
        return list_sectors(*a, **kw)

    def test_ignore_other_children(self):
        from ...countrymanager import CountryManager
        country = {'sector': CountryManager()}
        self.assertEqual(self.list_sectors(country), [])

    def test_info(self):
        from ...sector import Sector
        country = {'sector': Sector(id='sector', title=u'IT Development',
                                    login='sector', locked=False)}
        sectors = self.list_sectors(country)
        self.assertEqual(len(sectors), 1)
        info = sectors[0]
        self.assertEqual(
                set(info),
                set(['id', 'title', 'login', 'locked']))
        self.assertEqual(info['id'], 'sector')
        self.assertEqual(info['title'], u'IT Development')
        self.assertEqual(info['login'], 'sector')
        self.assertEqual(info['locked'], False)


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from ..sectors import View
        return View(*a, **kw)

    def test_return(self):
        import mock
        view = self.View('context', 'request')
        with mock.patch('euphorie.content.api.sectors.list_sectors',
                return_value='mgr-list') as mock_list_sectors:
            self.assertEqual(view.do_GET(), {'sectors': 'mgr-list'})
            mock_list_sectors.assert_called_once_with('context')


class SectorsTests(unittest.TestCase):
    def Sectors(self, *a, **kw):
        from ..sectors import Sectors
        return Sectors(*a, **kw)

    def test_getitem_unknown_key(self):
        country = {}
        sectors = self.Sectors('id', None, country)
        self.assertRaises(KeyError, sectors.__getitem__, 'key')

    def test_getitem_not_a_sector(self):
        country = {'key': u'Sector'}
        sectors = self.Sectors('id', None, country)
        self.assertRaises(KeyError, sectors.__getitem__, 'key')

    def test_getitem__sector(self):
        from Acquisition import aq_base
        from Acquisition import aq_parent
        from ...sector import Sector
        country = {'key': Sector()}
        sectors = self.Sectors('id', None, country)
        sector = sectors['key']
        self.assertTrue(aq_base(sector) is country['key'])
        self.assertTrue(aq_parent(sector) is sectors)


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_require_authentication(self):
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl/sectors')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        import json
        from ...tests.utils import createSector
        from ..authentication import generate_token
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries/de/sectors')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['sectors']))
        self.assertEqual(response['sectors'], [])

    def test_add_new_sector(self):
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
        browser.post('http://nohost/plone/api/countries/nl/sectors',
                json.dumps({'title': u'IT development',
                            'login': 'it',
                            'contact': {
                                'name': u'Jony Smith',
                                'email': u'jony@example.com',
                            },
                            'password': u'cobol-for-the-win'}))
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'sector')
        self.assertEqual(response['id'], 'it-development')
        self.assertTrue('it-development' in country)
        sector = country['it-development']
        self.assertEqual(sector.title, u'IT development')
        self.assertEqual(sector.login, 'it')
        self.assertEqual(sector.password, u'cobol-for-the-win')
