# coding=utf-8
from euphorie.client.api.authentication import generate_token
from euphorie.client.api.risk import ActionPlan
from euphorie.client.api.risk import Identification
from euphorie.client.api.risk import View
from euphorie.client.api.tests.utils import _setup_session
from euphorie.client.model import Risk
from euphorie.client.model import Session
from euphorie.content.solution import Solution
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone.namedfile.file import NamedBlobImage
from zope.publisher.browser import TestRequest

import json


DUMMY_GIF = 'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff' \
            '\xff\xff!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00' \
            '\x00\x01\x00\x01\x00\x00\x02\x01L\x00;'


class ViewTests(EuphorieIntegrationTestCase):

    def test_do_GET_minimal(self):
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
        risk = Session.query(Risk).first()
        view = View(risk, request)
        response = view.do_GET()
        self.assertEqual(
            set(response),
            set([
                'id', 'type', 'title', 'module-title', 'problem-description',
                'show-not-applicable', 'evaluation-method', 'present',
                'priority', 'comment'
            ])
        )
        self.assertEqual(response['id'], 2)
        self.assertEqual(response['type'], 'risk')
        self.assertEqual(response['title'], u'Everything is under control.')
        self.assertEqual(response['module-title'], u'Module title.')
        self.assertEqual(
            response['problem-description'], u'Not everything under control.'
        )
        self.assertEqual(response['show-not-applicable'], False)
        self.assertEqual(response['evaluation-method'], 'direct')
        self.assertEqual(response['present'], None)
        self.assertEqual(response['priority'], u'high')

    def test_do_GET_full(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.description = u'<p>Simple description</p>'
        risk.legal_reference = u'<p>Catch 22</p>'
        risk.evaluation_method = 'calculated'
        risk.image2 = NamedBlobImage(
            data=DUMMY_GIF, contentType='image/gif', filename=u'dummy.gif'
        )
        risk.caption2 = u'Secondary Image'
        risk['3'] = Solution(
            description=u'Standard solution 1',
            action_plan=u'Dummy plan',
            requirements=u'Dummy requirements'
        )
        request = TestRequest()
        request.survey = survey
        risk = Session.query(Risk).first()
        risk.skip_children = True
        view = View(risk, request)
        response = view.do_GET()
        self.assertEqual(
            set(response),
            set([
                'id', 'type', 'title', 'module-title', 'problem-description',
                'show-not-applicable', 'evaluation-method', 'present',
                'priority', 'comment', 'description', 'legal-reference',
                'evaluation-algorithm', 'frequency', 'frequency-options',
                'effect', 'effect-options', 'probability',
                'probability-options', 'images', 'standard-solutions'
            ])
        )
        self.assertEqual(response['description'], u'<p>Simple description</p>')
        self.assertEqual(response['legal-reference'], u'<p>Catch 22</p>')
        self.assertEqual(len(response['images']), 2)
        self.assertEqual(len(response['standard-solutions']), 1)
        self.assertEqual(
            response['standard-solutions'][0], {
                'description': u'Standard solution 1',
                'action-plan': u'Dummy plan',
                'prevention-plan': None,
                'requirements': u'Dummy requirements'
            }
        )

    def test_do_GET_use_vocabulary_token(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.title = u'Everything is under control.'
        risk.problem_description = u'Not everything under control.'
        risk.description = None
        risk.evaluation_method = 'calculated'
        request = TestRequest()
        request.survey = survey
        risk = Session.query(Risk).first()
        risk.probability = 3
        risk.frequency = 7
        view = View(risk, request)
        response = view.do_GET()
        self.assertEqual(response['probability'], 'medium')
        self.assertEqual(response['frequency'], 'constant')
        self.assertEqual(response['effect'], None)


class IdentificationTests(EuphorieIntegrationTestCase):

    def Identification(self, *a, **kw):
        return Identification(*a, **kw)

    def test_do_PUT_missing_present_value(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = Session.query(Risk).first()
        view = self.Identification(risk, request)
        view.input = {}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_present_invalid_value(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = Session.query(Risk).first()
        view = self.Identification(risk, request)
        view.input = {'present': 'foo'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_keep_existing_comment(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = Session.query(Risk).first()
        risk.comment = u'Original comment'
        view = self.Identification(risk, request)
        view.input = {'present': 'yes'}
        response = view.do_PUT()
        self.assertEqual(response['comment'], u'Original comment')
        self.assertEqual(risk.comment, u'Original comment')


class ActionPlanTests(EuphorieIntegrationTestCase):

    def ActionPlan(self, *a, **kw):
        return ActionPlan(*a, **kw)

    def test_do_PUT_set_priority_for_top5_risk_not_allowed(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        risk = survey['1']['2']
        risk.type = 'top5'
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = Session.query(Risk).first()
        view = self.ActionPlan(risk, request)
        view.input = {'priority': 'low'}
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_set_priority_for_normal_risk(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)

        risk = survey['1']['2']
        risk.type = 'risk'
        request = TestRequest()
        request.survey = survey
        request.survey_session = survey_session
        risk = Session.query(Risk).first()
        view = self.ActionPlan(risk, request)
        view.input = {'priority': 'low'}
        response = view.do_PUT()
        self.assertEqual(response['priority'], 'low')
        self.assertEqual(risk.priority, 'low')


class BrowserTests(EuphorieFunctionalTestCase):

    def test_get(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/1/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'risk')

    def test_get_translation(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        survey.language = 'nl'
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/1/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        options = dict((opt['value'], opt['title'])
                       for opt in response['frequency-options'])
        self.assertEqual(options['constant'], u'Voortdurend')
