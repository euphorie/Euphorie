from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class BrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import datetime
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                modified=datetime.datetime(2012, 4, 22, 23, 5, 12),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.open('http://nohost/plone/client/api/users/1/sessions/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['id', 'type', 'modified', 'title']))
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['type'], 'session')
        self.assertEqual(response['title'], 'Dummy session')
        self.assertEqual(response['modified'], '2012-04-22T23:05:12')
