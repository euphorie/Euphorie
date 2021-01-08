# coding=utf-8
"""
Survey
======

A survey holds the entire risk assessment survey. The survey is a hierarchical
structure containing modules, profile questions and questions. Both modules and
profile questions are used to create the hierarchy.
"""

from .. import MessageFactory as _
from .behaviour.uniqueid import get_next_id
from .behaviour.uniqueid import INameFromUniqueId
from .datamanager import ParentAttributeField
from .fti import check_fti_paste_allowed
from .interfaces import IQuestionContainer
from .interfaces import ISurveyUnpublishEvent
from .module import IModule
from .profilequestion import IProfileQuestion
from .utils import DragDropHelper
from .utils import StripMarkup
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.content.dependency import ConditionalHtmlText
from euphorie.content.dependency import ConditionalTextLine
from euphorie.content.utils import get_tool_type_default
from euphorie.content.utils import IToolTypesInfo
from five import grok
from htmllaundry.z3cform import HtmlText
from OFS.event import ObjectClonedEvent
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.dexterity.content import Container
from plone.directives import dexterity
from plone.directives import form
from plone.indexer import indexer
from plonetheme.nuplone.skin import actions
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.directives import depends
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from ZODB.POSException import ConflictError
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.container.interfaces import INameChooser
from zope.event import notify
from zope.interface import implements

import sys


grok.templatedir("templates")


class ISurvey(form.Schema, IBasic):
    """Survey.

    The survey is the root of a survey.
    """

    title = schema.TextLine(
        title=_("label_survey_title", default=u"Version name"),
        description=_(
            "help_survey_title",
            default=u"This is the title of this OiRA Tool version. This "
            u"name is never shown to users.",
        ),
        required=True,
    )
    form.order_before(title="*")

    form.omitted("description")

    introduction = HtmlText(
        title=_("label_introduction", default=u"Introduction text"),
        description=_(
            u"The introduction text is shown when starting a new "
            u"OiRA Tool session. If no introduction is provided here a "
            u"standard text will be shown. Please keep this text brief "
            u"so it will easily fit on screens of small devices such as "
            u"phones and PDAs."
        ),
        required=False,
    )
    form.widget(introduction=WysiwygFieldWidget)

    evaluation_optional = schema.Bool(
        title=_("label_evaluation_optional", default=u"Evaluation may be skipped"),
        description=_(
            "help_evaluation_optional",
            default=u"This option allows users to skip the evaluation " u"phase.",
        ),
        default=False,
        required=False,
    )

    language = schema.Choice(
        title=_("label_language", default=u"Language"),
        vocabulary="plone.app.vocabularies.AvailableContentLanguages",
        default=u"en",
        required=True,
    )

    classification_code = schema.TextLine(
        title=_("label_classification_code", default=u"Classification code"),
        description=_(
            "help_classification_code",
            default=u"A code identifying this sector. Classification "
            u"codes are defined by national standards bodies "
            u"and based on revision 2 of the NACE standard.",
        ),
        required=False,
    )

    tool_type = schema.Choice(
        title=_("label_tool_type", default=u"Type of OiRA Tool"),
        description=_(
            "description_tool_type",
            default=u"This selection determines, which variant of an OiRA Tool"
            u' will be created. If you are not sure, select "Classic".',
        ),
        vocabulary="euphorie.tool_types_vocabulary",
        defaultFactory=get_tool_type_default,
        required=True,
    )

    measures_text_handling = schema.Choice(
        title=_(
            "measures_text_handling",
            default=u"Handling of measures text (if measures-in-place are used)",
        ),
        description=_(
            "description_measures_text_handling",
            default=(
                u"Defines how the “Measures in place” options are displayed "
                u"to the user. "
                u"Choose “Simple” if the texts for Description and General Approach "
                u"are identical in your measures. "
                u"Choose “Full” if the texts in General Approach "
                u"provide more details than the Description."
            ),
        ),
        vocabulary="euphorie.measures_text_handling_vocabulary",
        default="full",
        required=True,
    )

    integrated_action_plan = schema.Bool(
        title=_("label_integrated_action_plan", default=u"Integrated Action Plan"),
        description=_(
            "description_integrated_action_plan",
            default=u"If selected, the option to plan measures will be offered "
            u"directly on the “Identification” page. There will be no separate "
            u"“Action Plan” step in the navigation.",
        ),
        required=False,
        default=False,
    )

    enable_tool_notification = schema.Bool(
        title=_(
            "label_enable_tool_notification",
            default=u"Show a custom notification for this OiRA tool?",
        ),
        description=_(
            u"description_tool_notification",
            default=u"If you enter text here, it will be shown to users "
            u"in a pop-up when they open the tool. It can be used for "
            u"notifying users about changes.",
        ),
        required=False,
        default=False,
    )

    depends("tool_notification_title", "enable_tool_notification", "on")
    tool_notification_title = ConditionalTextLine(
        title=_("label_tool_notification_title", default=u"Tool notification title"),
        required=True,
    )

    depends("tool_notification_message", "enable_tool_notification", "on")
    tool_notification_message = ConditionalHtmlText(
        title=_("label_tool_notification", default=u"Tool notification message"),
        required=True,
    )
    form.widget(tool_notification_message=WysiwygFieldWidget)


class SurveyAttributeField(ParentAttributeField):
    parent_mapping = {
        "survey_title": "title",
        "obsolete": "obsolete",
    }


def get_tool_type(context):
    """Return the tool type used in a given context. The type is set on
    the survey.
    """
    from euphorie.content.survey import ISurvey  # XXX Circular

    tt_default = get_tool_type_default()
    for parent in aq_chain(aq_inner(context)):
        if ISurvey.providedBy(parent):
            return getattr(parent, "tool_type", "") or tt_default
    return tt_default


class Survey(Container):
    """A risk assessment survey.

    A survey uses the *IIdGenerationRoot* behaviour to guarantee that
    all items inside the survey have a unique id.
    """

    grok.name("euphorie.container")

    implements(ISurvey, IQuestionContainer)

    dirty = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return op

    def _get_id(self, orig_id):
        """Pick an id for pasted content."""
        frame = sys._getframe(1)
        ob = frame.f_locals.get("ob")
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super(Survey, self)._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super(Survey, self)._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)

    def hasProfile(self):
        """Check if this survey has any profile questions.

        .. todo::
           Implement the deprecation checking
        """

        for child in self.values():
            if IProfileQuestion.providedBy(child):
                return True
        else:
            return False

    def hasNotification(self):
        """
        Checks if a notification message was set
        """
        return self.enable_tool_notification or False

    def ProfileQuestions(self):
        """Return a list of all profile questions."""
        return [child for child in self.values() if IProfileQuestion.providedBy(child)]

    def get_tool_type_name(self):
        """ Returns the human readable name of the chosen tool type """
        my_tool_type = get_tool_type(self)
        tti = getUtility(IToolTypesInfo)
        tool_types = tti()
        if my_tool_type not in tool_types:
            my_tool_type = tti.default_tool_type
        return tool_types[my_tool_type]["title"]


@indexer(ISurvey)
def SearchableTextIndexer(obj):
    return " ".join(
        [
            obj.title,
            StripMarkup(obj.description),
            StripMarkup(obj.introduction),
            obj.classification_code or u"",
        ]
    )


class View(grok.View, DragDropHelper):
    grok.context(ISurvey)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("survey_view")
    grok.name("nuplone-view")

    def _morph(self, child):
        state = getMultiAdapter((child, self.request), name="plone_context_state")
        return {"id": child.id, "title": child.title, "url": state.view_url()}

    def update(self):
        self.children = [
            self._morph(child)
            for child in self.context.values()
            if IModule.providedBy(child) or IProfileQuestion.providedBy(child)
        ]
        self.group = aq_parent(aq_inner(self.context))
        super(View, self).update()


class ISurveyAddSchema(form.Schema):
    title = schema.TextLine(
        title=_("label_survey_title", default=u"Version name"),
        description=_(
            "help_survey_title",
            default=u"This is the title of this OiRA Tool version. This "
            u"name is never shown to users.",
        ),
        required=True,
    )


class ISurveyEditSchema(ISurvey):
    survey_title = schema.TextLine(
        title=_("label_title", default=u"Title"),
        description=_(
            "help_surveygroup_title",
            default=u"The title of this OiRA Tool. This title is used in "
            u"the OiRA Tool overview in the clients.",
        ),
        required=True,
    )
    form.order_before(survey_title="*")

    obsolete = schema.Bool(
        title=_("label_survey_obsolete", default=u"Obsolete OiRA tool"),
        description=_(
            "help_survey_obsolete",
            default=u"This OiRA Tool is obsolete; it has been retired or "
            u"replaced with another OiRA Tool.",
        ),
        default=False,
        required=False,
    )
    form.order_before(obsolete="introduction")


class AddForm(dexterity.AddForm):
    """Custom add form for :obj:`Survey` instances. This form is
    needlessly complicated: it should use a schema and a vocabulary
    to offer a list of template surveys, but this is impossible since
    vocabulary factories always get a None context. See
    http://code.google.com/p/dexterity/issues/detail?id=125
    """

    grok.context(ISurvey)
    grok.name("euphorie.survey")
    grok.require("euphorie.content.AddNewRIEContent")

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


class Edit(form.SchemaEditForm):
    grok.context(ISurvey)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("edit")

    schema = ISurveyEditSchema

    def applyChanges(self, data):
        changes = super(Edit, self).applyChanges(data)
        if changes:
            # Reindex our parents title.
            catalog = getToolByName(self.context, "portal_catalog")
            catalog.indexObject(aq_parent(aq_inner(self.context)))
        return changes

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get("euphorie")
        if not settings.get("use_integrated_action_plan", False):
            self.widgets["integrated_action_plan"].mode = "hidden"


class Delete(actions.Delete):
    """Special delete action class which prevents deletion of published surveys
    or of the last survey in a group.
    """

    grok.context(ISurvey)

    def verify(self, container, context):
        flash = IStatusMessage(self.request).addStatusMessage

        if (
            hasattr(aq_base(container), "published")
            and container.published == context.id
        ):
            flash(
                _(
                    "message_no_delete_published_survey",
                    default=(
                        u"You cannot delete an OiRA Tool version that is published. "
                        u"Please unpublish it first."
                    ),
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


@grok.subscribe(ISurvey, ISurveyUnpublishEvent)
def handleSurveyUnpublish(survey, event):
    """Event handler (subscriber) for unpublishing a survey."""
    if hasattr(aq_base(survey), "published"):
        delattr(survey, "published")

    surveygroup = aq_parent(survey)
    if surveygroup.published == survey.id:
        surveygroup.published = None
