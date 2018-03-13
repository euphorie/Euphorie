# coding=utf-8
"""
Profile Question
----------------

A Profile Question is a container for Modules. A question is used to determine
whether or not a Module should be enabled, or whether it should be repeated.

portal_type: euphorie.profilequestion
"""
from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from .behaviour.uniqueid import get_next_id
from .behaviour.uniqueid import INameFromUniqueId
from .fti import check_fti_paste_allowed
from .interfaces import IQuestionContainer
from .module import ConstructionFilter
from .module import IModule
from .module import item_depth
from .module import tree_depth
from .risk import IRisk
from .utils import StripMarkup
from euphorie.content.dependency import ConditionalTextLine
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from plone.indexer import indexer
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.directives import depends
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implements

import sys


grok.templatedir("templates")


class IProfileQuestion(form.Schema, IRichDescription, IBasic):
    """Survey Profile question.

    A profile question is used to determine if parts of a survey should
    be skipped, or repeated multiple times.
    """
    question = schema.TextLine(
        title=_('label_profilequestion_question', default=u'Question'),
        description=_(u'This question must ask the user if this profile '
                      u'applies to them.'),
        required=True)
    form.widget(question="euphorie.content.risk.TextLines4Rows")

    use_location_question = schema.Bool(
        title=_("label_use_location_question",
                default=u"Ask the user about (multiple) locations?"),
        description=_(
            u'description_use_location_question',
            default=u'If this part is active, the user will be asked to '
            u'enter the name of all locations for which this module applies. '
            u'This means, the module will be repeated as many times as there '
            u'are locations. If you do not need this repeatable behaviour, '
            u'untick the checkbox to turn it off.'
        ),
        required=False,
        default=True)

    depends("label_multiple_present",
            "use_location_question",
            "on")
    label_multiple_present = ConditionalTextLine(
        title=_(u'Multiple item question'),
        required=True,
        description=_(u'This question must ask the user if the service is '
                      u'offered in more than one location.'),
    )
    form.widget(label_multiple_present="euphorie.content.risk.TextLines4Rows")

    depends("label_single_occurance",
            "use_location_question",
            "on")
    label_single_occurance = ConditionalTextLine(
        title=_(u'Single occurance prompt'),
        description=_(u'This must ask the user for the name of the '
                      u'relevant location.'),
        required=True)
    form.widget(label_single_occurance="euphorie.content.risk.TextLines4Rows")

    depends("label_multiple_occurances",
            "use_location_question",
            "on")
    label_multiple_occurances = ConditionalTextLine(
        title=_(u'Multiple occurance prompt'),
        description=_(u'This must ask the user for the names of all '
                      u'relevant locations.'),
        required=True)
    form.widget(label_multiple_occurances="euphorie.content.risk.TextLines4Rows")


class ProfileQuestion(dexterity.Container):
    implements(IProfileQuestion, IQuestionContainer)
    portal_type = 'euphorie.profilequestion'

    question = None
    image = None
    optional = False

    def _get_id(self, orig_id):
        """Pick an id for pasted content."""
        frame = sys._getframe(1)
        ob = frame.f_locals.get('ob')
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super(ProfileQuestion, self)._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super(ProfileQuestion, self)._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)
            if IQuestionContainer.providedBy(object):
                my_depth = item_depth(self)
                paste_depth = tree_depth(object)
                if my_depth + paste_depth > ConstructionFilter.maxdepth:
                    raise ValueError('Pasting would create a too deep structure.')


@indexer(IProfileQuestion)
def SearchableTextIndexer(obj):
    """ Index the title and description
    """
    return " ".join([obj.title,
                     StripMarkup(obj.description)])


class View(grok.View):
    """ View name: @@nuplone-view
    """
    grok.context(IProfileQuestion)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("profilequestion_view")
    grok.name("nuplone-view")

    def _morph(self, child):
        state = getMultiAdapter((child, self.request),
                name="plone_context_state")
        return {'id': child.id,
                'title': child.title,
                'url': state.view_url()}

    def update(self):
        """ Provide view attributes which list modules and risks in the current
        context.
        """
        self.modules = [self._morph(child)
                        for child in self.context.values()
                        if IModule.providedBy(child)]
        self.risks = [self._morph(child) for child in self.context.values()
                      if IRisk.providedBy(child)]


class AddForm(dexterity.AddForm):
    """ View name: euphorie.profilequestion
    """
    grok.context(IProfileQuestion)
    grok.name('euphorie.profilequestion')
    grok.require('euphorie.content.AddNewRIEContent')
    grok.layer(NuPloneSkin)
    form.wrap(True)

    schema = IProfileQuestion
    template = ViewPageTemplateFile('templates/profilequestion_add.pt')

    @property
    def label(self):
        return _(u"Add Profile question")


class EditForm(dexterity.EditForm):
    grok.context(IProfileQuestion)
    grok.require('cmf.ModifyPortalContent')
    grok.layer(NuPloneSkin)
    form.wrap(True)

    schema = IProfileQuestion
    template = ViewPageTemplateFile('templates/profilequestion_add.pt')

    @property
    def label(self):
        return _(u"Edit Profile question")
