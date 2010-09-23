"""
Survey
======

A survey holds the entire risk assessment survey. The survey is a hierarchical
structure containing modules, profile questions and questions. Both modules and
profile questions are used to create the hierarchy. 
"""

from Acquisition import aq_inner
from Acquisition import aq_base
from Acquisition import aq_chain
from OFS.event import ObjectClonedEvent
from ZODB.POSException import ConflictError
from AccessControl import getSecurityManager
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope import schema
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.event import notify
from five import grok
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import resolveDottedName
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.add import DefaultAddForm
from plone.directives import form
from plone.directives import dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.app.dexterity.behaviors.metadata import IBasic
from htmllaundry.z3cform import HtmlText
from euphorie.content import MessageFactory as _
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.module import IModule
from euphorie.content.interfaces import IQuestionContainer


class ISurvey(form.Schema, IBasic):
    """RIE Survey.

    The survey is the root of a RIE survey.
    """
    title = schema.TextLine(
            title = _(u"Title"),
            description = _(u"This is the title of this survey version. This "
                            u"name is never shown to users."),
            required = True)
    form.order_before(title="*")

    form.omitted("description")

    introduction = HtmlText(
            title = _(u"Introduction text"),
            description = _(u"The introduction text is shown when starting a "
                            u"new survey session. If no introduction is "
                            u"provided here a standard text will be shown."
                            u"Please keep this text brief so it will easily "
                            u"fit on screens of small devices such as "
                            u"phones and PDAs"),
            required = False)
    form.widget(introduction=WysiwygFieldWidget)

    evaluation_optional = schema.Bool(
            title = _(u"Evaluation may be skipped"),
            description = _(u"This option allows uses to skip the evaluation "
                            u"phase."),
            default = False)


class Survey(dexterity.Container):
    """A risk assessment survey.

    A survey uses the *IIdGenerationRoot* behaviour to guarantee that
    all items inside the survey have a unique id.
    """

    implements(ISurvey, IQuestionContainer)

    @property
    def hasProfile(self):
        """Check if this survey has any non-deprecated profile questions.

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


class View(grok.View):
    grok.context(ISurvey)
    grok.require("zope2.View")

    def may_publish(self):
        return getSecurityManager().checkPermission(
                "Euphorie: Publish a Survey", aq_inner(self.context))

    def publish_link(self):
        return "%s/@@publish" % aq_inner(self.context).absolute_url()

    def preview_link(self):
        return "%s/@@preview" % aq_inner(self.context).absolute_url()

    def _morph(self, child):
        state=getMultiAdapter((child, self.request), name="plone_context_state")
        return dict(id=child.id,
                    title=child.title,
                    url=state.view_url())

    def profile_questions(self):
        return [self._morph(child) for child in self.context.ProfileQuestions()]

    def add_profile_url(self):
        return "%s/++add++euphorie.profilequestion" % \
                aq_inner(self.context).absolute_url()

    def add_module_url(self):
        return "%s/++add++euphorie.module" % \
                aq_inner(self.context).absolute_url()

    def modules(self):
        return [self._morph(child) for child in self.context.values()
                if IModule.providedBy(child)]



class TemplateSurveyVocabulary(object):
    """Vocabulary factory for a list of available template surveys. Candidate
    surveys are all surveys for a sector with id `templates` in the current
    country.
    """
    implements(IVocabularyFactory)

    def findCountry(self, context):
        for parent in aq_chain(aq_inner(context)):
            if getattr(aq_base(parent), "portal_type", None)=="euphorie.country":
                return parent


    def getTemplates(self, country):
        from euphorie.content.surveygroup import ISurveyGroup

        sector=country.get("templates", None)
        if not sector:
            return []

        groups=[group for group in sector.values()
                if ISurveyGroup.providedBy(group)]
        surveys=[]
        for group in groups:
            surveys.extend([(group, survey) for survey in group.values()
                              if ISurvey.providedBy(survey)])
        return surveys


    def __call__(self, context):
        options=[]
        country=self.findCountry(context)
        if country:
            templates=self.getTemplates(country)
            templates.sort(key=lambda s: (s[0].title, s[1].title))
            options.extend([SimpleTerm("/".join(survey.getPhysicalPath()),
                                        u"%s / %s" % (group.title, survey.title))
                            for (group, survey) in templates])
        options[:0]=[SimpleTerm(u"", _("no_survey_skeleton", default=u"None"))]
        return SimpleVocabulary(options)

TemplateSurveyVocabularyFactory = TemplateSurveyVocabulary()



class ITemplateSchema(form.Schema):
    template = schema.Choice(
            title = _(u"Template"),
            description = _(u"Select a generic survey as base for this survey."),
            vocabulary = "euphorie.content.survey.templates",
            default=u"",
            required = True)
    form.order_after(template="title")



class AddForm(DefaultAddForm):
    """Custom add form for :obj:`Survey` instances. This add form adds a
    the :obj:`ITemplateSchema` schema, which allows users to pick a template
    survey to use as a basis for the new survey.
    """

    @property
    def additionalSchemata(self):
        yield ITemplateSchema

        fti = getUtility(IDexterityFTI, name=self.portal_type)
        for behavior_name in fti.behaviors:
            try:
                behavior_interface = resolveDottedName(behavior_name)
            except ValueError:
                continue
            if behavior_interface is not None:
                behavior_schema = IFormFieldProvider(behavior_interface, None)
                if behavior_schema is not None:
                    yield behavior_schema
    

    def copyTemplate(self, template, target):
        target=self.context[target.id] # Acquisition-wrap
        template=aq_chain(target)[-2].unrestrictedTraverse(template)
        for source in template.values():
            try:
                source._notifyOfCopyTo(target, op=0)
            except ConflictError:
                raise

            copy=source._getCopy(target)
            target._setObject(copy.id, copy)
            copy=target[copy.id] # Acquisition-wrap
            copy.wl_clearLocks()
            copy._postCopy(target, op=0)
            notify(ObjectClonedEvent(copy))


    def createAndAdd(self, data):
        template=data.get("ITemplateSchema.template", None)
        if template is not None:
            # If we keep this in z3c.form.applyChanges makes zope segfault when
            # it tries to set the field on the instance.
            del data["ITemplateSchema.template"]
        obj=super(AddForm, self).createAndAdd(data)
        if template:
            self.copyTemplate(template, obj)
        return obj
    

class AddView(DefaultAddView):
    """Custom add view factory. This is needed to hook up the :obj:`AddForm`
    custom add form.
    """
    form = AddForm

