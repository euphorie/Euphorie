# coding=utf-8
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
from euphorie.content.utils import IToolTypesInfo
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
        if self.evaluation_algorithm == u"french":
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


class AddForm(DefaultAddForm):

    portal_type = "euphorie.risk"
    default_fieldset_label = None

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
        self.order = [
            "header_identification",
            "header_evaluation",
            "header_main_image",
            "header_secondary_images",
            "header_additional_content",
        ]

    @property
    @memoize
    def evaluation_algorithm(self):
        return evaluation_algorithm(aq_inner(self.context))

    @property
    def schema(self):
        if self.evaluation_algorithm == u"french":
            return IFrenchRisk
        else:
            return IKinneyRisk

    def updateFields(self):
        super(AddForm, self).updateFields()
        self.groups.sort(key=lambda g: self.order.index(g.label))

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
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


class EditForm(DefaultEditForm):

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
    def tool_type(self):
        return get_tool_type(self.my_context)

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.order = [
            "header_identification",
            "header_evaluation",
            "header_main_image",
            "header_secondary_images",
            "header_additional_content",
        ]

    def updateFields(self):
        super(EditForm, self).updateFields()
        self.groups.sort(key=lambda g: self.order.index(g.label))

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets["title"].addClass("span-7")
        tt = getUtility(IToolTypesInfo)
        if not (
            self.use_existing_measures and self.tool_type in tt.types_existing_measures
        ):
            self.widgets["existing_measures"].mode = "hidden"
        else:
            self.widgets["existing_measures"].mode = "display"

    def extractData(self, setErrors=True):
        data = super(EditForm, self).extractData(setErrors)
        if data[0]["evaluation_method"] == "fixed":
            del data[0]["default_priority"]

        # If there is a validation error on the form, consume all status messages,
        # so that they don't appear in the form. We only want to show validation
        # messages directly on the respective field(s) in that case.
        if data[1]:
            status = IStatusMessage(self.request)
            status.show()
        return data
