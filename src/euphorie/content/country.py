"""
Country
-------

Is the container for sectors of that country, plus the country manager user
accounts.

https://admin.oiraproject.eu/sectors/eu
"""
from .. import MessageFactory as _
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ICountry(model.Schema, IBasic):
    """Country grouping in the online client."""

    country_type = schema.Choice(
        title=_("Country grouping"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("region", title=_("Region")),
                SimpleTerm("eu-member", title=_("EU member state")),
                SimpleTerm("efta", title=_("EFTA country")),
                SimpleTerm("candidate-eu", title=_("Candidate country")),
                SimpleTerm(
                    "potential-candidate-eu", title=_("Potential candidate country")
                ),
            ]
        ),
        default="eu-member",
        required=True,
    )

    directives.widget(risk_default_collapsible_sections=CheckBoxFieldWidget)
    risk_default_collapsible_sections = schema.List(
        title=_(
            "label__risk_default_collapsible_sections",
            "Expanded sections on risk page",
        ),
        description=_(
            "help__risk_default_collapsible_sections",
            "Define, which information sections should be open by "
            "default on a risk identification page. Sections not checked "
            "will be shown intially in collapsed mode, but the user can always "
            "open those sections with a click.",
        ),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary(
                [
                    SimpleTerm(
                        "collapsible_section_information", title=_("Information")
                    ),
                    SimpleTerm(
                        "collapsible_section_resources",
                        title=_("Resources: Legal references and attachments"),
                    ),
                    SimpleTerm("collapsible_section_comments", title=_("Comments")),
                ]
            )
        ),
        default=["collapsible_section_information"],
        required=False,
    )

    directives.widget(default_reports=CheckBoxFieldWidget)
    default_reports = schema.List(
        title=_("label__default_reports", "Available reports"),
        description=_(
            "help__default_reports",
            "Define, which reports are offered to the user on the Report page.",
        ),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary(
                [
                    SimpleTerm("report_full", title=_("Full report (Word document)")),
                    SimpleTerm(
                        "report_action_plan",
                        title=_("Action plan (Excel spreadsheet)"),
                    ),
                    SimpleTerm(
                        "report_overview_risks", title=_("Overview of risks (PDF)")
                    ),
                    SimpleTerm(
                        "report_overview_measures",
                        title=_("Overview of measures (PDF)"),
                    ),
                ]
            )
        ),
        default=["report_full", "report_action_plan", "report_overview_risks"],
        required=False,
    )

    enable_web_training = schema.Bool(
        title=_("label_enable_web_training", default="Enable Web Based Training?"),
        description=_(
            "help_enable_web_training_country",
            default="If this option is activated, an online training can be enabled on "
            "OiRA tools in this country.",
        ),
        required=False,
        default=True,
    )

    enable_consultancy = schema.Bool(
        title=_("label_enable_consultancy", default="Enable Consultancy?"),
        description=_(
            "help_enable_consultancy_country",
            default="If this option is activated, assessments can be reviewed and "
            "validated by consultants.",
        ),
        required=False,
        default=False,
    )


@implementer(ICountry)
class Country(Container):
    """A country folder."""

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False
