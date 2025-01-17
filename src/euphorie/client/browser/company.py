"""
Company
-------

View and update the company survey.
"""

from .. import MessageFactory as _
from datetime import datetime
from euphorie.client import model
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize
from plone.supermodel.model import Schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import form
from z3c.form.form import applyChanges
from zope import schema
from zope.deprecation import deprecate
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class CompanySchema(Schema):
    # Note the ideal type, but there is no convenient country field
    country = schema.TextLine(
        title=_("label_company_country", default="Your country"), required=False
    )

    employees = schema.Choice(
        title=_("label_employee_numbers", default="Number of employees"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    "1-9",
                    title=_("employee_numbers_1_to_9", default="1 to 9 employees"),
                ),
                SimpleTerm(
                    "10-49",
                    title=_("employee_numbers_10_to_49", default="10 to 49 employees"),
                ),
                SimpleTerm(
                    "50-249",
                    title=_(
                        "employee_numbers_50_to_249", default="50 to 249 employees"
                    ),
                ),
                SimpleTerm(
                    "250+",
                    title=_(
                        "employee_numbers_250_or_more", default="250 or more employees"
                    ),
                ),
            ]
        ),
        required=False,
    )

    conductor = schema.Choice(
        title=_("label_conductor", default="The risk assessment was conducted by"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("staff", title=_("conductor_staff", default="own staff")),
                SimpleTerm(
                    "third-party",
                    title=_(
                        "conductor_third_party",
                        default="an external consultant or service provider",
                    ),
                ),
                SimpleTerm(
                    "both",
                    title=_(
                        "conductor_both",
                        default="both own staff and an external consultant or "
                        "service provider",
                    ),
                ),
            ]
        ),
        required=False,
    )

    referer = schema.Choice(
        title=_(
            "label_referer",
            default="Through which channel did you learn about this " "tool?",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    "employers-organisation",
                    title=_(
                        "referer_employers_organisation",
                        default="an employers' organisation",
                    ),
                ),
                SimpleTerm(
                    "trade-union",
                    title=_(
                        "referer_trade_union", default="a trade union organisation"
                    ),
                ),
                SimpleTerm(
                    "national-public-institution",
                    title=_(
                        "referer_national_public_institution",
                        default="a national public " "institution/administration",
                    ),
                ),
                SimpleTerm(
                    "eu-institution",
                    title=_(
                        "referer_eu_institution",
                        default="an European institution/administration",
                    ),
                ),
                SimpleTerm(
                    "health-safety-experts",
                    title=_(
                        "referer_health_safety_expert",
                        default="health and safety experts",
                    ),
                ),
                SimpleTerm("other", title=_("referer_other", default="other channel")),
            ]
        ),
        required=False,
    )

    workers_participated = schema.Choice(
        title=_(
            "label_workers_participated",
            default="Workers were invited to participate in the " "risk assessment",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(True, title=_("label_yes", default="Yes")),
                SimpleTerm(False, title=_("label_no", default="No")),
            ]
        ),
        required=False,
    )

    needs_met = schema.Choice(
        title=_("label_needs_met", default="Did this OiRA tool meet your needs?"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(True, title=_("label_yes", default="Yes")),
                SimpleTerm(False, title=_("label_no", default="No")),
            ]
        ),
        required=False,
    )

    recommend_tool = schema.Choice(
        title=_(
            "label_recommend_tool",
            default="Would you recommend this OiRA tool to an enterprise "
            "similar to yours?",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(True, title=_("label_yes", default="Yes")),
                SimpleTerm(False, title=_("label_no", default="No")),
            ]
        ),
        required=False,
    )

    directives.mode(timestamp="hidden")
    timestamp = schema.Datetime(
        title="Timestamp",
        required=False,
    )


class Company(AutoExtensibleForm, form.Form):
    """Update the company details.

    View name: @@report_company
    """

    variation_class = "variation-risk-assessment"

    schema = CompanySchema
    template = ViewPageTemplateFile("templates/report_company.pt")
    company_class = model.Company

    @property
    def session(self):
        return self.context.session

    @property
    def default_company_values(self):
        """The values we use to create a new company."""
        return {"session": self.session}

    @property
    @memoize
    def company(self):
        """Get or create the company object for this session."""
        company = (
            model.Session.query(self.company_class)
            .filter(self.company_class.session == self.session)
            .first()
        )
        if not company:
            company = self.company_class(**self.default_company_values)

        # This is used to make the company object the context of the form
        directlyProvides(company, self.schema)
        return company

    @deprecate(
        "Deprecated in version 15.2.1.dev0. "
        "This was a trick to add the company attribute to the instance. "
        "Now company is a property."
    )
    def _assertCompany(self):
        return

    def countries(self):
        names = [
            {"id": key.lower(), "title": value}
            for (key, value) in self.request.locale.displayNames.territories.items()
        ]
        names.sort(key=lambda c: c["title"])
        return names

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def update(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        super().update()
        self._assertCompany()

    def getContent(self):
        self._assertCompany()
        return self.company

    def applyChanges(self, data):
        content = self.getContent()
        applyChanges(self, content, data)

    @button.buttonAndHandler("Previous")
    def handlePrevious(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        data["timestamp"] = datetime.now()
        self.applyChanges(data)
        url = "%s/@@report" % self.context.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler("Next")
    def handleNext(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        data["timestamp"] = datetime.now()
        self.applyChanges(data)
        url = "%s/@@report_view" % self.context.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler("Skip")
    def handleSkip(self, action):
        # XXX: This a hack. We need to know if a company report has been
        # skipped but can't add new SQL columns. So we mark the country 'xx'.
        data = {
            "conductor": None,
            "country": "xx",
            "employees": None,
            "referer": None,
            "workers_participated": None,
            "needs_met": None,
            "recommend_tool": None,
        }
        self.applyChanges(data)
        url = "%s/@@report_view" % self.context.absolute_url()
        self.request.response.redirect(url)
