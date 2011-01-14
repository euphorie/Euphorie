from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from zope.interface import implements
from zope.interface import Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from htmllaundry.z3cform import HtmlText
from euphorie.content.fti import ConditionalDexterityFTI
from euphorie.content.fti import IConstructionFilter
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content import MessageFactory as _
from euphorie.content.utils import getTermTitle
from euphorie.content.utils import StripMarkup
from euphorie.content.solution import ISolution
from plone.namedfile import field as filefield
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.directives import depends
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from plone.indexer import indexer

grok.templatedir("templates")


TextSpan7 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget", klass="span-7")
TextLines4Rows = FieldWidgetFactory("z3c.form.browser.textlines.TextLinesFieldWidget", rows=4)


class IRisk(form.Schema, IRichDescription, IBasic):
    """A possible risk that can be present in an organisation.
    """

    title = schema.TextLine(
            title = _("label_statement", default=u"Statement"),
            description = _("help_statement",
                default=u"This is a short statement about a possible risk."),
            required = True)
    form.widget(title="euphorie.content.risk.TextSpan7")
    form.order_before(title="*")

    problem_description = schema.TextLine(
            title = _("label_problem_description",
                    default=u"Inversed statement"),
            description = _("help_problem_description",
                    default=u"This is the inverse of the statement: a "
                            u"short description of current (bad) situation."),
            required = True)
    form.widget(problem_description="euphorie.content.risk.TextLines4Rows")
    form.order_after(problem_description="title")

    description = HtmlText(
            title = _("label_description", default=u"Description"),
            description = _("help_risk_description",
                default=u"Describe the risk. Include any relevant "
                        u"information that may be helpful for users."),
            required = True)
    form.widget(description="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    form.order_after(description="problem_description")

    legal_reference = HtmlText(
            title = _("label_legal_reference", default=u"Legal and policy references"),
            required=False)
    form.widget(legal_reference="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    form.order_after(legal_reference="description")

    form.fieldset("identification",
            label=_("header_identification", default=u"Identification"),
            fields=["show_notapplicable"])

    show_notapplicable = schema.Bool(
            title = _("label_show_notapplicable",
                default=u"Show `not applicable' option"),
            description = _("help_show_notapplicable",
                default=u"Offer a `not applicable' option in addition "
                        u"to the standard yes/no options."),
            default = False)

    form.fieldset("evaluation",
            label=_("header_evaluation", default=u"Evaluation"),
            description = _("intro_evaluation",
                default=u"You can specify how the risks priority is "
                        u"evaluated. For more details see the online "
                        u"manual."),
            fields=["type", "evaluation_method",
                    "default_priority",
                    "default_probability", "default_frequency", "default_effect",
                   ])

    type = schema.Choice(
            title = _("label_risk_type", default=u"Risk type"),
            description = _("help_risk_type",
                default=u"'Risk' is related to the workplace. 'Policy' is "
                        u"related to agreements, procedures and management "
                        u"decisions. It can be answered from behind a desk "
                        u"(no need to examine the workplace). 'Top 5' is one "
                        "of the top five risks of the sector."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(u"top5", title=_("risktype_top5", default=u"Top 5")),
                            SimpleTerm(u"risk", title=_("risktype_risk", default="Risk")),
                            SimpleTerm(u"policy", title=_("risktype_policy", default=u"Policy")),
                            ]),
            default = u"risk",
            required = True)


    depends("evaluation_method", "type", "==", "risk")
    evaluation_method = schema.Choice(
            title = _("label_evaluation_method", default=u"Evaluation method"),
            description = _("help_evaluation_method",
                default=u"Select 'estimated' if calcuation is not necessary "
                        u"or not possible."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(u"direct", title=_("evalmethod_direct", default=u"Estimated")),
                            SimpleTerm(u"calculated", title=_("evalmethod_calculated", default=u"Calculated")),
                            ]),
            default = u"calculated",
            required = False)

    depends("default_priority", "type", "==", "risk")
    depends("default_priority", "evaluation_method", "==", "direct")
    default_priority = schema.Choice(
            title = _("label_default_priority", default=u"Default priority"),
            description = _("help_default_priority",
                default=u"You can help the user by selecting a default "
                        u"priority. The user can still change the priority."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm("none", title=_("no_default", default=u"No default")),
                            SimpleTerm("low", title=_("priority_low", default=u"Low")),
                            SimpleTerm("medium", title=_("priority_medium", default=u"Medium")),
                            SimpleTerm("high", title=_("priority_high", default="High")),
                            ]),
            required = False,
            default = "none")
                      
    depends("default_probability", "type", "==", "risk")
    depends("default_probability", "evaluation_method", "==", "calculated")
    default_probability = schema.Choice(
            title = _("label_default_probability", default=u"Default probability"),
            description = _("help_default_probability",
                default=u"Indicate how likely occurence of this risk "
                        u"is in a normal situation."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(0, "none", title=_("no default", default=u"No default")),
                            SimpleTerm(1, "small", title=_("probability_small", default=u"Small")),
                            SimpleTerm(3, "medium", title=_("probability_medium", default=u"Medium")),
                            SimpleTerm(5, "large", title=_("probability_large", default=u"Large")),
                            ]),
            required = False,
            default = 0)

    depends("default_frequency", "type", "==", "risk")
    depends("default_frequency", "evaluation_method", "==", "calculated")
    default_frequency = schema.Choice(
            title = _("label_default_frequency", default=u"Default frequency"),
            description = _("help_default_frequency",
                default=u"Indicate how often this risk occurs in a "
                        u"normal situation."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(0, "none", title=_("no default", default=u"No default")),
                            SimpleTerm(1, "almost-never", title=_("frequency_almostnever", default=u"Almost never")),
                            SimpleTerm(4, "regular", title=_("frequency_regularly", default=u"Regularly")),
                            SimpleTerm(7, "constant", title=_("frequency_constantly", default=u"Constantly")),
                            ]),
            required = False,
            default = 0)

    depends("default_effect", "type", "==", "risk")
    depends("default_effect", "evaluation_method", "==", "calculated")
    default_effect = schema.Choice(
            title = _("label_default_severity", default=u"Default severity"),
            description = _("help_default_severity",
                default=u"Indicate the severity of the manage if this risk occurs."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(0, "none", title=_("no default", default=u"No default")),
                            SimpleTerm(1, "weak", title=_("effect_weak", default=u"Weak severity")),
                            SimpleTerm(5, "significant", title=_("effect_significant", default=u"Significant severity")),
                            SimpleTerm(10, "high", title=_("effect_high", default=u"High (very high) severity")),
                            ]),
            required = False,
            default = 0)

    form.fieldset("main_image",
            label=_("header_main_image", default=u"Main image"),
            description=_("intro_main_image",
                default=u"The main image will get a more prominent position in "
                        u"the client than the other images."),
            fields=["image", "caption"])

    image = filefield.NamedBlobImage(
            title = _("label_image", default=u"Image file"),
            description = _("help_image_upload",
                default=u"Upload an image. Make sure your image is of format png, jpg "
                        u"or gif and does not contain any special characters."),
            required = False)
    caption = schema.TextLine(
            title = _("label_caption", default=u"Image caption"),
            required=False)

    form.fieldset("secondary_images",
            label=_("header_secondary_images", default=u"Secondary images"),
            fields=["image2", "caption2", "image3", "caption3", "image4", "caption4" ])

    image2 = filefield.NamedBlobImage(
            title = _("label_image", default=u"Image file"),
            description = _("help_image_upload",
                default=u"Upload an image. Make sure your image is of format png, jpg "
                        u"or gif and does not contain any special characters."),
            required = False)
    caption2 = schema.TextLine(
            title = _("label_caption", default=u"Image caption"),
            required=False)

    image3 = filefield.NamedBlobImage(
            title = _("label_image", default=u"Image file"),
            description = _("help_image_upload",
                default=u"Upload an image. Make sure your image is of format png, jpg "
                        u"or gif and does not contain any special characters."),
            required = False)
    caption3 = schema.TextLine(
            title = _("label_caption", default=u"Image caption"),
            required=False)

    image4 = filefield.NamedBlobImage(
            title = _("label_image", default=u"Image file"),
            description = _("help_image_upload",
                default=u"Upload an image. Make sure your image is of format png, jpg "
                        u"or gif and does not contain any special characters."),
            required = False)
    caption4 = schema.TextLine(
            title = _("label_caption", default=u"Image caption"),
            required=False)




class Risk(dexterity.Container):
    implements(IRisk)




@indexer(IRisk)
def SearchableTextIndexer(obj):
    return " ".join([obj.title,
                     StripMarkup(obj.problem_description),
                     StripMarkup(obj.description),
                     StripMarkup(obj.legal_reference)])


class View(grok.View):
    grok.context(IRisk)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("risk_view")
    grok.name("nuplone-view")

    def update(self):
        super(View, self).update()
        context=aq_inner(self.context)
        self.module_title=aq_parent(context).title
        self.type=getTermTitle(IRisk["type"], context.type)
        self.evaluation_method=getTermTitle(IRisk["evaluation_method"], context.evaluation_method)
        self.default_priority=getTermTitle(IRisk["default_priority"], context.default_priority)
        self.default_probability=getTermTitle(IRisk["default_probability"], context.default_probability)
        self.default_frequency=getTermTitle(IRisk["default_frequency"], context.default_frequency)
        self.default_effect=getTermTitle(IRisk["default_effect"], context.default_effect)

        self.solutions=[dict(id=solution.id,
                             url=solution.absolute_url(),
                             description=solution.description)
                        for solution in context.values()
                        if ISolution.providedBy(solution)]


class Edit(form.SchemaEditForm):
    grok.context(IRisk)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("edit")
    grok.template("risk_edit")

    schema = IRisk
    default_fieldset_label = None



class ConstructionFilter(grok.MultiAdapter):
    """FTI construction filter for :py:class:`Risk` objects. This filter
     prevents creating of modules if the current container already contains a
     module.

    This multi adapter requires the use of the conditional FTI as implemented
    by :py:class:`euphorie.content.fti.ConditionalDexterityFTI`.
    """

    grok.adapts(ConditionalDexterityFTI, Interface)
    grok.implements(IConstructionFilter)
    grok.name("euphorie.risk")

    def __init__(self, fti, container):
        self.fti=fti
        self.container=container

    def checkForModules(self):
        """Check if the container already contains a module. If so refuse to
        allow creation of a risk.
        """
        for key in self.container:
            pt=self.container[key].portal_type
            if pt=="euphorie.module":
                return False
        else:
            return True


    def allowed(self):
        return self.checkForModules()

