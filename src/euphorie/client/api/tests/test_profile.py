# coding=utf-8
from euphorie.client.api.authentication import generate_token
from euphorie.client.api.profile import View
from euphorie.client.model import SurveySession
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.profilequestion import ProfileQuestion
from euphorie.content.survey import Survey
from euphorie.content.tests.utils import PROFILE_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from z3c.saconfig import Session

import datetime
import json
import mock


class ViewTests(EuphorieIntegrationTestCase):

    def View(self, *a, **kw):
        return View(*a, **kw)

    def test_get_no_profile(self):
        survey = Survey(id='5')
        view = self.View(survey, None)
        view.survey = mock.Mock(return_value=survey)
        with mock.patch('euphorie.client.api.profile.extractProfile') \
                as mock_extractProfile:
            mock_extractProfile.return_value = {}
            response = view.do_GET()
            self.assertEqual(response['profile'], [])

    def test_get_with_profile(self):
        self.portal.survey = Survey(id='survey')
        survey = self.portal.survey
        survey._setOb('5', ProfileQuestion(id='5', question=u'Locations'))
        view = self.View(survey, None)
        view.survey = mock.Mock(return_value=survey)
        with mock.patch('euphorie.client.api.profile.extractProfile') \
                as mock_extractProfile:
            mock_extractProfile.return_value = {'5': [u'London', u'Tokyo']}
            response = view.do_GET()
            profile = response['profile']
            self.assertEqual(
                profile, [{
                    'id': '5',
                    'question': u'Locations',
                    'value': [u'London', u'Tokyo']
                }]
            )

    def test_put_no_profile(self):
        account = addAccount(password='secret')
        survey_session = SurveySession(
            title=u'Dummy session',
            zodb_path='nl/ict/software-development',
            account=account
        )
        view = self.View(survey_session, None)
        view.input = {}
        Session.add(survey_session)
        survey = Survey(id='survey')
        view.survey = mock.Mock(return_value=survey)
        with mock.patch('euphorie.client.api.profile.extractProfile') \
                as mock_extractProfile:
            mock_extractProfile.return_value = {}
            response = view.do_PUT()
            self.assertEqual(response['profile'], [])

    def test_put_too_much_data(self):
        import mock
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.model import SurveySession
        from euphorie.content.survey import Survey
        account = addAccount(password='secret')
        survey_session = SurveySession(
            title=u'Dummy session',
            zodb_path='nl/ict/software-development',
            account=account
        )
        view = self.View(survey_session, None)
        view.input = {'5': True}
        survey = Survey(id='survey')
        view.survey = mock.Mock(return_value=survey)
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_put_not_all_questions_answered(self):
        import mock
        from euphorie.content.survey import Survey
        from euphorie.content.profilequestion import ProfileQuestion
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.model import SurveySession
        account = addAccount(password='secret')
        survey_session = SurveySession(
            title=u'Dummy session',
            zodb_path='nl/ict/software-development',
            account=account
        )
        view = self.View(survey_session, None)
        view.input = {}
        self.portal.survey = Survey(id='survey')
        survey = self.portal.survey
        survey._setOb('5', ProfileQuestion(id='5', question=u'Locations'))
        view.survey = mock.Mock(return_value=survey)
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')


class BrowserTests(EuphorieFunctionalTestCase):

    def test_get_empty_profile(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, PROFILE_SURVEY)
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
            'http://nohost/plone/client/api/users/1/sessions/1/profile'
        )
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
            set(response), set(['id', 'type', 'title', 'profile'])
        )
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['type'], 'profile')
        self.assertEqual(response['title'], u'Dummy session')
        self.assertEqual(
            response['profile'], [{
                'id': u'1',
                'question': u'List all your departments:',
                'value': []
            }]
        )
