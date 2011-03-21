import unittest
import Acquisition
from zope.component.testing import PlacelessSetup

class Mock(Acquisition.Explicit):
    def __init__(self, **kwargs):
        for (key,value) in kwargs.items():
            setattr(self, key, value)

    def absolute_url(self):
        return "http://nohost/%s" % self.id

    def manage_fixupOwnershipAfterAdd(self):
        pass


class ViewTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        super(ViewTests, self).setUp()
        from zope.component import provideAdapter
        from zope.annotation.attribute import AttributeAnnotations
        from plone.folder.default import DefaultOrdering
        from plone.app.layout.globals.context import ContextState
        from zope.interface import Interface
        from euphorie.content.survey import View
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)
        provideAdapter(ContextState, adapts=(Interface, Interface),
                       provides=Interface, name="plone_context_state")
        # grok makes unit testing extremely painful
        View.__view_name__ = "iew"
        View.module_info=Mock()
        View.module_info.package_dotted_name="euphorie.content.survey.View"

    def tearDown(self):
        from euphorie.content.survey import View
        super(ViewTests, self).tearDown()
        del View.__view_name__
        del View.module_info

    def _request(self):
        from zope.interface import alsoProvides
        from zope.publisher.browser import TestRequest
        from zope.annotation.interfaces import IAttributeAnnotatable
        req=TestRequest() 
        alsoProvides(req, IAttributeAnnotatable)
        return req


    def testProfileQuestions_NoChildren(self):
        from euphorie.content.survey import Survey
        from euphorie.content.survey import View
        survey=Survey()
        view=View(survey, self._request())
        self.assertEqual(view.profile_questions(), [])


    def testProfileQuestions_ProfileChild(self):
        from zope.interface import alsoProvides
        from euphorie.content.survey import Survey
        from euphorie.content.profilequestion import IProfileQuestion
        from euphorie.content.survey import View
        survey=Survey()
        view=View(survey, self._request())
        child=Mock(id="child", title=u"Child")
        alsoProvides(child, IProfileQuestion)
        survey["child"]=child

        pq=view.profile_questions()
        self.assertEqual(len(pq), 1)

    def testProfileQuestions_ReturnedData(self):
        from zope.interface import alsoProvides
        from euphorie.content.survey import Survey
        from euphorie.content.profilequestion import IProfileQuestion
        from euphorie.content.survey import View
        survey=Survey()
        view=View(survey, self._request())
        child=Mock(id="child", title=u"Child")
        alsoProvides(child, IProfileQuestion)
        survey["child"]=child

        pq=view.profile_questions()
        self.assertEqual(pq[0], dict(id="child",
                                     title=u"Child",
                                     url="http://nohost/child"))


    def testProfileQuestions_OtherChild(self):
        from euphorie.content.survey import Survey
        from euphorie.content.survey import View
        survey=Survey()
        view=View(survey, self._request())
        child=Mock(id="child", title=u"Child")
        survey["child"]=child

        pq=view.profile_questions()
        self.assertEqual(len(pq), 0)



class HandleSurveyUnpublishTests(unittest.TestCase):
    def handleSurveyUnpublish(self, *a, **kw):
        from euphorie.content.survey import handleSurveyUnpublish
        return handleSurveyUnpublish(*a, **kw)

    def testRemovePublishedFromSurvey(self):
        surveygroup=Mock(published=None)
        surveygroup.survey=Mock(id="survey", published="yes")
        self.handleSurveyUnpublish(surveygroup.survey, None)
        self.assertTrue(not hasattr(surveygroup.survey, "published"))

    def testUpdatateSurveygroupIfCurrentlyPublished(self):
        surveygroup=Mock(published="survey")
        surveygroup.survey=Mock(id="survey", published="yes")
        self.handleSurveyUnpublish(surveygroup.survey, None)
        self.assertEqual(surveygroup.published, None)

    def testUpdatateSurveygroupIfOtherPublished(self):
        surveygroup=Mock(published="other")
        surveygroup.survey=Mock(id="survey", published="yes")
        self.handleSurveyUnpublish(surveygroup.survey, None)
        self.assertEqual(surveygroup.published, "other")

