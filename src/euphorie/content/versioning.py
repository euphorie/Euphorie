from euphorie.content.survey import ISurvey
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName


@grok.subscribe(ISurvey, IActionSucceededEvent)
def handleSurveyPublish(survey, event):
    """Event handler (subscriber) for succesfull workflow transitions for
    :py:obj:`ISurvey` objects. This handler archives the current version.
    """
    if event.action not in ["publish", "update"]:
        return

    repository = getToolByName(survey, "portal_repository")
    repository.save(survey, "Survey published")
