# coding=utf-8
from euphorie.client.api.authentication import generate_token
from euphorie.client.api.module import Identification
from euphorie.client.api.tests.utils import _setup_session
from euphorie.client.model import Module
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from sqlalchemy.orm import object_session
from zope.publisher.browser import TestRequest

import json


DUMMY_GIF = 'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff' \
            '\xff\xff!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00' \
            '\x00\x01\x00\x01\x00\x00\x02\x01L\x00;'


class ViewTests(EuphorieIntegrationTestCase):

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
            set(['id', 'type', 'title', 'description', 'optional'])
        )
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['type'], 'module')
        self.assertEqual(response['title'], u'Module one')
        self.assertEqual(response['description'], u'Quick description')
        self.assertEqual(response['optional'], False)

    def test_do_GET_full(self):
        from sqlalchemy.orm import object_session
        from zope.publisher.browser import TestRequest
        from euphorie.client.model import Module
        from plone.namedfile.file import NamedBlobImage
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        module = survey['1']
        module.description = u'<p>Simple description</p>'
        module.solution_direction = u'<p>Fix It Fast</p>'
        module.optional = True
        module.question = u'Is this needed?'
        module.image = NamedBlobImage(
            data=DUMMY_GIF, contentType='image/gif', filename=u'dummy.gif'
        )
        module.caption = u'Key Image'
        request = TestRequest()
        request.survey = survey
        module = object_session(survey_session).query(Module).first()
        module.skip_children = True
        view = self.View(module, request)
        response = view.do_GET()
        self.assertEqual(
            set(response),
            set([
                'id', 'type', 'title', 'optional', 'image', 'description',
                'solution-direction', 'question', 'skip-children'
            ])
        )
        self.assertEqual(response['description'], u'<p>Simple description</p>')
        self.assertEqual(response['solution-direction'], u'<p>Fix It Fast</p>')
        self.assertEqual(response['question'], u'Is this needed?')
        self.assertEqual(response['skip-children'], True)
        self.assertEqual(
            set(response['image']), set(['thumbnail', 'original', 'caption'])
        )
        self.assertEqual(response['image']['caption'], u'Key Image')
        self.assertEqual(
            response['image']['original'],
            u'http://nohost/plone/client/nl/ict/software-development/1/'
            '@@download/image/dummy.gif'
        )
        self.assertTrue(
            response['image']['thumbnail'].startswith(
                u'http://nohost/plone/client/nl/ict/software-development'
                '/1/@@images/'
            )
        )


class IdentificationTests(EuphorieIntegrationTestCase):

    def Identification(self, *a, **kw):
        return Identification(*a, **kw)

    def test_do_PUT_missing_value(self):
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
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_invalid_value(self):
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
        response = view.do_PUT()
        self.assertEqual(response['type'], 'error')

    def test_do_PUT_update_value(self):
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
        response = view.do_PUT()
        self.assertEqual(response['skip-children'], True)
        self.assertEqual(module.skip_children, True)


class BrowserTests(EuphorieFunctionalTestCase):

    def test_get(self):
        self.loginAsPortalOwner()
        (account, survey, survey_session) = _setup_session(self.portal)
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open('http://nohost/plone/client/api/users/1/sessions/1/1')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'module')
