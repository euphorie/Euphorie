# coding=utf-8
from Acquisition import aq_parent
from euphorie.content.surveygroup import AddForm
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.folder.interfaces import IExplicitOrdering
from Products.CMFCore.WorkflowCore import ActionSucceededEvent
from zope import component
from zope.event import notify


class SurveyGroupTests(EuphorieIntegrationTestCase):

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSurveyGroup(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        return surveygroup

    def testNoWorkflow(self):
        surveygroup = self.createSurveyGroup()
        pw = api.portal.get_tool('portal_workflow')
        chain = pw.getChainFor(surveygroup)
        self.assertEqual(chain, ())

    def testNotGloballyAllowed(self):
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.survey" not in types)

    def testAllowedContentTypes(self):
        surveygroup = self.createSurveyGroup()
        types = [fti.id for fti in surveygroup.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.survey"]))

    def testCanNotBeCopied(self):
        surveygroup = self.createSurveyGroup()
        self.assertFalse(surveygroup.cb_isCopyable())


class HandleSurveyPublishTests(EuphorieIntegrationTestCase):

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSurveyGroup(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        return surveygroup

    def testNothingPublished(self):
        surveygroup = self.createSurveyGroup()
        self.assertEqual(surveygroup.published, None)

    def testUnknownWorkflowAction(self):
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        notify(ActionSucceededEvent(survey, None, "bogus", None))
        self.assertEqual(surveygroup.published, None)

    def testPublishAction(self):
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        notify(ActionSucceededEvent(survey, None, "publish", None))
        self.assertEqual(surveygroup.published, "survey")

    def testUpdateAction(self):
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        notify(ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(surveygroup.published, "survey")

    def testUnpublishAction(self):
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        notify(ActionSucceededEvent(survey, None, "publish", None))
        self.assertEqual(surveygroup.published, "survey")
        request = survey.REQUEST
        unpublishview = component.getMultiAdapter((surveygroup, request),
                                                  name='unpublish')
        unpublishview.unpublish()
        self.assertEqual(surveygroup.published, None)


class HandleSurveyDeleteVerificationTests(EuphorieIntegrationTestCase):

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSurveyGroup(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        return surveygroup

    def testDeleteOneOfManySurvey(self):
        """ It should be possible to delete one of many surveys, when it's not
            published.
        """
        surveygroup = self.createSurveyGroup()
        self._create(surveygroup, "euphorie.survey", "dummy")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        self.assertEqual(surveygroup.published, None)
        deleteaction = component.getMultiAdapter((survey, survey.REQUEST),
                                                 name='delete')
        self.assertEqual(deleteaction.verify(surveygroup, survey), True)

    def testDeleteOnlySurvey(self):
        """ Validation should fail when trying to delete the only survey in a
            surveygroup
        """
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        deleteaction = component.getMultiAdapter((survey, survey.REQUEST),
                                                 name='delete')
        self.assertEqual(deleteaction.verify(surveygroup, survey), False)

    def testDeletePublishedSurvey(self):
        """ Validation should fail when trying to delete a published survey
        """
        surveygroup = self.createSurveyGroup()
        self._create(surveygroup, "euphorie.survey", "dummy")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        notify(ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(surveygroup.published, "survey")
        deleteaction = component.getMultiAdapter((survey, survey.REQUEST),
                                                 name='delete')
        self.assertEqual(deleteaction.verify(surveygroup, survey), False)

    def testDeleteUnPublishedSurvey(self):
        """ It should be possible to delete unpublished surveys
        """
        surveygroup = self.createSurveyGroup()
        self._create(surveygroup, "euphorie.survey", "dummy")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        deleteaction = component.getMultiAdapter((survey, survey.REQUEST),
                                                 name='delete')
        notify(ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(surveygroup.published, "survey")
        unpublishview = component.getMultiAdapter(
            (surveygroup, survey.REQUEST), name='unpublish'
        )
        unpublishview.unpublish()

        self.assertEqual(surveygroup.published, None)
        self.assertEqual(deleteaction.verify(surveygroup, survey), True)


class AddFormTests(EuphorieFunctionalTestCase):

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        module = self._create(survey, "euphorie.module", "module")
        return module

    def testCopyPreservesOrder(self):
        original_order = [
            u"one", u"two", u"three", u"four", u"five", u"six", u"seven",
            u"eight", u"nine", u"ten"
        ]
        module = self.createModule()
        for title in original_order:
            self._create(module, "euphorie.risk", title, title=title)
        self.assertEqual([r.title for r in module.values()], original_order)
        request = module.REQUEST
        survey = aq_parent(module)
        container = self.portal.sectors.nl.sector
        target = self._create(container, "euphorie.surveygroup", "target")
        copy = AddForm(container, request).copyTemplate(survey, target)
        self.assertEqual([r.title for r in copy["module"].values()],
                         original_order)

    def testReorderThenCopyTemplateKeepsOrder(self):
        original_order = [
            u"one", u"two", u"three", u"four", u"five", u"six", u"seven",
            u"eight", u"nine", u"ten"
        ]
        sorted_order = list(sorted(original_order))
        module = self.createModule()
        for title in original_order:
            self._create(module, "euphorie.risk", title, title=title)
        self.assertEqual([r.title for r in module.values()], original_order)
        ordering = IExplicitOrdering(module)
        ordering.orderObjects("title")
        self.assertEqual([r.title for r in module.values()], sorted_order)
        request = module.REQUEST
        survey = aq_parent(module)
        container = self.portal.sectors.nl.sector
        target = self._create(container, "euphorie.surveygroup", "target")
        copy = AddForm(container, request).copyTemplate(survey, target)
        self.assertEqual([r.title for r in copy["module"].values()],
                         sorted_order)

    def testCopyClearsPublishFlag(self):
        survey = aq_parent(self.createModule())
        survey.published = True
        request = survey.REQUEST
        container = self.portal.sectors.nl.sector
        target = self._create(container, "euphorie.surveygroup", "target")
        copy = AddForm(container, request).copyTemplate(survey, target)
        self.assertFalse(getattr(copy, "published", False))

    def testCopyResetsWorkflow(self):
        survey = aq_parent(self.createModule())
        survey.published = True
        request = survey.REQUEST
        container = self.portal.sectors.nl.sector
        target = self._create(container, "euphorie.surveygroup", "target")
        copy = AddForm(container, request).copyTemplate(survey, target)
        self.assertEqual(
            self.portal.portal_workflow.getInfoFor(copy, "review_state"),
            "draft"
        )

    def testCopyEvaluationAlgorithmFromGroup(self):
        survey = aq_parent(self.createModule())
        survey.aq_parent.evaluation_algorithm = u"french"
        request = survey.REQUEST
        container = self.portal.sectors.nl.sector
        target = self._create(
            container,
            "euphorie.surveygroup",
            "target",
            evaluation_algorithm=u"kinney"
        )
        AddForm(container, request).copyTemplate(survey, target)
        self.assertEqual(target.evaluation_algorithm, u"french")
