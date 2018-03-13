# coding=utf-8
from euphorie.client.api.sector import View
from euphorie.client.sector import ClientSector
from euphorie.client.tests.utils import addSurvey
from euphorie.content.survey import Survey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.ghost import PathGhost
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone.folder.default import DefaultOrdering
from zope.annotation.attribute import AttributeAnnotations
from zope.component import provideAdapter
from zope.publisher.browser import TestRequest

import json


class ViewTests(EuphorieIntegrationTestCase):

    def setUp(self):
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)

    def View(self, *a, **kw):
        return View(*a, **kw)

    def test_plain_view(self):
        sector = ClientSector(id='ict', title=u'ICT')
        response = self.View(sector, TestRequest()).do_GET()
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(set(response), set(['id', 'title', 'surveys']))
        self.assertEqual(response['id'], 'ict')
        self.assertEqual(response['title'], u'ICT')
        self.assertEqual(response['surveys'], [])

    def test_survey_info(self):
        sector = ClientSector(id='ict', title=u'ICT')
        sector._setOb(
            'gaming',
            Survey(id='gaming', title=u'Gaming', language='nl'),
        )
        response = self.View(sector, TestRequest()).do_GET()
        self.assertEqual(len(response['surveys']), 1)
        survey_info = response['surveys'][0]
        self.assertTrue(isinstance(survey_info, dict))
        self.assertEqual(set(survey_info), set(['id', 'title', 'language']))
        self.assertEqual(survey_info['id'], 'gaming')
        self.assertEqual(survey_info['title'], u'Gaming')
        self.assertEqual(survey_info['language'], 'nl')

    def test_ignore_non_survey_child(self):
        sector = ClientSector(id='ict', title=u'ICT')
        sector['gaming'] = PathGhost('gaming')
        response = self.View(sector, TestRequest()).do_GET()
        self.assertEqual(response['surveys'], [])

    def test_survey_info_filter_by_language(self):
        sector = ClientSector(id='ict', title=u'ICT')
        sector._setOb(
            'gaming',
            Survey(id='gaming', title=u'Gaming', language='nl'),
        )
        request = TestRequest()
        request.form['language'] = 'en'
        response = self.View(sector, request).do_GET()
        self.assertEqual(len(response['surveys']), 0)
        request.form['language'] = 'nl'
        response = self.View(sector, request).do_GET()
        self.assertEqual(len(response['surveys']), 1)


class BrowserTests(EuphorieFunctionalTestCase):

    def test_get(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        browser.open('http://nohost/plone/client/api/surveys/nl/ict')
        response = json.loads(browser.contents)
        self.assertEqual(response['id'], 'ict')
