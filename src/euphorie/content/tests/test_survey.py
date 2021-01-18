# coding=utf-8
from ..browser.survey import SurveyView
from euphorie.content.module import IModule
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.survey import handleSurveyUnpublish
from euphorie.content.survey import Survey
from euphorie.testing import EuphorieIntegrationTestCase
from plone.app.layout.globals.context import ContextState
from plone.folder.default import DefaultOrdering
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import provideAdapter
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.publisher.browser import TestRequest

import Acquisition
import unittest


try:
    from unittest import mock
except ImportError:
    import mock


class Mock(Acquisition.Explicit):
    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def absolute_url(self):
        return "http://nohost/%s" % self.id

    def manage_fixupOwnershipAfterAdd(self):
        pass


class ViewTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super(ViewTests, self).setUp()
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)
        provideAdapter(
            ContextState,
            adapts=(Interface, Interface),
            provides=Interface,
            name="plone_context_state",
        )
        SurveyView.__view_name__ = "View"
        SurveyView.module_info = Mock()
        SurveyView.module_info.package_dotted_name = (
            "euphorie.content.browser.survey.SurveyView"
        )

    def tearDown(self):
        super(ViewTests, self).tearDown()
        del SurveyView.__view_name__
        del SurveyView.module_info

    def _request(self):
        req = TestRequest()
        alsoProvides(req, IAttributeAnnotatable)
        return req

    def test_update_no_children(self):
        survey = Survey()
        view = SurveyView(survey, self._request())
        self.assertEqual(view.children, [])

    def test_update_with_profile(self):
        survey = Survey()
        child = Mock(id="child", title=u"Child")
        alsoProvides(child, IProfileQuestion)
        survey._setObject("child", child, suppress_events=True)
        view = SurveyView(survey, self._request())
        view._morph = mock.Mock(return_value="info")
        self.assertEqual(view.children, ["info"])

    def test_update_with_module(self):
        survey = Survey()
        child = Mock(id="child", title=u"Child")
        alsoProvides(child, IModule)
        survey._setObject("child", child, suppress_events=True)
        view = SurveyView(survey, self._request())
        view._morph = mock.Mock(return_value="info")
        self.assertEqual(view.children, ["info"])

    def test_update_other_child(self):
        survey = Survey()
        view = SurveyView(survey, self._request())
        child = Mock(id="child", title=u"Child")
        survey._setObject("child", child, suppress_events=True)
        self.assertEqual(view.children, [])

    def test_moprh(self):
        child = Mock(id="child", title=u"Child")
        view = SurveyView(None, self._request())
        self.assertEqual(
            view._morph(child),
            {"id": "child", "title": u"Child", "url": "http://nohost/child"},
        )


class HandleSurveyUnpublishTests(unittest.TestCase):
    def handleSurveyUnpublish(self, *a, **kw):
        return handleSurveyUnpublish(*a, **kw)

    def testRemovePublishedFromSurvey(self):
        surveygroup = Mock(published=None)
        surveygroup.survey = Mock(id="survey", published="yes")
        self.handleSurveyUnpublish(surveygroup.survey, None)
        self.assertTrue(not hasattr(surveygroup.survey, "published"))

    def testUpdatateSurveygroupIfCurrentlyPublished(self):
        surveygroup = Mock(published="survey")
        surveygroup.survey = Mock(id="survey", published="yes")
        self.handleSurveyUnpublish(surveygroup.survey, None)
        self.assertEqual(surveygroup.published, None)

    def testUpdatateSurveygroupIfOtherPublished(self):
        surveygroup = Mock(published="other")
        surveygroup.survey = Mock(id="survey", published="yes")
        self.handleSurveyUnpublish(surveygroup.survey, None)
        self.assertEqual(surveygroup.published, "other")
