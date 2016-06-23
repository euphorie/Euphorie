from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


DUMMY_GIF = 'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff' \
            '\xff\xff!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00' \
            '\x00\x01\x00\x01\x00\x00\x02\x01L\x00;'


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
        from euphorie.client.api.risk import View
        return View(*a, **kw)

    def test_do_GET_minimal(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        survey['1'].title = u'Module title.'
        risk = survey['1']['2']
        risk.title = u'Everything is under control.'
        risk.problem_description = u'Not everything under control.'
        risk.description = None
        risk.evaluation_method = 'direct'
        risk.image = None
        request = TestRequest()
        request.survey = survey
        risk = object_session(survey_session).query(Risk).first()
        view = self.View(risk, request)
        response = view.do_GET()
        self.assertEqual(
                set(response),
                set(['id', 'type', 'title', 'module-title',
                      'problem-description', 'show-not-applicable',
                      'evaluation-method', 'present', 'priority', 'comment']))
        self.assertEqual(response['id'], 2)
        self.assertEqual(response['type'], 'risk')
        self.assertEqual(response['title'], u'Everything is under control.')
        self.assertEqual(response['module-title'], u'Module title.')
        self.assertEqual(
                response['problem-description'],
                u'Not everything under control.')
        self.assertEqual(response['show-not-applicable'], False)
        self.assertEqual(response['evaluation-method'], 'direct')
        self.assertEqual(response['present'], None)
        self.assertEqual(response['priority'], u'high')

    def test_do_GET_full(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        from euphorie.content.solution import Solution
        from plone.namedfile.file import NamedBlobImage
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.description = u'<p>Simple description</p>'
        risk.legal_reference = u'<p>Catch 22</p>'
        risk.evaluation_method = 'calculated'
        risk.image2 = NamedBlobImage(data=DUMMY_GIF, contentType='image/gif',
                filename=u'dummy.gif')
        risk.caption2 = u'Secondary Image'
        risk['3'] = Solution(description=u'Standard solution 1',
                action_plan=u'Dummy plan',
                requirements=u'Dummy requirements')
        request = TestRequest()
        request.survey = survey
        risk = object_session(survey_session).query(Risk).first()
        risk.skip_children = True
        view = self.View(risk, request)
        response = view.do_GET()
        self.assertEqual(
                set(response),
                set(['id', 'type', 'title', 'module-title',
                     'problem-description', 'show-not-applicable',
                     'evaluation-method', 'present', 'priority', 'comment',
                     'description', 'legal-reference', 'evaluation-algorithm',
                     'frequency', 'frequency-options',
                     'effect', 'effect-options',
                     'probability', 'probability-options',
                     'images', 'standard-solutions'
                     ]))
        self.assertEqual(response['description'], u'<p>Simple description</p>')
        self.assertEqual(response['legal-reference'], u'<p>Catch 22</p>')
        self.assertEqual(len(response['images']), 2)
        self.assertEqual(len(response['standard-solutions']), 1)
        self.assertEqual(
                response['standard-solutions'][0],
                {'description': u'Standard solution 1',
                 'action-plan': u'Dummy plan',
                 'prevention-plan': None,
                 'requirements': u'Dummy requirements'})

    def test_do_GET_use_vocabulary_token(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.title = u'Everything is under control.'
        risk.problem_description = u'Not everything under control.'
        risk.description = None
        risk.evaluation_method = 'calculated'
        request = TestRequest()
        request.survey = survey
        risk = object_session(survey_session).query(Risk).first()
        risk.probability = 3
        risk.frequency = 7
        view = self.View(risk, request)
        response = view.do_GET()
        self.assertEqual(response['probability'], 'medium')
        self.assertEqual(response['frequency'], 'constant')
        self.assertEqual(response['effect'], None)


class IdentificationTests(EuphorieFunctionalTestCase):
    def Identification(self, *a, **kw):
        from euphorie.client.api.risk import Identification
        return Identification(*a, **kw)

    def test_do_PUT_missing_present_value(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Risk).first()
        view = self.Identification(risk, request)
        view.input = {}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_present_invalid_value(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Risk).first()
        view = self.Identification(risk, request)
        view.input = {'present': 'foo'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_keep_existing_comment(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Risk).first()
        risk.comment = u'Original comment'
        view = self.Identification(risk, request)
        view.input = {'present': 'yes'}
        response = view.do_PUT()
        self.assertEqual(response['comment'], u'Original comment')
        self.assertEqual(risk.comment, u'Original comment')


class ActionPlanTests(EuphorieFunctionalTestCase):
    def ActionPlan(self, *a, **kw):
        from euphorie.client.api.risk import ActionPlan
        return ActionPlan(*a, **kw)

    def test_do_PUT_set_priority_for_top5_risk_not_allowed(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.type = 'top5'
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Risk).first()
        view = self.ActionPlan(risk, request)
        view.input = {'priority': 'low'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_set_priority_for_normal_risk(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Risk
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.type = 'risk'
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = object_session(survey_session).query(Risk).first()
        view = self.ActionPlan(risk, request)
        view.input = {'priority': 'low'}
        response = view.do_PUT()
        self.assertEqual(response['priority'], 'low')
        self.assertEqual(risk.priority, 'low')


class BrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import json
        from euphorie.client.api.authentication import generate_token
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/1/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'risk')

    def test_get_translation(self):
        import json
        from euphorie.client.api.authentication import generate_token
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        survey.language = 'nl'
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/1/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        options = dict((opt['value'], opt['title'])
                           for opt in response['frequency-options'])
        self.assertEqual(options['constant'], u'Voortdurend')
