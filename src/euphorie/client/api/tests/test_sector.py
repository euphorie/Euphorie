import unittest
from zope.component.testing import PlacelessSetup
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        from zope.component import provideAdapter
        from zope.annotation.attribute import AttributeAnnotations
        from plone.folder.default import DefaultOrdering
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)

    def View(self, *a, **kw):
        from euphorie.client.api.sector import View
        return View(*a, **kw)

    def test_plain_view(self):
        from zope.publisher.browser import TestRequest
        from euphorie.client.sector import ClientSector
        sector = ClientSector(id='ict', title=u'ICT')
        response = self.View(sector, TestRequest()).do_GET()
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(
                set(response),
                set(['id', 'title', 'surveys']))
        self.assertEqual(response['id'], 'ict')
        self.assertEqual(response['title'], u'ICT')
        self.assertEqual(response['surveys'], [])

    def test_survey_info(self):
        from zope.publisher.browser import TestRequest
        from euphorie.content.survey import Survey
        from euphorie.client.sector import ClientSector
        sector = ClientSector(id='ict', title=u'ICT')
        sector['gaming'] = Survey(id='gaming', title=u'Gaming',
                language='nl')
        response = self.View(sector, TestRequest()).do_GET()
        self.assertEqual(len(response['surveys']), 1)
        survey_info = response['surveys'][0]
        self.assertTrue(isinstance(survey_info, dict))
        self.assertEqual(set(survey_info), set(['id', 'title', 'language']))
        self.assertEqual(survey_info['id'], 'gaming')
        self.assertEqual(survey_info['title'], u'Gaming')
        self.assertEqual(survey_info['language'], 'nl')

    def test_ignore_non_survey_child(self):
        from zope.publisher.browser import TestRequest
        from euphorie.ghost import PathGhost
        from euphorie.client.sector import ClientSector
        sector = ClientSector(id='ict', title=u'ICT')
        sector['gaming'] = PathGhost('gaming')
        response = self.View(sector, TestRequest()).do_GET()
        self.assertEqual(response['surveys'], [])

    def test_survey_info_filter_by_language(self):
        from zope.publisher.browser import TestRequest
        from euphorie.content.survey import Survey
        from euphorie.client.sector import ClientSector
        sector = ClientSector(id='ict', title=u'ICT')
        sector['gaming'] = Survey(id='gaming', title=u'Gaming',
                language='nl')
        request = TestRequest()
        request.form['language'] = 'en'
        response = self.View(sector, request).do_GET()
        self.assertEqual(len(response['surveys']), 0)
        request.form['language'] = 'nl'
        response = self.View(sector, request).do_GET()
        self.assertEqual(len(response['surveys']), 1)


class BrowserTests(EuphorieFunctionalTestCase):
    def test_get(self):
        import json
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = Browser()
        browser.open('http://nohost/plone/client/api/surveys/nl/ict')
        response = json.loads(browser.contents)
        self.assertEqual(response['id'], 'ict')
