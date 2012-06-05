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
        request.language = None
        sessions = self.Sessions('sessions', request, account)
        with mock.patch('euphorie.client.api.sessions.get_survey') \
                as mock_get:
            mock_survey = mock_get(request, 'survey/path')
            mock_survey.language = None
            result = sessions['1']
            self.assertTrue(aq_base(result) is survey_session)
            self.assertTrue(aq_parent(result) is sessions)
            self.assertTrue(request.survey is mock_survey)


class ViewTests(EuphorieFunctionalTestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.sessions import View
        return View(*a, **kw)

    def test_do_GET(self):
        import mock
        view = self.View(None, None)
        view.sessions = mock.Mock(return_value='session data')
        self.assertEqual(view.do_GET(), {'sessions': 'session data'})

    def test_do_POST_missing_survey_path(self):
        import mock
        request = mock.Mock()
        view = self.View(None, request)
        view.input = {}
        self.assertEqual(view.do_POST()['type'], 'error')

    def test_do_POST_bad_survey_path(self):
        import mock
        request = mock.Mock()
        request.client.restrictedTraverse.side_effect = KeyError()
        view = self.View(None, request)
        view.input = {'survey': 'bad/path'}
        self.assertEqual(view.do_POST()['type'], 'error')
        request.client.restrictedTraverse.assert_called_once_with(
                ['bad', 'path'])

    def test_do_POST_survey_path_does_not_point_to_survey(self):
        import mock
        request = mock.Mock()
        request.client.restrictedTraverse.return_value = 'thing'
        view = self.View(None, request)
        view.input = {'survey': 'bad/path'}
        self.assertEqual(view.do_POST()['type'], 'error')

    def test_do_POST_survey_without_profile(self):
        from z3c.saconfig import Session
        from AccessControl.SecurityManagement import newSecurityManager
        from zope.publisher.browser import TestRequest
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.model import SurveySession
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        account = addAccount()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        request = TestRequest()
        request.client = self.portal.client
        survey = self.portal.client['nl']['ict']['software-development']
        view = self.View(survey, request)
        view.input = {'survey': 'nl/ict/software-development'}
        newSecurityManager(None, account)
        response = view.do_POST()
        self.assertTrue(
                response['next-step'].endswith('identification'))
        survey_session = Session.query(SurveySession).first()
        self.assertEqual(survey_session.title, u'Software development')
        self.assertTrue(survey_session.hasTree())

    def test_do_POST_survey_specify_title(self):
        from z3c.saconfig import Session
        from AccessControl.SecurityManagement import newSecurityManager
        from zope.publisher.browser import TestRequest
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.model import SurveySession
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        account = addAccount()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        request = TestRequest()
        request.client = self.portal.client
        survey = self.portal.client['nl']['ict']['software-development']
        view = self.View(survey, request)
        view.input = {'survey': 'nl/ict/software-development',
                      'title': u'Alternative title'}
        newSecurityManager(None, account)
        response = view.do_POST()
        self.assertTrue(
                response['next-step'].endswith('identification'))
        survey_session = Session.query(SurveySession).first()
        self.assertEqual(survey_session.title, u'Alternative title')

    def test_do_POST_survey_with_profile(self):
        from z3c.saconfig import Session
        from AccessControl.SecurityManagement import newSecurityManager
        from zope.publisher.browser import TestRequest
        from euphorie.content.tests.utils import PROFILE_SURVEY
        from euphorie.client.model import SurveySession
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        account = addAccount()
        self.loginAsPortalOwner()
        addSurvey(self.portal, PROFILE_SURVEY)
        request = TestRequest()
        request.client = self.portal.client
        survey = self.portal.client['nl']['ict']['software-development']
        view = self.View(survey, request)
        view.input = {'survey': 'nl/ict/software-development'}
        newSecurityManager(None, account)
        response = view.do_POST()
        self.assertTrue(
                response['next-step'].endswith('profile'))
        survey_session = Session.query(SurveySession).first()
        self.assertTrue(not survey_session.hasTree())


class BrowserTests(EuphorieFunctionalTestCase):
    def test_do_GET_basic(self):
        import json
        from euphorie.client.api.authentication import generate_token
        from euphorie.client.tests.utils import addAccount
        account = addAccount()
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['sessions']))
        self.assertEqual(response['sessions'], [])
