from ftw.upgrade import UpgradeStep
from plone import api

import logging


logger = logging.getLogger(__name__)


class RetractUnpublishedSurveys(UpgradeStep):
    """Retract unpublished surveys.

    Each surveygroup has an attribute 'published'.
    This contains the id of a contained survey that is actually published
    on the client side.
    The review state of the contained surveys should match:

    * The survey with this id must be in the 'published' state.
    * All other surveys must be in the 'draft' state.

    This upgrade step wants to make sure this is the case.

    We should watch out though: I don't think it is a good idea to let this
    upgrade step add/update/remove items on the client side.  This means we
    must not publish any survey, but only retract surveys where needed.

    So if a supposedly published survey does not have the published state,
    we only print a warning.
    """

    def __call__(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        for brain in catalog.unrestrictedSearchResults(
            portal_type="euphorie.surveygroup"
        ):
            try:
                surveygroup = brain.getObject()
            except Exception:
                logger.warning("Cannot get object for brain at %s", brain.getPath())
                continue
            published_id = surveygroup.published
            for content in surveygroup.contentValues():
                if content.portal_type != "euphorie.survey":
                    continue
                old_state = api.content.get_state(obj=content)
                if content.id == published_id:
                    if old_state != "published":
                        logger.warning(
                            "Survey is marked as the published tool version for its "
                            "surveygroup, but its review state is %r. You should "
                            "investigate: %s",
                            old_state,
                            brain.getPath(),
                        )
                    continue
                if old_state == "published":
                    logger.warning(
                        "Survey has state 'published', but is not marked as the "
                        "published tool version for its surveygroup. Reverting it "
                        "to 'draft' state: %s",
                        brain.getPath(),
                    )
                    api.content.transition(obj=content, to_state="draft")
