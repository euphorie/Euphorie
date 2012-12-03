import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from ..sector import View
        return View(*a, **kw)

    def test_do_GET_basic(self):
        from ...sector import Sector
        context = Sector(id='it', title=u'IT Development',
                contact_name=u'Manager', contact_email='manager@example.com',
                login='itdev', locked=True)
        view = self.View(context, None)
        response = view.do_GET()
        self.assertEqual(
                set(response),
                set(['type', 'id', 'title', 'contact', 'login', 'locked']))
        self.assertEqual(response['type'], 'sector')
        self.assertEqual(response['id'], 'it')
        self.assertEqual(response['title'], u'IT Development')
        self.assertEqual(
                response['contact'],
                {'name': u'Manager', 'email': 'manager@example.com'})
        self.assertEqual(response['login'], 'itdev')
        self.assertEqual(response['locked'], True)

    def test_do_PUT_update_error(self):
        import mock
        view = self.View(None, None)
        view.update_object = mock.Mock(side_effect=ValueError)
        view.input = {'locked': True}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_response(self):
        import mock
        view = self.View(None, None)
        view.update_object = mock.Mock()
        view.do_GET = mock.Mock(return_value='info')
        self.assertEqual(view.do_PUT(), 'info')


class ViewFunctionalTests(EuphorieFunctionalTestCase):
    def View(self, *a, **kw):
        from ..sector import View
        return View(*a, **kw)

    def test_do_DELETE_no_permission(self):
        from zExceptions import Unauthorized
        from ...sector import Sector
        container = self.portal.sectors['nl']
        container['it'] = Sector(id='manager')
        view = self.View(container['it'], None)
        self.assertRaises(Unauthorized, view.do_DELETE)

    def test_do_DELETE_with_permission(self):
        from ...sector import Sector
        container = self.portal.sectors['nl']
        container['it'] = Sector(id='it')
        view = self.View(container['it'], None)
        self.loginAsPortalOwner()
        view.do_DELETE()
        self.assertTrue('it' not in container)

    def test_browser_require_authentication(self):
        self.loginAsPortalOwner()
        self.portal.sectors['nl'].invokeFactory('euphorie.countrymanager', 'manager')
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries/nl/managers/manager')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_browser_authenticated_user(self):
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
