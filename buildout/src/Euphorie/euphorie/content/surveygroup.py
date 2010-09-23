from Acquisition import aq_inner
from zope import schema
from zope.interface import implements
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from euphorie.content import MessageFactory as _
from euphorie.content.survey import ISurvey


class ISurveyGroup(form.Schema, IBasic):
    title = schema.TextLine(
            title = _(u"Title"),
            description = _(u"The title of this survey. This title is used in "
                            u"the survey overview in the clients."),
            default = _(u"Standard survey"),
            required = True)
    form.order_before(title="*")

    form.omitted("description")

    language = schema.Choice(
            title = _(u"Language"),
            description = _(u""),
            vocabulary = "plone.app.vocabularies.AvailableContentLanguages",
            default = u"en",
            required = True)

    classification_code = schema.ASCIILine(
           title = _(u"Classification code"),
           description = _(u"A code identifying this sector. Classification "
                           u"codes are defined by national standards bodies "
                           u"and based on revision 2 of the NACE standard."),
           required = True)


class SurveyGroup(dexterity.Container):
        implements(ISurveyGroup)



class View(grok.View):
    grok.context(ISurveyGroup)
    grok.require("zope2.View")

    def update(self):
        self.add_survey_url="%s/++add++euphorie.survey" % \
                aq_inner(self.context).absolute_url()
        self.surveys=[dict(id=survey.id,
                           title=survey.title,
                           url=survey.absolute_url())
                      for survey in self.context.values()
                      if ISurvey.providedBy(survey)]
        super(View, self).update()


from Acquisition import aq_chain
from OFS.event import ObjectClonedEvent
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.event import notify
from euphorie.content.survey import ITemplateSchema
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import resolveDottedName
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.add import DefaultAddForm
from plone.autoform.interfaces import IFormFieldProvider

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
        source=aq_chain(target)[-2].unrestrictedTraverse(template)
        try:
            source._notifyOfCopyTo(target, op=0)
        except ConflictError:
            raise

        copy=source._getCopy(target)
        target._setObject(copy.id, copy)

        copy=target[copy.id] # Acquisition-wrap
        copy.wl_clearLocks()
        copy._postCopy(target, op=0)
        notify(ObjectClonedEvent(target[copy.id]))


    def createAndAdd(self, data):
        template=data.get("ITemplateSchema.template", None)
        if template is not None:
            # If we keep this in z3c.form.applyChanges makes zope segfault when
            # it tries to set the field on the instance.
            del data["ITemplateSchema.template"]
        obj=super(AddForm, self).createAndAdd(data)
        if template:
            self.copyTemplate(template, obj)
            pass
        return obj
    

class AddView(DefaultAddView):
    """Custom add view factory. This is needed to hook up the :obj:`AddForm`
    custom add form.
    """
    form = AddForm

