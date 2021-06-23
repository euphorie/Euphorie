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
                SimpleTerm(u"region", title=_("Region")),
                SimpleTerm(u"eu-member", title=_(u"EU member state")),
                SimpleTerm(u"efta", title=_(u"EFTA country")),
                SimpleTerm(u"candidate-eu", title=_(u"Candidate country")),
                SimpleTerm(
                    u"potential-candidate-eu", title=_(u"Potential candidate country")
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
            u"Expanded sections on risk page",
        ),
        description=_(
            "help__risk_default_collapsible_sections",
            u"Define, which information sections should be open by "
            u"default on a risk identification page. Sections not checked "
            u"will be shown intially in collapsed mode, but the user can always "
            u"open those sections with a click.",
        ),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary(
                [
                    SimpleTerm(
                        u"collapsible_section_information", title=_(u"Information")
                    ),
                    SimpleTerm(
                        u"collapsible_section_resources",
                        title=_(u"Resources: Legal references and attachments"),
                    ),
                    SimpleTerm(u"collapsible_section_comments", title=_(u"Comments")),
                ]
            )
        ),
        default=["collapsible_section_information"],
        required=False,
    )

    directives.widget(default_reports=CheckBoxFieldWidget)
    default_reports = schema.List(
        title=_("label__default_reports", u"Available reports"),
        description=_(
            "help__default_reports",
            u"Define, which reports are offered to the user on the Report page.",
        ),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary(
                [
                    SimpleTerm(u"report_full", title=_(u"Full report (Word document)")),
                    SimpleTerm(
                        u"report_action_plan",
                        title=_(u"Action plan (Excel spreadsheet)"),
                    ),
                    SimpleTerm(
                        u"report_overview_risks", title=_(u"Overview of risks (PDF)")
                    ),
                    SimpleTerm(
                        u"report_overview_measures",
                        title=_(u"Overview of measures (PDF)"),
                    ),
                ]
            )
        ),
        default=["report_full", "report_action_plan", "report_overview_risks"],
        required=False,
    )


@implementer(ICountry)
class Country(Container):
    """A country folder."""

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False
