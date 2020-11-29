# coding=utf-8
from ..module import IModule
from ..profilequestion import IProfileQuestion
from ..survey import ISurvey
from ..survey import ISurveyAddSchema
from ..utils import DragDropHelper
from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.event import ObjectClonedEvent
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.appconfig.interfaces import IAppConfig
from ZODB.POSException import ConflictError
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.container.interfaces import INameChooser
from zope.event import notify


class SurveyView(BrowserView, DragDropHelper):
    def _morph(self, child):
        state = getMultiAdapter((child, self.request), name="plone_context_state")
        return {"id": child.id, "title": child.title, "url": state.view_url()}

    @property
    def children(self):
        return [
            self._morph(child)
            for child in self.context.values()
            if IModule.providedBy(child) or IProfileQuestion.providedBy(child)
        ]

    @property
    def group(self):
        return aq_parent(aq_inner(self.context))


class AddForm(DefaultAddForm):
    """Custom add form for :obj:`Survey` instances. This form is
    needlessly complicated: it should use a schema and a vocabulary
    to offer a list of template surveys, but this is impossible since
    vocabulary factories always get a None context. See
    http://code.google.com/p/dexterity/issues/detail?id=125
    """

    portal_type = "euphorie.survey"
    schema = ISurveyAddSchema
    template = ViewPageTemplateFile("templates/survey_add.pt")

    def surveys(self):
        templates = [
            {"id": survey.id, "title": survey.title}
            for survey in self.context.values()
            if ISurvey.providedBy(survey)
        ]
        return templates

    def copyTemplate(self, source, title):
        target = aq_inner(self.context)
        try:
            source._notifyOfCopyTo(target, op=0)
        except ConflictError:
            raise

        copy = source._getCopy(target)
        copy.title = title
        chooser = INameChooser(target)
        copy.id = chooser.chooseName(None, copy)
        target._setObject(copy.id, copy)

        copy = target[copy.id]  # Acquisition-wrap
        copy.wl_clearLocks()
        copy._postCopy(target, op=0)
        notify(ObjectClonedEvent(target[copy.id]))
        return copy

    def createAndAdd(self, data):
        surveygroup = aq_inner(self.context)
        template = surveygroup[self.request.form["survey"]]
        survey = self.copyTemplate(template, data["title"])
        self.immediate_view = survey.absolute_url()
        return survey


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    def applyChanges(self, data):
        changes = super(EditForm, self).applyChanges(data)
        if changes:
            # Reindex our parents title.
            catalog = getToolByName(self.context, "portal_catalog")
            catalog.indexObject(aq_parent(aq_inner(self.context)))
        return changes

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get("euphorie")
        if not settings.get("use_integrated_action_plan", False):
            self.widgets["integrated_action_plan"].mode = "hidden"
