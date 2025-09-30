from ftw.upgrade import UpgradeStep
from plone import api


class SetTheNewFieldEnableTestQuestions(UpgradeStep):
    """Set the new field enable_test_questions."""

    def __call__(self):
        """Upgrade step to set the new field enable_test_questions.

        If the web training is not enabled do not do anything.

        Otherwise check all the surveys that we have.
        If the survey web training is enabled and we have at least one
        training question in the survey, set the new field to True.
        """
        if not api.portal.get_registry_record(
            "euphorie.use_training_module", default=False
        ):
            return

        brains = api.content.find(portal_type="euphorie.survey")
        for brain in brains:
            survey = brain.getObject()
            if getattr(survey, "enable_web_training", True):
                if api.content.find(
                    context=survey, portal_type="euphorie.training_question"
                ):
                    survey.enable_test_questions = True
