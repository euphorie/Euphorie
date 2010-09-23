import unittest
import Acquisition
from zope.interface import alsoProvides
from zope.component.testing import PlacelessSetup
from euphorie.content.survey import Survey
from euphorie.content.survey import View
from euphorie.content.profilequestion import IProfileQuestion

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
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)
        provideAdapter(ContextState, adapts=(Interface, Interface),
                       provides=Interface, name="plone_context_state")
        # grok makes unit testing extremely painful
        View.__view_name__ = "iew"
        View.module_info=Mock()
        View.module_info.package_dotted_name="euphorie.content.survey.View"

    def tearDown(self):
        super(ViewTests, self).tearDown()
        del View.__view_name__
        del View.module_info

    def _request(self):
        from zope.publisher.browser import TestRequest
        from zope.annotation.interfaces import IAttributeAnnotatable
        req=TestRequest() 
        alsoProvides(req, IAttributeAnnotatable)
        return req


    def testProfileQuestions_NoChildren(self):
        survey=Survey()
        view=View(survey, self._request())
        self.assertEqual(view.profile_questions(), [])


    def testProfileQuestions_ProfileChild(self):
        survey=Survey()
        view=View(survey, self._request())
        child=Mock(id="child", title=u"Child")
        alsoProvides(child, IProfileQuestion)
        survey["child"]=child

        pq=view.profile_questions()
        self.assertEqual(len(pq), 1)

    def testProfileQuestions_ReturnedData(self):
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
        survey=Survey()
        view=View(survey, self._request())
        child=Mock(id="child", title=u"Child")
        survey["child"]=child

        pq=view.profile_questions()
        self.assertEqual(len(pq), 0)

