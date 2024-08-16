from Products.CMFCore.utils import getToolByName


def handleSurveyPublish(survey, event):
    """Event handler (subscriber) for successfull workflow transitions for
    :py:obj:`ISurvey` objects. This handler archives the current version.
    """
    if event.action not in ["publish", "update"]:
        return

    repository = getToolByName(survey, "portal_repository")
    repository.save(survey, "Survey published")
