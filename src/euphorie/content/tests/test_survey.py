from ..browser.survey import SurveyView
from euphorie.content.module import IModule
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.survey import handleSurveyUnpublish
from euphorie.content.survey import Survey
from euphorie.testing import EuphorieIntegrationTestCase
from unittest import mock
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest

import Acquisition
import unittest


class Mock(Acquisition.Explicit):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def absolute_url(self):
        return "http://nohost/%s" % self.id

    def manage_fixupOwnershipAfterAdd(self):
        pass


class ViewTests(EuphorieIntegrationTestCase):
    def _request(self):
        req = TestRequest()
        alsoProvides(req, IAttributeAnnotatable)
        return req

    def test_update_no_children(self):
        survey = Survey()
        view = SurveyView(survey, self._request())
        self.assertEqual(view.modules_and_profile_questions, [])

    def test_update_with_profile(self):
        survey = Survey()
        child = Mock(id="child", title="Child")
        alsoProvides(child, IProfileQuestion)
        survey._setObject("child", child, suppress_events=True)
        view = SurveyView(survey, self._request())
        view._morph = mock.Mock(return_value="info")
        self.assertEqual(view.modules_and_profile_questions, ["info"])

    def test_update_with_module(self):
        survey = Survey()
        child = Mock(id="child", title="Child")
        alsoProvides(child, IModule)
        survey._setObject("child", child, suppress_events=True)
        view = SurveyView(survey, self._request())
        view._morph = mock.Mock(return_value="info")
        self.assertEqual(view.modules_and_profile_questions, ["info"])

    def test_update_other_child(self):
        survey = Survey()
        view = SurveyView(survey, self._request())
        child = Mock(id="child", title="Child")
        survey._setObject("child", child, suppress_events=True)
        self.assertEqual(view.modules_and_profile_questions, [])

    def test_moprh(self):
        child = Mock(id="child", title="Child")
        view = SurveyView(None, self._request())
        self.assertEqual(
            view._morph(child),
            {
                "id": "child",
                "title": "Child",
                "url": "http://nohost/child",
                "is_profile_question": False,
            },
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
