from ..risk import evaluation_algorithm
from ..risk import IFrenchEvaluation
from ..risk import IFrenchRisk
from ..risk import IKinneyEvaluation
from ..risk import IKinneyRisk
from ..risk import IRisk
from ..solution import ISolution
from ..utils import DragDropHelper
from ..utils import getTermTitleByValue
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition.interfaces import IAcquirer
from euphorie.content.survey import get_tool_type
from euphorie.content.utils import get_tool_type_default
from euphorie.content.utils import IToolTypesInfo
from euphorie.content.utils import parse_scaled_answers
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize.instance import memoize
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.form import applyChanges
from zope.component import createObject
from zope.component import getUtility
from zope.interface import alsoProvides


class RiskView(BrowserView, DragDropHelper):
    @property
    @memoize
    def my_context(self):
        return aq_inner(self.context)

    @property
    def module_title(self):
        return aq_parent(self.context).title

    @property
    def evaluation_algorithm(self):
        return evaluation_algorithm(self.my_context)

    @property
    def risk_type(self):
        return getTermTitleByValue(IRisk["type"], self.my_context.type)

    @property
    def tool_type_data(self) -> dict:
        """There is an utility that provides the tool types information.

        The information are stored in a dictionary with the tool type as key.

        The default utility return the dict `euphorie.content.utils.TOOL_TYPES`.

        This is not directly used by this package, but custom code will use this.
        """
        tool_types_info = getUtility(IToolTypesInfo)()
        tool_type = get_tool_type(self.my_context)
        try:
            return tool_types_info[tool_type]
        except KeyError:
            return tool_types_info[get_tool_type_default()]

    @property
    def solutions(self):
        return [
            {
                "id": solution.id,
                "url": solution.absolute_url(),
                "description": solution.description,
            }
            for solution in self.my_context.values()
            if ISolution.providedBy(solution)
        ]

    @property
    def evaluation_method(self):
        return getTermTitleByValue(
            IRisk["evaluation_method"], self.my_context.evaluation_method
        )

    @property
    def default_priority(self):
        return getTermTitleByValue(
            IKinneyRisk["default_priority"], self.my_context.default_priority
        )

    @property
    def default_severity(self):
        return getTermTitleByValue(
            IFrenchEvaluation["default_severity"], self.my_context.default_severity
        )

    @property
    def default_frequency(self):
        if self.evaluation_algorithm == "french":
            return getTermTitleByValue(
                IFrenchEvaluation["default_frequency"],
                self.my_context.default_frequency,
            )
        else:
            return getTermTitleByValue(
                IKinneyEvaluation["default_frequency"],
                self.my_context.default_frequency,
            )

    @property
    def default_probability(self):
        return getTermTitleByValue(
            IKinneyEvaluation["default_probability"],
            self.my_context.default_probability,
        )

    @property
    def default_effect(self):
        return getTermTitleByValue(
            IKinneyEvaluation["default_effect"], self.my_context.default_effect
        )

    @property
    @memoize
    def portal_transforms(self):
        return api.portal.get_tool("portal_transforms")

    def get_safe_html(self, text):
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()

    @property
    @memoize
    def scaled_answers(self):
        """Get values and answers if the scaled_answers field is used.

        This returns a list of dictionaries.
        """
        context = self.my_context
        if not getattr(context, "use_scaled_answer", False):
            return []
        return parse_scaled_answers(context.scaled_answers)


class RiskFieldsetOrderingMixin:

    order = [
        "header_identification",
        "header_evaluation",
        "header_main_image",
        "header_secondary_images",
        "header_additional_content",
    ]

    def updateFields(self):
        """
        Override the parent method to sort fieldsets based on the predefined order.

        The method uses the `order` attribute to determine the position of each
        fieldset. If a fieldset's label is not found in the `order` list, it is
        placed at the end. Sorting is performed in-place on the `self.groups` list.
        """
        super().updateFields()

        def index_of_group(group):
            try:
                return self.order.index(group.label)
            except ValueError:
                return len(self.order)

        self.groups.sort(key=index_of_group)


class AddForm(RiskFieldsetOrderingMixin, DefaultAddForm):
    portal_type = "euphorie.risk"
    default_fieldset_label = None

    @property
    @memoize
    def evaluation_algorithm(self):
        return evaluation_algorithm(aq_inner(self.context))

    @property
    def schema(self):
        if self.evaluation_algorithm == "french":
            return IFrenchRisk
        else:
            return IKinneyRisk

    def updateWidgets(self):
        super().updateWidgets()
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
        if hasattr(content, "_setPortalTypeName"):
            content._setPortalTypeName(fti.getId())
        if IAcquirer.providedBy(content):
            content = content.__of__(container)
        applyChanges(self, content, data)
        for group in self.groups:
            applyChanges(group, content, data)
        return aq_base(content)


class AddView(DefaultAddView):
    form = AddForm


class EditForm(RiskFieldsetOrderingMixin, DefaultEditForm):
    portal_type = "euphorie.risk"
    default_fieldset_label = None

    @property
    @memoize
    def my_context(self):
        return aq_inner(self.context)

    @property
    @memoize
    def evaluation_algorithm(self):
        return self.my_context.evaluation_algorithm()

    @property
    def schema(self):
        if self.evaluation_algorithm == "french":
            return IFrenchRisk
        else:
            return IKinneyRisk

    @property
    def use_existing_measures(self):
        return api.portal.get_registry_record(
            "euphorie.use_existing_measures", default=False
        )

    @property
    @memoize
    def portal_transforms(self):
        return api.portal.get_tool("portal_transforms")

    def get_safe_html(self, text):
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()

    @property
    def tool_type(self):
        return get_tool_type(self.my_context)

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["title"].addClass("span-7")
        tt = getUtility(IToolTypesInfo)
        if not (
            self.use_existing_measures and self.tool_type in tt.types_existing_measures
        ):
            self.widgets["existing_measures"].mode = "hidden"
        else:
            self.widgets["existing_measures"].mode = "display"
        for fname in ("description", "legal_reference"):
            value = self.widgets[fname].value or ""
            safe_value = self.get_safe_html(value)
            if value != safe_value:
                self.widgets[fname].value = safe_value

    def extractData(self, setErrors=True):
        data = super().extractData(setErrors)
        if data[0]["evaluation_method"] == "fixed":
            del data[0]["default_priority"]

        # If there is a validation error on the form, consume all status messages,
        # so that they don't appear in the form. We only want to show validation
        # messages directly on the respective field(s) in that case.
        if data[1]:
            status = IStatusMessage(self.request)
            status.show()
        return data
