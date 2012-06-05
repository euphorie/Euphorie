from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class BrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import datetime
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.client.api.authentication import generate_token
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['id', 'survey', 'type', 'created', 'modified',
                     'title', 'next-step']))
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['survey'], 'nl/ict/software-development')
        self.assertEqual(response['type'], 'session')
        self.assertEqual(response['title'], 'Dummy session')
        self.assertEqual(response['created'], '2012-04-22T23:05:12')
        self.assertEqual(response['modified'], '2012-04-23T11:50:30')
        self.assertEqual(
                response['next-step'],
                'http://nohost/plone/client/api/users/1/sessions/1/'
                'identification')

    def test_with_introduction(self):
        import datetime
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.client.api.authentication import generate_token
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey = self.portal.client['nl']['ict']['software-development']
        survey.introduction = u'<p>Fancy intro.</p>'
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertTrue('introduction' in response)
        self.assertEqual(response['introduction'], u'<p>Fancy intro.</p>')


class IdentificationReportTests(EuphorieFunctionalTestCase):
    def test_browser(self):
        import datetime
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.client.api.authentication import generate_token
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.handleErrors = False
        browser.open('http://nohost/plone/client/api/users/1/'
                        'sessions/1/report-identification')
        self.assertEqual(browser.headers['Content-Type'], 'application/rtf')


class ActionPlanReportTests(EuphorieFunctionalTestCase):
    def test_browser(self):
        import datetime
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.client.api.authentication import generate_token
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.handleErrors = False
        browser.open('http://nohost/plone/client/api/users/1/'
                        'sessions/1/report-actionplan')
        self.assertEqual(browser.headers['Content-Type'], 'application/rtf')


class timelineReportTests(EuphorieFunctionalTestCase):
    def test_browser(self):
        import datetime
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.client.api.authentication import generate_token
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.handleErrors = False
        browser.open('http://nohost/plone/client/api/users/1/'
                        'sessions/1/report-timeline')
        self.assertEqual(
                browser.headers['Content-Type'],
                'application/vnd.openxmlformats-'
                                        'officedocument.spreadsheetml.sheet')
