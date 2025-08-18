from Acquisition import aq_parent
from euphorie.content.browser.surveygroup import AddForm
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.base.utils import unrestricted_construct_instance
from plone.folder.interfaces import IExplicitOrdering
from Products.CMFCore.WorkflowCore import ActionSucceededEvent
from zope import component
from zope.event import notify


class SurveyGroupTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.client = self.portal.client
        self.loginAsPortalOwner()

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
        pw = api.portal.get_tool("portal_workflow")
        chain = pw.getChainFor(surveygroup)
        self.assertEqual(chain, ())

    def testNotGloballyAllowed(self):
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.assertTrue("euphorie.survey" not in types)

    def testAllowedContentTypes(self):
        surveygroup = self.createSurveyGroup()
        types = [fti.id for fti in surveygroup.allowedContentTypes()]
        self.assertEqual(set(types), {"euphorie.survey"})

    def testCanNotBeCopied(self):
        surveygroup = self.createSurveyGroup()
        self.assertFalse(surveygroup.cb_isCopyable())


class HandleSurveyPublishTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.client = self.portal.client
        self.loginAsPortalOwner()

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
        unpublishview = component.getMultiAdapter(
            (surveygroup, request), name="unpublish"
        )
        unpublishview.unpublish()
        self.assertEqual(surveygroup.published, None)

    def testUndeletableSurveys(self):
        surveygroup = self.createSurveyGroup()
        one = self._create(surveygroup, "euphorie.survey", "one")

        # If you have just one survey, it cannot be deleted
        with self.assertRaises(ValueError):
            api.content.delete(one)

        # A survey group should only contain surveys, but theoretically there
        # could be other content.  You still cannot delete the only survey
        unrestricted_construct_instance("Image", surveygroup, "pretty")
        with self.assertRaises(ValueError):
            api.content.delete(one)

        two = self._create(surveygroup, "euphorie.survey", "two")
        # Unpublished surveys can be deleted
        api.content.delete(two)

        # Published surveys cannot be deleted
        three = self._create(surveygroup, "euphorie.survey", "three")
        notify(ActionSucceededEvent(three, None, "update", None))
        with self.assertRaises(ValueError):
            api.content.delete(three)


class HandleSurveyDeleteVerificationTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.client = self.portal.client
        self.loginAsPortalOwner()

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSurveyGroup(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        return surveygroup

    def testDeleteOneOfManySurvey(self):
        """It should be possible to delete one of many surveys, when it's not
        published."""
        surveygroup = self.createSurveyGroup()
        self._create(surveygroup, "euphorie.survey", "dummy")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        self.assertEqual(surveygroup.published, None)
        deleteaction = component.getMultiAdapter(
            (survey, survey.REQUEST), name="delete"
        )
        self.assertEqual(deleteaction.verify(surveygroup, survey), True)

    def testDeleteOnlySurvey(self):
        """Validation should fail when trying to delete the only survey in a
        surveygroup."""
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        deleteaction = component.getMultiAdapter(
            (survey, survey.REQUEST), name="delete"
        )
        self.assertEqual(deleteaction.verify(surveygroup, survey), False)

    def testDeletePublishedSurvey(self):
        """Validation should fail when trying to delete a published survey."""
        surveygroup = self.createSurveyGroup()
        self._create(surveygroup, "euphorie.survey", "dummy")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        notify(ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(surveygroup.published, "survey")
        deleteaction = component.getMultiAdapter(
            (survey, survey.REQUEST), name="delete"
        )
        self.assertEqual(deleteaction.verify(surveygroup, survey), False)

    def testDeleteUnPublishedSurvey(self):
        """It should be possible to delete unpublished surveys."""
        surveygroup = self.createSurveyGroup()
        self._create(surveygroup, "euphorie.survey", "dummy")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        deleteaction = component.getMultiAdapter(
            (survey, survey.REQUEST), name="delete"
        )
        notify(ActionSucceededEvent(survey, None, "update", None))
        self.assertEqual(surveygroup.published, "survey")
        unpublishview = component.getMultiAdapter(
            (surveygroup, survey.REQUEST), name="unpublish"
        )
        unpublishview.unpublish()

        self.assertEqual(surveygroup.published, None)
        self.assertEqual(deleteaction.verify(surveygroup, survey), True)


class AddFormTests(EuphorieFunctionalTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.client = self.portal.client
        self.loginAsPortalOwner()

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

    def testCopyResetsUIDs(self):
        module = self.createModule()
        self._create(module, "euphorie.risk", "one", title="one")
        request = module.REQUEST
        survey = aq_parent(module)
        container = self.portal.sectors.nl.sector
        target = self._create(container, "euphorie.surveygroup", "target")
        copy = AddForm(container, request).copyTemplate(survey, target)
        self.assertNotEqual(survey.UID(), copy.UID())
        self.assertNotEqual(survey.module.UID(), copy.module.UID())
        self.assertNotEqual(survey.module.one.UID(), copy.module.one.UID())

    def testCopyPreservesOrder(self):
        original_order = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
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
        self.assertEqual([r.title for r in copy["module"].values()], original_order)

    def testReorderThenCopyTemplateKeepsOrder(self):
        original_order = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
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
        self.assertEqual([r.title for r in copy["module"].values()], sorted_order)

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
            self.portal.portal_workflow.getInfoFor(copy, "review_state"), "draft"
        )

    def testCopyEvaluationAlgorithmFromGroup(self):
        survey = aq_parent(self.createModule())
        survey.aq_parent.evaluation_algorithm = "french"
        request = survey.REQUEST
        container = self.portal.sectors.nl.sector
        target = self._create(
            container, "euphorie.surveygroup", "target", evaluation_algorithm="kinney"
        )
        AddForm(container, request).copyTemplate(survey, target)
        self.assertEqual(target.evaluation_algorithm, "french")
