# -*- coding: UTF-8 -*-
"""
Risk
----

An individual "question" about a risk that the user needs to answer.

portal_type: euphorie.risk
"""

from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from .behaviour.uniqueid import get_next_id
from .behaviour.uniqueid import INameFromUniqueId
from .fti import check_fti_paste_allowed
from .fti import ConditionalDexterityFTI
from .fti import IConstructionFilter
from .solution import ISolution
from .utils import DragDropHelper
from .utils import getTermTitleByValue
from .utils import StripMarkup
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition.interfaces import IAcquirer
from euphorie.content.utils import IToolTypesInfo
from five import grok
from htmllaundry.z3cform import HtmlText
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import dexterity
from plone.directives import form
from plone.indexer import indexer
from plone.memoize.instance import memoize
from plone.namedfile import field as filefield
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.directives import depends
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from z3c.appconfig.interfaces import IAppConfig
from z3c.form.form import applyChanges
from zope import schema
from zope.component import createObject
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from zope.interface import noLongerProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import sys

grok.templatedir("templates")


TextLines4Rows = FieldWidgetFactory(
    "z3c.form.browser.textlines.TextLinesFieldWidget", rows=4)


class TextLinesWithBreaks(schema.TextLine):

    def constraint(self, value):
        return True

TextLines8Rows = FieldWidgetFactory(
    "z3c.form.browser.textlines.TextLinesFieldWidget", rows=8)


class IRisk(form.Schema, IRichDescription, IBasic):
    """A possible risk that can be present in an organisation.
    """

    title = schema.TextLine(
            title=_("label_statement", default=u"Affirmative statement"),
            description=_("help_statement",
                default=u"This is a short affirmative statement about a "
                    u"possible risk (e.g. The building is well maintained.)"),
            required=True)
    form.widget(title="euphorie.content.risk.TextLines4Rows")
    form.order_before(title="*")

    problem_description = schema.TextLine(
            title=_("label_problem_description",
                    default=u"Negative statement"),
            description=_("help_problem_description",
                    default=u"This is the inverse of the affirmative "
                        u"statement (e.g. The building is not well maintained.)"),
            required=True)
    form.widget(problem_description="euphorie.content.risk.TextLines4Rows")
    form.order_after(problem_description="title")

    description = HtmlText(
            title=_("label_description", default=u"Description"),
            description=_("help_risk_description",
                default=u"Describe the risk. Include any relevant information "
                    u"that may be helpful for the end-user."),
            required=True)
    form.widget(description="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    form.order_after(description="problem_description")

    existing_measures = TextLinesWithBreaks(
        title=_(
            "deprecated_label_existing_measures",
            default=u"Measures that are already in place (Only shown here for "
            u"reference! Use the “Add Measure” button on the Risk for adding "
            u"measures that are shown to the user during Identification.)"),
        description=_(
            "help_existing_measures",
            default=u"Use this field to define (common) measures that the "
            u"user might have already implemented. "
            u"Separate measures with a line break (Enter). The user will be "
            u"able to deselect those measures that are not applicable to their"
            u"situation."),
        required=False)
    form.widget(existing_measures="euphorie.content.risk.TextLines8Rows")
    form.order_after(existing_measures="description")

    legal_reference = HtmlText(
            title=_("label_legal_reference",
                default=u"Legal and policy references"),
            required=False)
    form.widget(legal_reference="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    form.order_after(legal_reference="description")

    form.fieldset("identification",
            label=_("header_identification", default=u"Identification"),
            fields=["show_notapplicable"])

    show_notapplicable = schema.Bool(
            title=_("label_show_notapplicable",
                default=u"Show `not applicable' option"),
            description=_("help_show_notapplicable",
                default=u"Offer a `not applicable' option in addition "
                        u"to the standard yes/no options."),
            default=False)

    type = schema.Choice(
            title=_("label_risk_type", default=u"Risk type"),
            description=_("help_risk_type",
                default=u'"Priority risk" is one of the high risks in the '
                    u'sector. "Risk" is related to the workplace or to the work '
                    u'carried out. "Policy" refers to agreements, procedures, '
                    u'and management decisions.'),
            vocabulary=SimpleVocabulary([
                            SimpleTerm(u"top5",
                                title=_("risktype_top5", default=u"Priority risk")),
                            SimpleTerm(u"risk",
                                title=_("risktype_risk", default="Risk")),
                            SimpleTerm(u"policy",
                                title=_("risktype_policy", default=u"Policy")),
                            ]),
            default=u"risk",
            required=True)

    depends("risk_always_present", "type", "==", "risk")
    risk_always_present = schema.Bool(
        title=_("label_risk_always_present", default=u"Risk is always present"),
        description=_(
            "description_risk_always_present",
            default=u'If selected, the user will not be able to answer "Yes" or '
            '"No", since the risk is considered to be always present. The '
            'Evaluation and Action Plan will behave in the same way as for '
            'regular risks.'
        ),
        required=False,
        default=False,
    )

    depends("evaluation_method", "type", "==", "risk")
    evaluation_method = schema.Choice(
            title=_("label_evaluation_method", default=u"Evaluation method"),
            description=_("help_evaluation_method",
                default=u"Select 'estimated' if calcuation is not necessary "
                        u"or not possible."),
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"direct",
                    title=_("evalmethod_direct", default=u"Estimated")),
                SimpleTerm(u"calculated",
                    title=_("evalmethod_calculated", default=u"Calculated")),
                SimpleTerm(u"fixed",
                    title=_("evalmethod_fixed", default=u"Skip evaluation")),
            ]),
            default=u"calculated",
            required=False)

    depends("fixed_priority", "type", "==", "risk")
    depends("fixed_priority", "evaluation_method", "==", "fixed")
    fixed_priority = schema.Choice(
            title=_("report_timeline_priority", default=u"Priority"),
            vocabulary=SimpleVocabulary([
                SimpleTerm("low", title=_("priority_low", default=u"Low")),
                SimpleTerm("medium",
                    title=_("priority_medium", default=u"Medium")),
                SimpleTerm("high", title=_("priority_high", default="High")),
            ]),
            required=False,
            default="low")

    depends("default_priority", "type", "==", "risk")
    depends("default_priority", "evaluation_method", "==", "direct")
    default_priority = schema.Choice(
            title=_("label_default_priority", default=u"Default priority"),
            description=_("help_default_priority",
                default=u"You can help the end-user by selecting a default "
                    u"priority. He/she can still change the priority."),
            vocabulary=SimpleVocabulary([
                SimpleTerm("none",
                    title=_("no_default", default=u"No default")),
                SimpleTerm("low", title=_("priority_low", default=u"Low")),
                SimpleTerm("medium",
                    title=_("priority_medium", default=u"Medium")),
                SimpleTerm("high", title=_("priority_high", default="High")),
            ]),
            required=False,
            default="low")

    form.fieldset("main_image",
            label=_("header_main_image", default=u"Main image"),
            description=_("intro_main_image",
                default=u"The main image will get a more prominent position "
                        u"in the client than the other images."),
            fields=["image", "caption"])

    image = filefield.NamedBlobImage(
            title=_("label_image", default=u"Image file"),
            description=_("help_image_upload",
                default=u"Upload an image. Make sure your image is of format "
                        u"png, jpg or gif and does not contain any special "
                        u"characters."),
            required=False)
    caption = schema.TextLine(
            title=_("label_caption", default=u"Image caption"),
            required=False)

    form.fieldset("secondary_images",
            label=_("header_secondary_images", default=u"Secondary images"),
            fields=["image2", "caption2", "image3", "caption3",
                    "image4", "caption4"])

    image2 = filefield.NamedBlobImage(
            title=_("label_image", default=u"Image file"),
            description=_("help_image_upload",
                default=u"Upload an image. Make sure your image is of format "
                        u"png, jpg or gif and does not contain any special "
                        u"characters."),
            required=False)
    caption2 = schema.TextLine(
            title=_("label_caption", default=u"Image caption"),
            required=False)

    image3 = filefield.NamedBlobImage(
            title=_("label_image", default=u"Image file"),
            description=_("help_image_upload",
                default=u"Upload an image. Make sure your image is of format "
                        u"png, jpg or gif and does not contain any special "
                        u"characters."),
            required=False)
    caption3 = schema.TextLine(
            title=_("label_caption", default=u"Image caption"),
            required=False)

    image4 = filefield.NamedBlobImage(
            title=_("label_image", default=u"Image file"),
            description=_("help_image_upload",
                default=u"Upload an image. Make sure your image is of format "
                        u"png, jpg or gif and does not contain any special "
                        u"characters."),
            required=False)
    caption4 = schema.TextLine(
            title=_("label_caption", default=u"Image caption"),
            required=False)

    form.fieldset(
        "additional_content",
        label=_("header_additional_content", default=u"Additional content"),
        description=_(
            "intro_additional_content",
            default=u"Attach any additional content you consider helpful "
            "for the user"),
        fields=[
            "file1", "file1_caption", "file2", "file2_caption",
            "file3", "file3_caption", "file4", "file4_caption"])

    file1 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file1_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)

    file2 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file2_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)

    file3 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file3_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)

    file4 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file4_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)


class IFrenchEvaluation(form.Schema):
    depends("default_severity", "type", "==", "risk")
    depends("default_severity", "evaluation_method", "==", "calculated")
    default_severity = schema.Choice(
            title=_("label_default_severity", default=u"Default severity"),
            description=_("help_default_severity",
                default=u"Indicate the severity if this risk occurs."),
            vocabulary=SimpleVocabulary([
                SimpleTerm(0, "none",
                    title=_("no default", default=u"No default")),
                SimpleTerm(1, "weak",
                    title=_("severity_weak", default=u"Weak")),
                SimpleTerm(5, "not-severe",
                    title=_("severity_not_severe",
                        default=u"Not very severe")),
                SimpleTerm(7, "severe",
                    title=_("severity_severe", default=u"Severe")),
                SimpleTerm(10, "very-severe",
                    title=_("severity_very_severe", default=u"Very severe")),
            ]),
            required=True,
            default=0)

    depends("default_frequency", "type", "==", "risk")
    depends("default_frequency", "evaluation_method", "==", "calculated")
    default_frequency = schema.Choice(
            title=_("label_default_frequency", default=u"Default frequency"),
            description=_("help_default_frequency",
                default=u"Indicate how often this risk occurs in a "
                        u"normal situation."),
            vocabulary=SimpleVocabulary([
                SimpleTerm(0, "none",
                    title=_("no default", default=u"No default")),
                SimpleTerm(1, "rare",
                    title=_("frequency_french_rare", default=u"Rare")),
                SimpleTerm(3, "not-often",
                    title=_("frequency_french_not_often",
                        default=u"Not very often")),
                SimpleTerm(7, "often",
                    title=_("frequency_french_often", default=u"Often")),
                SimpleTerm(9, "regularly",
                    title=_("frequency_french_regularly",
                        default=u"Very often or regularly")),
            ]),
            required=True,
            default=0)


class IKinneyEvaluation(form.Schema):
    depends("default_probability", "type", "==", "risk")
    depends("default_probability", "evaluation_method", "==", "calculated")
    default_probability = schema.Choice(
            title=_("label_default_probability",
                default=u"Default probability"),
            description=_("help_default_probability",
                default=u"Indicate how likely occurence of this risk "
                        u"is in a normal situation."),
            vocabulary=SimpleVocabulary([
                SimpleTerm(0, "none",
                    title=_("no default", default=u"No default")),
                SimpleTerm(1, "small",
                    title=_("probability_small", default=u"Small")),
                SimpleTerm(3, "medium",
                    title=_("probability_medium", default=u"Medium")),
                SimpleTerm(5, "large",
                    title=_("probability_large", default=u"Large")),
            ]),
            required=False,
            default=0)

    depends("default_frequency", "type", "==", "risk")
    depends("default_frequency", "evaluation_method", "==", "calculated")
    default_frequency = schema.Choice(
            title=_("label_default_frequency", default=u"Default frequency"),
            description=_("help_default_frequency",
                default=u"Indicate how often this risk occurs in a "
                        u"normal situation."),
            vocabulary=SimpleVocabulary([
                SimpleTerm(0, "none",
                    title=_("no default", default=u"No default")),
                SimpleTerm(1, "almost-never",
                    title=_("frequency_almostnever", default=u"Almost never")),
                SimpleTerm(4, "regular",
                    title=_("frequency_regularly", default=u"Regularly")),
                SimpleTerm(7, "constant",
                    title=_("frequency_constantly", default=u"Constantly")),
            ]),
            required=False,
            default=0)

    depends("default_effect", "type", "==", "risk")
    depends("default_effect", "evaluation_method", "==", "calculated")
    default_effect = schema.Choice(
            title=_("label_default_severity", default=u"Default severity"),
            description=_("help_default_severity",
                default=u"Indicate the severity if this risk occurs."),
            vocabulary=SimpleVocabulary([
                SimpleTerm(0, "none",
                    title=_("no default", default=u"No default")),
                SimpleTerm(1, "weak",
                    title=_("effect_weak", default=u"Weak severity")),
                SimpleTerm(5, "significant",
                    title=_("effect_significant",
                        default=u"Significant severity")),
                SimpleTerm(10, "high",
                    title=_("effect_high",
                        default=u"High (very high) severity")),
            ]),
            required=False,
            default=0)


class IKinneyRisk(IRisk, IKinneyEvaluation):
    form.fieldset("evaluation",
            label=_("header_evaluation", default=u"Evaluation"),
            description=_("intro_evaluation",
                default=u"You can specify how the risks priority is "
                        u"evaluated. For more details see the online "
                        u"manual."),
            fields=["type", "risk_always_present", "evaluation_method",
                    "fixed_priority",
                    "default_priority",
                    "default_probability", "default_frequency",
                    "default_effect"])


class IFrenchRisk(IRisk, IFrenchEvaluation):
    form.fieldset("evaluation",
            label=_("header_evaluation", default=u"Evaluation"),
            description=_("intro_evaluation",
                default=u"You can specify how the risks priority is "
                        u"evaluated. For more details see the online "
                        u"manual."),
            fields=["type", "risk_always_present", "evaluation_method",
                    "fixed_priority",
                    "default_priority",
                    "default_severity", "default_frequency"])


class Risk(dexterity.Container):
    implements(IRisk)

    type = 'risk'

    default_probability = 0
    default_frequency = 0
    default_effect = 0
    default_severity = 0

    image = None
    caption = None
    image2 = None
    caption2 = None
    image3 = None
    caption3 = None
    image4 = None
    caption4 = None
    file1 = None
    file1_caption = None
    file2 = None
    file2_caption = None
    file3 = None
    file3_caption = None
    file4 = None
    file4_caption = None

    def _get_id(self, orig_id):
        """Pick an id for pasted content."""
        frame = sys._getframe(1)
        ob = frame.f_locals.get('ob')
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super(Risk, self)._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super(Risk, self)._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)

    def evaluation_algorithm(self):
        """Return the evaluation algorithm used by this risk. The
        algorithm is determined by the `evaluation_algorithm` flag
        for the parent :py:class:`euphorie.content.surveygroup.SurveyGroup`.
        """
        return evaluation_algorithm(self)

    @property
    def fixed_priority(self):
        priority = self.default_priority
        # 'none' is acceptable for default_priority, but not for fixed_priority,
        # so in that case default it to 'low'.
        if priority == 'none':
            return 'low'
        return priority

    @fixed_priority.setter
    def fixed_priority(self, value):
        self.default_priority = value

    @property
    @memoize
    def _solutions(self):
        solutions = []
        for item in self.objectValues():
            if ISolution.providedBy(item):
                solutions.append(item)
        return solutions

    def get_pre_defined_measures(self, request=None):
        """ Iterate over the Solution items on this risk.
        """
        from euphorie.client.interfaces import IItalyIdentificationPhaseSkinLayer   # noqa
        from euphorie.client.interfaces import IItalyReportPhaseSkinLayer
        measures = []
        for item in self._solutions:
            description = item.description and item.description.strip() or ""
            prevention_plan = (
                item.prevention_plan and item.prevention_plan.strip() or "")
            if (
                IItalyIdentificationPhaseSkinLayer.providedBy(request) or
                IItalyReportPhaseSkinLayer.providedBy(request)
            ):
                measures.append(
                    u"%s: %s" % (description, prevention_plan)
                )
            else:
                measures.append(description)
        return measures


def EnsureInterface(risk):
    """Make sure a risk has the correct interface set for, matching the
    evaluation method of the survey group.
    """
    algorithm = evaluation_algorithm(risk)
    if algorithm == u"french":
        alsoProvides(risk, IFrenchRisk)
        noLongerProvides(risk, IKinneyRisk)
    else:
        alsoProvides(risk, IKinneyRisk)
        noLongerProvides(risk, IFrenchRisk)


def evaluation_algorithm(context):
    """Return the evaluation algorithm used in a given context. The
    algorithm is determined by the `evaluation_algorithm` flag
    for the parent :py:class:`euphorie.content.surveygroup.SurveyGroup`.
    """
    from euphorie.content.surveygroup import ISurveyGroup  # XXX Circular
    for parent in aq_chain(aq_inner(context)):
        if IFrenchEvaluation.providedBy(parent):
            return u"french"
        elif IKinneyEvaluation.providedBy(parent):
            return u"kinney"
        if ISurveyGroup.providedBy(parent):
            return parent.evaluation_algorithm
    return u"kinney"


@indexer(IRisk)
def SearchableTextIndexer(obj):
    return " ".join([obj.title,
                     StripMarkup(obj.problem_description),
                     StripMarkup(obj.description),
                     StripMarkup(obj.legal_reference)])


class View(grok.View, DragDropHelper):
    grok.context(IRisk)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("risk_view")
    grok.name("nuplone-view")

    def update(self):
        super(View, self).update()
        context = aq_inner(self.context)
        self.module_title = aq_parent(context).title
        self.evaluation_algorithm = evaluation_algorithm(context)
        self.type = getTermTitleByValue(IRisk["type"], context.type)
        self.evaluation_method = getTermTitleByValue(
                IRisk["evaluation_method"], context.evaluation_method)
        self.default_priority = getTermTitleByValue(
                IKinneyRisk["default_priority"], context.default_priority)
        if self.evaluation_algorithm == u"french":
            self.default_severity = getTermTitleByValue(
                    IFrenchEvaluation["default_severity"],
                    context.default_severity)
            self.default_frequency = getTermTitleByValue(
                    IFrenchEvaluation["default_frequency"],
                    context.default_frequency)
        else:
            self.default_probability = getTermTitleByValue(
                    IKinneyEvaluation["default_probability"],
                    context.default_probability)
            self.default_frequency = getTermTitleByValue(
                    IKinneyEvaluation["default_frequency"],
                    context.default_frequency)
            self.default_effect = getTermTitleByValue(
                    IKinneyEvaluation["default_effect"],
                    context.default_effect)

        self.solutions = [{'id': solution.id,
                            'url': solution.absolute_url(),
                            'description': solution.description}
                           for solution in context.values()
                           if ISolution.providedBy(solution)]


class Add(dexterity.AddForm):
    grok.context(IRisk)
    grok.name("euphorie.risk")
    grok.require("euphorie.content.AddNewRIEContent")

    default_fieldset_label = None

    def __init__(self, context, request):
        from euphorie.content.survey import get_tool_type
        dexterity.AddForm.__init__(self, context, request)
        self.evaluation_algorithm = evaluation_algorithm(context)
        self.order = ['header_identification',
                 'header_evaluation',
                 'header_main_image',
                 'header_secondary_images',
                 'header_additional_content']

    @property
    def schema(self):
        if self.evaluation_algorithm == u"french":
            return IFrenchRisk
        else:
            return IKinneyRisk

    def updateFields(self):
        super(Add, self).updateFields()
        self.groups.sort(key=lambda g: self.order.index(g.label))

    def updateWidgets(self):
        super(Add, self).updateWidgets()
        self.widgets["title"].addClass("span-7")
        self.widgets["existing_measures"].mode = "hidden"

    def create(self, data):
        # This is mostly a direct copy of
        # :py:meth:`plone.dexterity.browser.add.DefaultAddForm.create`,
        # extended to apply the right interface.
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        content = createObject(fti.factory)
        alsoProvides(content, self.schema)
        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())
        if IAcquirer.providedBy(content):
            content = content.__of__(container)
        applyChanges(self, content, data)
        for group in self.groups:
            applyChanges(group, content, data)
        return aq_base(content)


class Edit(form.SchemaEditForm):
    grok.context(IRisk)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("edit")

    default_fieldset_label = None

    def __init__(self, context, request):
        from euphorie.content.survey import get_tool_type
        self.order = ['header_identification',
                      'header_evaluation',
                      'header_main_image',
                      'header_secondary_images',
                      'header_additional_content']
        self.evaluation_algorithm = context.evaluation_algorithm()
        if self.evaluation_algorithm == u"french":
            self.schema = IFrenchRisk
        else:
            self.schema = IKinneyRisk
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.use_existing_measures = settings.get('use_existing_measures', False)
        self.tool_type = get_tool_type(context)
        form.SchemaEditForm.__init__(self, context, request)

    def updateFields(self):
        super(Edit, self).updateFields()
        self.groups.sort(key=lambda g: self.order.index(g.label))

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        self.widgets["title"].addClass("span-7")
        tt = getUtility(IToolTypesInfo)
        if not (
            self.use_existing_measures and
            self.tool_type in tt.types_existing_measures
        ):
            self.widgets["existing_measures"].mode = "hidden"
        else:
            self.widgets["existing_measures"].mode = "display"

    def extractData(self, setErrors=True):
        data = super(Edit, self).extractData(setErrors)
        if data[0]['evaluation_method'] == 'fixed':
            del data[0]['default_priority']
        return data


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
        self.fti = fti
        self.container = container

    def checkForModules(self):
        """Check if the container already contains a module. If so refuse to
        allow creation of a risk.
        """
        for key in self.container:
            pt = self.container[key].portal_type
            if pt == "euphorie.module":
                return False
        else:
            return True

    def allowed(self):
        return self.checkForModules()
