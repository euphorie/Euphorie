from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


def _setup_session(portal):
    from euphorie.content.tests.utils import BASIC_SURVEY
    from euphorie.client.tests.utils import addAccount
    from euphorie.client.tests.utils import addSurvey
    from euphorie.client.session import create_survey_session
    from euphorie.client.profile import set_session_profile
    addSurvey(portal, BASIC_SURVEY)
    survey = portal.client['nl']['ict']['software-development']
    account = addAccount(password='secret')
    survey_session = create_survey_session(u'Dummy session',
            survey, account)
    survey_session = set_session_profile(survey, survey_session, {})
    return (account, survey, survey_session)


class ViewTests(EuphorieFunctionalTestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.module import View
        return View(*a, **kw)

    def test_do_GET_minimal(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Module
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        module = object_session(survey_session).query(Module).first()
        view = self.View(module, request)
        response = view.do_GET()
        self.assertEqual(
                set(response),
                set(['id', 'type', 'title', 'description', 'optional']))
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['type'], 'module')
        self.assertEqual(response['title'], u'Module one')
        self.assertEqual(response['description'], u'Quick description')
        self.assertEqual(response['optional'], False)

    def test_do_GET_full(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Module
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        module = survey['1']
        module.description = u'<p>Simple description</p>'
        module.solution_direction = u'<p>Fix It Fast</p>'
        module.optional = True
        module.question = u'Is this needed?'
        request = TestRequest()
        request.survey = survey
        module = object_session(survey_session).query(Module).first()
        module.skip_children = True
        view = self.View(module, request)
        response = view.do_GET()
        self.assertEqual(
                set(response),
                set(['id', 'type', 'title', 'optional',
                     'description', 'solution-direction',
                     'question', 'skip-children']))
        self.assertEqual(response['description'], u'<p>Simple description</p>')
        self.assertEqual(response['solution-direction'], u'<p>Fix It Fast</p>')
        self.assertEqual(response['question'], u'Is this needed?')
        self.assertEqual(response['skip-children'], True)


class IdentificationTests(EuphorieFunctionalTestCase):
    def Identification(self, *a, **kw):
        from euphorie.client.api.module import Identification
        return Identification(*a, **kw)

    def test_do_POST_missing_value(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Module
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        module = survey['1']
        module.optional = True
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Module).first()
        view = self.Identification(risk, request)
        view.input = {}
        response = view.do_POST()
        self.assertEqual(response['type'], 'error')

    def test_do_POST_invalid_value(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Module
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        module = survey['1']
        module.optional = True
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Module).first()
        view = self.Identification(risk, request)
        view.input = {'skip-children': 'yes'}
        response = view.do_POST()
        self.assertEqual(response['type'], 'error')

    def test_do_POST_update_value(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Module
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        module = survey['1']
        module.optional = True
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        module = object_session(survey_session).query(Module).first()
        view = self.Identification(module, request)
        view.input = {'skip-children': True}
        response = view.do_POST()
        self.assertEqual(response['skip-children'], True)
        self.assertEqual(module.skip_children, True)


class BrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import json
        from euphorie.client.api.authentication import generate_token
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'module')
