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
from .utils import StripMarkup
from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.content.utils import ensure_image_size
from euphorie.htmllaundry.z3cform import HtmlText
from plone import api
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.namedfile import field as filefield
from plone.namedfile.interfaces import INamedBlobImageField
from plone.supermodel import model
from plonetheme.nuplone.z3cform.directives import depends
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from plonetheme.nuplone.z3cform.widget import WysiwygFieldWidget
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import validator
from zope import schema
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import noLongerProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import sys


TextLines4Rows = FieldWidgetFactory(
    "z3c.form.browser.textlines.TextLinesFieldWidget", rows=4
)


class TextLinesWithBreaks(schema.TextLine):
    def constraint(self, value):
        return True


TextLines8Rows = FieldWidgetFactory(
    "z3c.form.browser.textlines.TextLinesFieldWidget", rows=8
)


class IRisk(model.Schema, IRichDescription, IBasic):
    """A possible risk that can be present in an organisation."""

    title = schema.TextLine(
        title=_("label_statement", default="Affirmative statement"),
        description=_(
            "help_statement",
            default="This is a short affirmative statement about a "
            "possible risk (e.g. The building is well maintained.)",
        ),
        required=True,
    )
    directives.widget(title="euphorie.content.risk.TextLines4Rows")
    directives.order_before(title="*")

    problem_description = schema.TextLine(
        title=_("label_problem_description", default="Negative statement"),
        description=_(
            "help_problem_description",
            default="This is the inverse of the affirmative "
            "statement (e.g. The building is not well maintained.)",
        ),
        required=True,
    )
    directives.widget(problem_description="euphorie.content.risk.TextLines4Rows")
    directives.order_after(problem_description="title")

    description = HtmlText(
        title=_("label_description", default="Description"),
        description=_(
            "help_risk_description",
            default="Describe the risk. Include any relevant information "
            "that may be helpful for the end-user.",
        ),
        required=True,
    )
    directives.widget(description=WysiwygFieldWidget)
    directives.order_after(description="problem_description")

    existing_measures = TextLinesWithBreaks(
        title=_(
            "deprecated_label_existing_measures",
            default="Measures that are already in place (Only shown here for "
            "reference! Use the “Add Measure” button on the Risk for adding "
            "measures that are shown to the user during Identification.)",
        ),
        description=_(
            "help_existing_measures",
            default="Use this field to define (common) measures that the "
            "user might have already implemented. "
            "Separate measures with a line break (Enter). The user will be "
            "able to deselect those measures that are not applicable to their"
            "situation.",
        ),
        required=False,
    )
    directives.widget(existing_measures="euphorie.content.risk.TextLines8Rows")
    directives.order_after(existing_measures="description")

    legal_reference = HtmlText(
        title=_("label_legal_reference", default="Legal and policy references"),
        required=False,
    )
    directives.widget(legal_reference=WysiwygFieldWidget)
    directives.order_after(legal_reference="description")

    model.fieldset(
        "identification",
        label=_("header_identification", default="Identification"),
        fields=["show_notapplicable"],
    )

    show_notapplicable = schema.Bool(
        title=_("label_show_notapplicable", default="Show `not applicable' option"),
        description=_(
            "help_show_notapplicable",
            default="Offer a `not applicable' option in addition "
            "to the standard yes/no options.",
        ),
        default=False,
    )

    type = schema.Choice(
        title=_("label_risk_type", default="Risk type"),
        description=_(
            "help_risk_type",
            default='"Priority risk" is one of the high risks in the '
            'sector. "Risk" is related to the workplace or to the work '
            'carried out. "Policy" refers to agreements, procedures, '
            "and management decisions.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("top5", title=_("risktype_top5", default="Priority risk")),
                SimpleTerm("risk", title=_("risktype_risk", default="Risk")),
                SimpleTerm("policy", title=_("risktype_policy", default="Policy")),
            ]
        ),
        default="risk",
        required=True,
    )

    depends("risk_always_present", "type", "==", "risk")
    risk_always_present = schema.Bool(
        title=_("label_risk_always_present", default="Risk is always present"),
        description=_(
            "description_risk_always_present",
            default='If selected, the user will not be able to answer "Yes" or '
            '"No", since the risk is considered to be always present. The '
            "Evaluation and Action Plan will behave in the same way as for "
            "regular risks.",
        ),
        required=False,
        default=False,
    )

    depends("evaluation_method", "type", "==", "risk")
    evaluation_method = schema.Choice(
        title=_("label_evaluation_method", default="Evaluation method"),
        description=_(
            "help_evaluation_method",
            default="Select 'estimated' if calcuation is not necessary "
            "or not possible.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("direct", title=_("evalmethod_direct", default="Estimated")),
                SimpleTerm(
                    "calculated",
                    title=_("evalmethod_calculated", default="Calculated"),
                ),
                SimpleTerm(
                    "fixed", title=_("evalmethod_fixed", default="Skip evaluation")
                ),
            ]
        ),
        default="calculated",
        required=False,
    )

    depends("fixed_priority", "type", "==", "risk")
    depends("fixed_priority", "evaluation_method", "==", "fixed")
    fixed_priority = schema.Choice(
        title=_("report_timeline_priority", default="Priority"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("low", title=_("priority_low", default="Low")),
                SimpleTerm("medium", title=_("priority_medium", default="Medium")),
                SimpleTerm("high", title=_("priority_high", default="High")),
            ]
        ),
        required=False,
        default="low",
    )

    depends("default_priority", "type", "==", "risk")
    depends("default_priority", "evaluation_method", "==", "direct")
    default_priority = schema.Choice(
        title=_("label_default_priority", default="Default priority"),
        description=_(
            "help_default_priority",
            default="You can help the end-user by selecting a default "
            "priority. He/she can still change the priority.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("none", title=_("no_default", default="No default")),
                SimpleTerm("low", title=_("priority_low", default="Low")),
                SimpleTerm("medium", title=_("priority_medium", default="Medium")),
                SimpleTerm("high", title=_("priority_high", default="High")),
            ]
        ),
        required=False,
        default="low",
    )

    model.fieldset(
        "main_image",
        label=_("header_main_image", default="Main image"),
        description=_(
            "intro_main_image",
            default="The main image will get a more prominent position "
            "in the client than the other images.",
        ),
        fields=["image", "caption"],
    )

    image = filefield.NamedBlobImage(
        title=_("label_image", default="Image file"),
        description=_(
            "help_image_upload",
            default="Upload an image. Make sure your image is of format "
            "png, jpg or gif and does not contain any special "
            "characters. The minimum size is 1000 (width) x 430 (height) pixels.",
        ),
        required=False,
    )
    caption = schema.TextLine(
        title=_("label_caption", default="Image caption"), required=False
    )

    model.fieldset(
        "secondary_images",
        label=_("header_secondary_images", default="Secondary images"),
        fields=["image2", "caption2", "image3", "caption3", "image4", "caption4"],
    )

    image2 = filefield.NamedBlobImage(
        title=_("label_image", default="Image file"),
        description=_(
            "help_image_upload",
            default="Upload an image. Make sure your image is of format "
            "png, jpg or gif and does not contain any special "
            "characters. The minimum size is 1000 (width) x 430 (height) pixels.",
        ),
        required=False,
    )
    caption2 = schema.TextLine(
        title=_("label_caption", default="Image caption"), required=False
    )

    image3 = filefield.NamedBlobImage(
        title=_("label_image", default="Image file"),
        description=_(
            "help_image_upload",
            default="Upload an image. Make sure your image is of format "
            "png, jpg or gif and does not contain any special "
            "characters. The minimum size is 1000 (width) x 430 (height) pixels.",
        ),
        required=False,
    )
    caption3 = schema.TextLine(
        title=_("label_caption", default="Image caption"), required=False
    )

    image4 = filefield.NamedBlobImage(
        title=_("label_image", default="Image file"),
        description=_(
            "help_image_upload",
            default="Upload an image. Make sure your image is of format "
            "png, jpg or gif and does not contain any special "
            "characters. The minimum size is 1000 (width) x 430 (height) pixels.",
        ),
        required=False,
    )
    caption4 = schema.TextLine(
        title=_("label_caption", default="Image caption"), required=False
    )

    model.fieldset(
        "additional_content",
        label=_("header_additional_content", default="Additional content"),
        description=_(
            "intro_additional_content",
            default="Attach any additional content you consider helpful "
            "for the user",
        ),
        fields=[
            "file1",
            "file1_caption",
            "file2",
            "file2_caption",
            "file3",
            "file3_caption",
            "file4",
            "file4_caption",
        ],
    )

    file1 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file1_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )

    file2 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file2_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )

    file3 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file3_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )

    file4 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file4_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )


class ImageSizeValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        try:
            previous_value = self.field.get(self.context)
        except AttributeError:
            previous_value = None
        if previous_value == value:
            try:
                ensure_image_size(value)
            except Invalid as invalid:
                IStatusMessage(self.context.REQUEST).add(invalid, "warn")
        else:
            ensure_image_size(value)


validator.WidgetValidatorDiscriminators(
    ImageSizeValidator, context=IRisk, field=INamedBlobImageField
)


class IFrenchEvaluation(model.Schema):
    depends("default_severity", "type", "==", "risk")
    depends("default_severity", "evaluation_method", "==", "calculated")
    default_severity = schema.Choice(
        title=_("label_default_severity", default="Default severity"),
        description=_(
            "help_default_severity",
            default="Indicate the severity if this risk occurs.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(0, "none", title=_("no default", default="No default")),
                SimpleTerm(1, "weak", title=_("severity_weak", default="Weak")),
                SimpleTerm(
                    5,
                    "not-severe",
                    title=_("severity_not_severe", default="Not very severe"),
                ),
                SimpleTerm(7, "severe", title=_("severity_severe", default="Severe")),
                SimpleTerm(
                    10,
                    "very-severe",
                    title=_("severity_very_severe", default="Very severe"),
                ),
            ]
        ),
        required=True,
        default=0,
    )

    depends("default_frequency", "type", "==", "risk")
    depends("default_frequency", "evaluation_method", "==", "calculated")
    default_frequency = schema.Choice(
        title=_("label_default_frequency", default="Default frequency"),
        description=_(
            "help_default_frequency",
            default="Indicate how often this risk occurs in a " "normal situation.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(0, "none", title=_("no default", default="No default")),
                SimpleTerm(1, "rare", title=_("frequency_french_rare", default="Rare")),
                SimpleTerm(
                    3,
                    "not-often",
                    title=_("frequency_french_not_often", default="Not very often"),
                ),
                SimpleTerm(
                    7, "often", title=_("frequency_french_often", default="Often")
                ),
                SimpleTerm(
                    9,
                    "regularly",
                    title=_(
                        "frequency_french_regularly", default="Very often or regularly"
                    ),
                ),
            ]
        ),
        required=True,
        default=0,
    )


class IKinneyEvaluation(model.Schema):
    depends("default_probability", "type", "==", "risk")
    depends("default_probability", "evaluation_method", "==", "calculated")
    default_probability = schema.Choice(
        title=_("label_default_probability", default="Default probability"),
        description=_(
            "help_default_probability",
            default="Indicate how likely occurence of this risk "
            "is in a normal situation.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(0, "none", title=_("no default", default="No default")),
                SimpleTerm(1, "small", title=_("probability_small", default="Small")),
                SimpleTerm(
                    3, "medium", title=_("probability_medium", default="Medium")
                ),
                SimpleTerm(5, "large", title=_("probability_large", default="Large")),
            ]
        ),
        required=False,
        default=0,
    )

    depends("default_frequency", "type", "==", "risk")
    depends("default_frequency", "evaluation_method", "==", "calculated")
    default_frequency = schema.Choice(
        title=_("label_default_frequency", default="Default frequency"),
        description=_(
            "help_default_frequency",
            default="Indicate how often this risk occurs in a " "normal situation.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(0, "none", title=_("no default", default="No default")),
                SimpleTerm(
                    1,
                    "almost-never",
                    title=_("frequency_almostnever", default="Almost never"),
                ),
                SimpleTerm(
                    4, "regular", title=_("frequency_regularly", default="Regularly")
                ),
                SimpleTerm(
                    7,
                    "constant",
                    title=_("frequency_constantly", default="Constantly"),
                ),
            ]
        ),
        required=False,
        default=0,
    )

    depends("default_effect", "type", "==", "risk")
    depends("default_effect", "evaluation_method", "==", "calculated")
    default_effect = schema.Choice(
        title=_("label_default_severity", default="Default severity"),
        description=_(
            "help_default_severity",
            default="Indicate the severity if this risk occurs.",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(0, "none", title=_("no default", default="No default")),
                SimpleTerm(1, "weak", title=_("effect_weak", default="Weak severity")),
                SimpleTerm(
                    5,
                    "significant",
                    title=_("effect_significant", default="Significant severity"),
                ),
                SimpleTerm(
                    10,
                    "high",
                    title=_("effect_high", default="High (very high) severity"),
                ),
            ]
        ),
        required=False,
        default=0,
    )


class IKinneyRisk(IRisk, IKinneyEvaluation):
    model.fieldset(
        "evaluation",
        label=_("header_evaluation", default="Evaluation"),
        description=_(
            "intro_evaluation",
            default="You can specify how the risks priority is "
            "evaluated. For more details see the online "
            "manual.",
        ),
        fields=[
            "type",
            "risk_always_present",
            "evaluation_method",
            "fixed_priority",
            "default_priority",
            "default_probability",
            "default_frequency",
            "default_effect",
        ],
    )


class IFrenchRisk(IRisk, IFrenchEvaluation):
    model.fieldset(
        "evaluation",
        label=_("header_evaluation", default="Evaluation"),
        description=_(
            "intro_evaluation",
            default="You can specify how the risks priority is "
            "evaluated. For more details see the online "
            "manual.",
        ),
        fields=[
            "type",
            "risk_always_present",
            "evaluation_method",
            "fixed_priority",
            "default_priority",
            "default_severity",
            "default_frequency",
        ],
    )


@implementer(IRisk)
class Risk(Container):
    type = "risk"

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
        ob = frame.f_locals.get("ob")
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super()._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super()._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)

    def evaluation_algorithm(self):
        """Return the evaluation algorithm used by this risk.

        The
        algorithm is determined by the `evaluation_algorithm` flag
        for the parent :py:class:`euphorie.content.surveygroup.SurveyGroup`.
        """
        return evaluation_algorithm(self)

    @property
    def fixed_priority(self):
        priority = self.default_priority
        # 'none' is acceptable for default_priority, but not for fixed_priority,
        # so in that case default it to 'low'.
        if priority == "none":
            return "low"
        return priority

    @fixed_priority.setter
    def fixed_priority(self, value):
        self.default_priority = value

    @property
    def _solutions(self):
        solutions = []
        for item in self.objectValues():
            if ISolution.providedBy(item):
                solutions.append(item)
        return solutions

    def get_pre_defined_measures(self, request=None):
        """Iterate over the Solution items on this risk."""
        measures = []
        webhelpers = api.content.get_view("webhelpers", self, request)
        for item in self._solutions:
            description = item.description and item.description.strip() or ""
            prevention_plan = (
                item.prevention_plan and item.prevention_plan.strip() or ""
            )
            measure = description
            if webhelpers.country in ("it",):
                if prevention_plan:
                    measure = f"{measure}: {prevention_plan}"
            measures.append(measure)

        return measures


def EnsureInterface(risk):
    """Make sure a risk has the correct interface set for, matching the
    evaluation method of the survey group."""
    algorithm = evaluation_algorithm(risk)
    if algorithm == "french":
        alsoProvides(risk, IFrenchRisk)
        noLongerProvides(risk, IKinneyRisk)
    else:
        alsoProvides(risk, IKinneyRisk)
        noLongerProvides(risk, IFrenchRisk)


def evaluation_algorithm(context):
    """Return the evaluation algorithm used in a given context.

    The
    algorithm is determined by the `evaluation_algorithm` flag
    for the parent :py:class:`euphorie.content.surveygroup.SurveyGroup`.
    """
    from euphorie.content.surveygroup import ISurveyGroup  # XXX Circular

    for parent in aq_chain(aq_inner(context)):
        if ISurveyGroup.providedBy(parent):
            return parent.evaluation_algorithm
    return "kinney"


@indexer(IRisk)
def SearchableTextIndexer(obj):
    return " ".join(
        [
            obj.title,
            StripMarkup(obj.problem_description),
            StripMarkup(obj.description),
            StripMarkup(obj.legal_reference),
        ]
    )


@adapter(ConditionalDexterityFTI, Interface)
@implementer(IConstructionFilter)
class ConstructionFilter:
    """FTI construction filter for :py:class:`Risk` objects. This filter
    prevents creating of modules if the current container already contains a
    module.

    This multi adapter requires the use of the conditional FTI as implemented
    by :py:class:`euphorie.content.fti.ConditionalDexterityFTI`.
    """

    def __init__(self, fti, container):
        self.fti = fti
        self.container = container

    def checkForModules(self):
        """Check if the container already contains a module.

        If so refuse to allow creation of a risk.
        """
        for key in self.container:
            pt = self.container[key].portal_type
            if pt == "euphorie.module":
                return False
        else:
            return True

    def allowed(self):
        return self.checkForModules()


def handle_risk_pasted(risk, event):
    EnsureInterface(risk)
