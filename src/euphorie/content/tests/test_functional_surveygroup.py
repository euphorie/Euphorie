from Acquisition import aq_parent
from euphorie.content.browser.surveygroup import AddForm
from euphorie.content.interfaces import SurveyUnpublishEvent
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
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

    def testOnlyOnePublishedSurvey(self):
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        survey2 = self._create(surveygroup, "euphorie.survey", "survey2")
        self.assertEqual(self.portal.client.keys(), [])
        api.content.transition(obj=survey, transition="publish")
        self.assertEqual(surveygroup.published, "survey")
        self.assertEqual(api.content.get_state(obj=survey), "published")
        self.assertEqual(api.content.get_state(obj=survey2), "draft")
        # The survey has been created on the client side with the id of the
        # surveygroup.
        self.assertEqual(self.portal.client["nl"]["sector"].keys(), ["group"])
        # Publish the second survey.
        api.content.transition(obj=survey2, transition="publish")
        self.assertEqual(surveygroup.published, "survey2")
        self.assertEqual(api.content.get_state(obj=survey), "draft")
        self.assertEqual(api.content.get_state(obj=survey2), "published")
        # The danger is that retracting the other survey deletes the survey on
        # the client side.  So check that this is still there.
        self.assertEqual(self.portal.client["nl"]["sector"].keys(), ["group"])
        # The SurveyUnpublishEvent removes the survey from the client side.
        # If we explicitly notify an unpublish event for the survey that is not
        # actually published, this should not remove the client side survey.
        # This is a check to avoid regressions.
        notify(SurveyUnpublishEvent(survey))
        self.assertEqual(self.portal.client["nl"]["sector"].keys(), ["group"])

    def test_20240731180000_retract_unpublished_surveys__wrong_draft(self):
        # Create a wrong situation: a survey group is marked as being the
        # client-side-published survey, but its own review state is 'draft'.
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        surveygroup.published = "survey"
        self.assertEqual(self.portal.client.keys(), [])

        # Get the upgrade step and execute it.
        # Easiest is to set the profile to the previous version.
        profile = "euphorie.deployment:default"
        dest = "20240731180000"
        setup = api.portal.get_tool(name="portal_setup")
        setup.setLastVersionForProfile(profile, "20240426095318")
        self.assertEqual(len(setup.listUpgrades(profile, dest=dest)), 1)
        setup.upgradeProfile(profile, dest=dest)

        # In this case we do not dare change anything, because we do not want
        # to touch anything on the client side, and especially not suddenly
        # create an entire client-side survey.
        self.assertEqual(api.content.get_state(obj=survey), "draft")
        self.assertEqual(self.portal.client.keys(), [])

    def test_20240731180000_retract_unpublished_surveys__wrong_published(self):
        # Start with a standard situation, with a published survey.
        surveygroup = self.createSurveyGroup()
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        api.content.transition(obj=survey, transition="publish")
        self.assertEqual(surveygroup.published, "survey")
        self.assertEqual(api.content.get_state(obj=survey), "published")
        self.assertEqual(self.portal.client["nl"]["sector"].keys(), ["group"])

        # Now turn it into a wrong situation, mimicking what may be the case in
        # real databases until now: unmark the survey as being the
        # client-side-published survey, but let its own review state remain
        # 'published'.
        surveygroup.published = None

        # Get the upgrade step and execute it.
        # Easiest is to set the profile to the previous version.
        profile = "euphorie.deployment:default"
        dest = "20240731180000"
        setup = api.portal.get_tool(name="portal_setup")
        setup.setLastVersionForProfile(profile, "20240426095318")
        self.assertEqual(len(setup.listUpgrades(profile, dest=dest)), 1)
        setup.upgradeProfile(profile, dest=dest)

        # In this case we want to survey to revert to draft, but we want to avoid
        # changing anything on the client side.
        self.assertEqual(api.content.get_state(obj=survey), "draft")
        self.assertEqual(self.portal.client["nl"]["sector"].keys(), ["group"])


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
