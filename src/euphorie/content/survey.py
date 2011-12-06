"""
Survey
======

A survey holds the entire risk assessment survey. The survey is a hierarchical
structure containing modules, profile questions and questions. Both modules and
profile questions are used to create the hierarchy. 
"""

from Acquisition import aq_inner
from Acquisition import aq_parent
from ZODB.POSException import ConflictError
from OFS.event import ObjectClonedEvent
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.event import notify
from zope import schema
from five import grok
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.container.interfaces import INameChooser
from plone.directives import form
from plone.directives import dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.app.dexterity.behaviors.metadata import IBasic
from htmllaundry.z3cform import HtmlText
from Products.statusmessages.interfaces import IStatusMessage
from Products.Archetypes.utils import shasattr
from euphorie.content import MessageFactory as _
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.module import IModule
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.interfaces import ISurveyUnpublishEvent
from euphorie.content.utils import StripMarkup
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.skin import actions
from plone.indexer import indexer


grok.templatedir("templates")

class ISurvey(form.Schema, IBasic):
    """Survey.

    The survey is the root of a survey.
    """
    title = schema.TextLine(
            title = _("label_survey_title", default=u"Version name"),
            description = _("help_survey_title",
                default=u"This is the title of this survey version. This "
                        u"name is never shown to users."),
            required = True)
    form.order_before(title="*")

    form.omitted("description")

    introduction = HtmlText(
            title = _("label_introduction", default=u"Introduction text"),
            description = _("help_introduction",
                default=u"The introduction text is shown when starting a "
                        u"new survey session. If no introduction is "
                        u"provided here a standard text will be shown."
                        u"Please keep this text brief so it will easily "
                        u"fit on screens of small devices such as "
                        u"phones and PDAs"),
            required = False)
    form.widget(introduction=WysiwygFieldWidget)

    evaluation_optional = schema.Bool(
            title = _("label_evaluation_optional", default=u"Evaluation may be skipped"),
            description = _("help_evaluation_optional",
                default=u"This option allows uses to skip the evaluation phase."),
            default = False,
            required = False)

    language = schema.Choice(
            title = _("label_language", default=u"Language"),
            vocabulary = "plone.app.vocabularies.AvailableContentLanguages",
            default = u"en",
            required = True)

    classification_code = schema.ASCIILine(
           title = _("label_classification_code", default=u"Classification code"),
           description = _("help_classification_code",
               default=u"A code identifying this sector. Classification "
                       u"codes are defined by national standards bodies "
                       u"and based on revision 2 of the NACE standard."),
           required = False)



class Survey(dexterity.Container):
    """A risk assessment survey.

    A survey uses the *IIdGenerationRoot* behaviour to guarantee that
    all items inside the survey have a unique id.
    """
    grok.name("euphorie.container")

    implements(ISurvey, IQuestionContainer)

    dirty = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False


    @property
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

    def ProfileQuestions(self):
        """Return a list of all profile questions."""
        return [child for child in self.values()
                if IProfileQuestion.providedBy(child)]



@indexer(ISurvey)
def SearchableTextIndexer(obj):
    return " ".join([obj.title,
                     StripMarkup(obj.description),
                     StripMarkup(obj.introduction),
                     obj.classification_code or u""])



class View(grok.View):
    grok.context(ISurvey)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("survey_view")
    grok.name("nuplone-view")

    def _morph(self, child):
        state=getMultiAdapter((child, self.request), name="plone_context_state")
        return dict(id=child.id,
                    title=child.title,
                    url=state.view_url())

    def profile_questions(self):
        return [self._morph(child) for child in self.context.ProfileQuestions()]

    def modules(self):
        return [self._morph(child) for child in self.context.values()
                if IModule.providedBy(child)]

    def update(self):
        self.group=aq_parent(aq_inner(self.context))
        super(View, self).update()



class ISurveyAddSchema(form.Schema):
    title = schema.TextLine(
            title = _("label_survey_title", default=u"Version name"),
            description = _("help_survey_title",
                default=u"This is the title of this survey version. This "
                        u"name is never shown to users."),
            required = True)



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
        templates=[dict(id=survey.id,
                   title=survey.title)
                   for survey in self.context.values()
                   if ISurvey.providedBy(survey)]
        return templates


    def copyTemplate(self, source, title):
        target=aq_inner(self.context)
        try:
            source._notifyOfCopyTo(target, op=0)
        except ConflictError:
            raise

        copy=source._getCopy(target)
        copy.title=title
        chooser=INameChooser(target)
        copy.id=chooser.chooseName(None, copy)
        target._setObject(copy.id, copy)

        copy=target[copy.id] # Acquisition-wrap
        copy.wl_clearLocks()
        copy._postCopy(target, op=0)
        notify(ObjectClonedEvent(target[copy.id]))
        return copy


    def createAndAdd(self, data):
        surveygroup=aq_inner(self.context)
        template=surveygroup[self.request.form["survey"]]
        survey=self.copyTemplate(template, data["title"])
        self.immediate_view=survey.absolute_url()
        return survey



class Delete(actions.Delete):
    """Special delete action class which prevents deletion of published surveys
       or of the last survey in a group.
    """
    grok.context(ISurvey)

    def verify(self, container, context):
        flash = IStatusMessage(self.request).addStatusMessage

        if shasattr(container, 'published') and container.published==context.id:
            flash(_("message_no_delete_published_survey", 
                    default=u"You cannot delete a survey that is published. Please unpublish it first."), 
                    "error")
            self.request.response.redirect(context.absolute_url())
            return False

        count=0
        for survey in container.values():
            if ISurvey.providedBy(survey):
                count+=1

        if count > 1:
            return True
        else:
            flash(_("message_delete_no_last_survey", 
                    default=u"You can not delete the only survey version."), 
                    "error")
            self.request.response.redirect(context.absolute_url())
            return False


@grok.subscribe(ISurvey, ISurveyUnpublishEvent)
def handleSurveyUnpublish(survey, event):
    """Event handler (subscriber) for unpublishing a survey."""
    if shasattr(survey, "published"):
        delattr(survey, "published")

    surveygroup=aq_parent(survey)
    if surveygroup.published==survey.id:
        surveygroup.published=None


