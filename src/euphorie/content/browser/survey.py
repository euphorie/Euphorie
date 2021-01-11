# coding=utf-8
from ..module import IModule
from ..profilequestion import IProfileQuestion
from ..survey import ISurvey
from ..survey import ISurveyAddSchema
from ..utils import DragDropHelper
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.content import MessageFactory as _
from OFS.event import ObjectClonedEvent
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plonetheme.nuplone.skin import actions
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError
from zope.component import getMultiAdapter
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
        if not api.portal.get_registry_record(
            "euphorie.use_integrated_action_plan", default=False
        ):
            self.widgets["integrated_action_plan"].mode = "hidden"


class Delete(actions.Delete):
    """Special delete action class which prevents deletion of published surveys
    or of the last survey in a group.
    """

    def verify(self, container, context):
        flash = IStatusMessage(self.request).addStatusMessage

        if (
            hasattr(aq_base(container), "published")
            and container.published == context.id
        ):
            flash(
                _(
                    "message_no_delete_published_survey",
                    default=u"You cannot delete an OiRA Tool version that is "
                    u"published. Please unpublish it first.",
                ),
                "error",
            )
            self.request.response.redirect(context.absolute_url())
            return False

        count = 0
        for survey in container.values():
            if ISurvey.providedBy(survey):
                count += 1

        if count > 1:
            return True
        else:
            flash(
                _(
                    "message_delete_no_last_survey",
                    default=u"This is the only version of the OiRA Tool and can "
                    u"therefore not be deleted. Did you perhaps want to "
                    u"remove the OiRA Tool itself?",
                ),
                "error",
            )
            self.request.response.redirect(context.absolute_url())
            return False
