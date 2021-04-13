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
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class CompanySchema(Schema):
    # Note the ideal type, but there is no convenient country field
    country = schema.TextLine(
        title=_("label_company_country", default=u"Your country"), required=False
    )

    employees = schema.Choice(
        title=_("label_employee_numbers", default=u"Number of employees"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    u"1-9",
                    title=_("employee_numbers_1_to_9", default=u"1 to 9 employees"),
                ),
                SimpleTerm(
                    u"10-49",
                    title=_("employee_numbers_10_to_49", default=u"10 to 49 employees"),
                ),
                SimpleTerm(
                    u"50-249",
                    title=_(
                        "employee_numbers_50_to_249", default=u"50 to 249 employees"
                    ),
                ),
                SimpleTerm(
                    u"250+",
                    title=_(
                        "employee_numbers_250_or_more", default=u"250 or more employees"
                    ),
                ),
            ]
        ),
        required=False,
    )

    conductor = schema.Choice(
        title=_("label_conductor", default=u"The risk assessment was conducted by"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(u"staff", title=_("conductor_staff", default=u"own staff")),
                SimpleTerm(
                    u"third-party",
                    title=_(
                        "conductor_third_party",
                        default=u"an external consultant or service provider",
                    ),
                ),
                SimpleTerm(
                    u"both",
                    title=_(
                        "conductor_both",
                        default=u"both own staff and an external consultant or "
                        u"service provider",
                    ),
                ),
            ]
        ),
        required=False,
    )

    referer = schema.Choice(
        title=_(
            "label_referer",
            default=u"Through which channel did you learn about this " u"tool?",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    u"employers-organisation",
                    title=_(
                        "referer_employers_organisation",
                        default=u"an employers' organisation",
                    ),
                ),
                SimpleTerm(
                    u"trade-union",
                    title=_(
                        "referer_trade_union", default=u"a trade union organisation"
                    ),
                ),
                SimpleTerm(
                    u"national-public-institution",
                    title=_(
                        "referer_national_public_institution",
                        default=u"a national public " u"institution/administration",
                    ),
                ),
                SimpleTerm(
                    u"eu-institution",
                    title=_(
                        "referer_eu_institution",
                        default=u"an European institution/administration",
                    ),
                ),
                SimpleTerm(
                    u"health-safety-experts",
                    title=_(
                        "referer_health_safety_expert",
                        default=u"health and safety experts",
                    ),
                ),
                SimpleTerm(
                    u"other", title=_("referer_other", default=u"other channel")
                ),
            ]
        ),
        required=False,
    )

    workers_participated = schema.Choice(
        title=_(
            "label_workers_participated",
            default=u"Workers were invited to participate in the " u"risk assessment",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(True, title=_("label_yes", default=u"Yes")),
                SimpleTerm(False, title=_("label_no", default=u"No")),
            ]
        ),
        required=False,
    )

    needs_met = schema.Choice(
        title=_("label_needs_met", default=u"Did this OiRA tool meet your needs?"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(True, title=_("label_yes", default=u"Yes")),
                SimpleTerm(False, title=_("label_no", default=u"No")),
            ]
        ),
        required=False,
    )

    recommend_tool = schema.Choice(
        title=_(
            "label_recommend_tool",
            default=u"Would you recommend this OiRA tool to an enterprise "
            u"similar to yours?",
        ),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(True, title=_("label_yes", default=u"Yes")),
                SimpleTerm(False, title=_("label_no", default=u"No")),
            ]
        ),
        required=False,
    )

    directives.mode(timestamp="hidden")
    timestamp = schema.Datetime(
        title=u"Timestamp",
        required=False,
    )


class Company(AutoExtensibleForm, form.Form):
    """Update the company details.

    View name: @@report_company
    """

    variation_class = "variation-risk-assessment"

    schema = CompanySchema
    company = None
    template = ViewPageTemplateFile("templates/report_company.pt")

    @property
    def session(self):
        return self.context.session

    def _assertCompany(self):
        if self.company is not None:
            return
        session = self.session
        if session.company is None:
            session.company = model.Company()
        directlyProvides(session.company, CompanySchema)
        self.company = session.company

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
        super(Company, self).update()
        self._assertCompany()

    def getContent(self):
        self._assertCompany()
        return self.company

    def applyChanges(self, data):
        content = self.getContent()
        applyChanges(self, content, data)

    @button.buttonAndHandler(u"Previous")
    def handlePrevious(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        data["timestamp"] = datetime.now()
        self.applyChanges(data)
        url = "%s/@@report" % self.context.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler(u"Next")
    def handleNext(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        data["timestamp"] = datetime.now()
        self.applyChanges(data)
        url = "%s/@@report_view" % self.context.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler(u"Skip")
    def handleSkip(self, action):
        # XXX: This a hack. We need to know if a company report has been
        # skipped but can't add new SQL columns. So we mark the country 'xx'.
        data = {
            "conductor": None,
            "country": u"xx",
            "employees": None,
            "referer": None,
            "workers_participated": None,
            "needs_met": None,
            "recommend_tool": None,
        }
        self.applyChanges(data)
        url = "%s/@@report_view" % self.context.absolute_url()
        self.request.response.redirect(url)
