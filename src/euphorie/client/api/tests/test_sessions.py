import unittest
from zope.component.testing import PlacelessSetup
from euphorie.client.tests.database import DatabaseTests
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class SessionsTests(DatabaseTests):
    def Sessions(self, *a, **kw):
        from euphorie.client.api.sessions import Sessions
        return Sessions(*a, **kw)

    def test_getitem_invalid_key(self):
        from euphorie.client.tests.utils import addAccount
        account = addAccount()
        sessions = self.Sessions('sessions', None, account)
        self.assertRaises(KeyError, sessions.__getitem__, 'ABC')

    def test_getitem_unknown_session(self):
        from euphorie.client.tests.utils import addAccount
        account = addAccount()
        sessions = self.Sessions('sessions', None, account)
        self.assertRaises(KeyError, sessions.__getitem__, '15')

    def test_getitem_removed_session(self):
        # Corner case: admin removed survey, but survey session still exists
        import mock
        from sqlalchemy.orm import object_session
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.model import SurveySession
        account = addAccount()
        survey_session = SurveySession(title=u'Dummy',
                zodb_path='does/not/exist', account=account)
        object_session(account).add(survey_session)
        sessions = self.Sessions('sessions', None, account)
        with mock.patch('euphorie.client.api.sessions.get_survey') \
                as mock_get:
            mock_get.return_value = None
            self.assertRaises(KeyError, sessions.__getitem__, '1')

    def test_getitem_valid_session(self):
        import mock
        from sqlalchemy.orm import object_session
        from Acquisition import aq_base
        from Acquisition import aq_parent
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.model import SurveySession
        account = addAccount()
        survey_session = SurveySession(title=u'Dummy',
                zodb_path='survey/path', account=account)
        object_session(account).add(survey_session)
        request = mock.Mock()
        sessions = self.Sessions('sessions', request, account)
        with mock.patch('euphorie.client.api.sessions.get_survey') \
                as mock_get:
            mock_get.return_value = 'mock-survey'
            result = sessions['1'] 
            self.assertTrue(aq_base(result) is survey_session)
            self.assertTrue(aq_parent(result) is sessions)
            mock_get.assert_called_once_with(request, 'survey/path')
            self.assertEqual(request.survey, 'mock-survey')


class ViewTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        from zope.component import provideAdapter
        from zope.annotation.attribute import AttributeAnnotations
        from plone.folder.default import DefaultOrdering
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)


class BrowserTests(EuphorieFunctionalTestCase):
    def test_GET_basic(self):
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        account = Account(loginname='john', password=u'jane')
        Session.add(account)
        browser = Browser()
        browser.open('http://nohost/plone/client/api/users/1/sessions')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['sessions']))
        self.assertEqual(response['sessions'], [])
