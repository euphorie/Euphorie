"""
Company
-------

View and update the company survey.
"""

from five import grok
from zope import schema
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from z3c.form import button
from z3c.form.form import applyChanges
from plone.directives import form
from .. import MessageFactory as _
from ..ghost import PathGhost
from euphorie.client import model
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client.session import SessionManager

grok.templatedir("templates")


class CompanySchema(form.Schema):
    # Note the ideal type, but there is no convenient country field
    country = schema.TextLine(
            title=_("label_company_country", default=u"Your country"),
            required=False)

    employees = schema.Choice(
            title=_("label_employee_numbers", default=u"Number of employees"),
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"1-9", title=_("employee_numbers_1_to_9",
                    default=u"1 to 9 employees")),
                SimpleTerm(u"10-49", title=_("employee_numbers_10_to_49",
                    default=u"10 to 49 employees")),
                SimpleTerm(u"50-249", title=_("employee_numbers_50_to_249",
                    default=u"50 to 249 employees")),
                SimpleTerm(u"250+", title=_("employee_numbers_250_or_more",
                    default=u"250 or more employees")),
                ]),
            required=False)

    conductor = schema.Choice(
            title=_("label_conductor",
                default=u"The risk assessment was conducted by"),
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"staff", title=_("conductor_staff",
                    default=u"own staff")),
                SimpleTerm(u"third-party", title=_("conductor_third_party",
                    default=u"an external consultant or service provider")),
                SimpleTerm(u"both", title=_("conductor_both",
                    default=u"both own staff and an external consultant or "
                            u"service provider")),
                ]),
            required=False)

    referer = schema.Choice(
            title=_("label_referer",
                default=u"Through which channel did you learn about this "
                        u"tool?"),
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"employers-organisation",
                    title=_("referer_employers_organisation",
                        default=u"an employers' organisation")),
                SimpleTerm(u"trade-union",
                    title=_("referer_trade_union",
                        default=u"a trade union organisation")),
                SimpleTerm(u"national-public-institution",
                    title=_("referer_national_public_institution",
                        default=u"a national public "
                                u"institution/administration")),
                SimpleTerm(u"eu-institution",
                    title=_("referer_eu_institution",
                        default=u"an European institution/administration")),
                SimpleTerm(u"health-safety-experts",
                    title=_("referer_health_safety_expert",
                        default=u"health and safety experts")),
                SimpleTerm(u"other",
                    title=_("referer_other",
                        default=u"other channel")),
                    ]),
            required=False)

    workers_participated = schema.Choice(
            title=_("label_workers_participated",
                default=u"Workers were invited to participate in the "
                        u"risk assessment"),
            vocabulary=SimpleVocabulary([
                SimpleTerm(True, title=_("label_yes", default=u"Yes")),
                SimpleTerm(False, title=_("label_no", default=u"No")),
            ]),
            required=False)

    needs_met = schema.Choice(
        title=_(
            "label_needs_met",
            default=u"Did this OiRA tool meet your needs?"),
        vocabulary=SimpleVocabulary([
            SimpleTerm(True, title=_("label_yes", default=u"Yes")),
            SimpleTerm(False, title=_("label_no", default=u"No")),
        ]),
        required=False
    )

    recommend_tool = schema.Choice(
        title=_(
            "label_recommend_tool",
            default=u"Would you recommend this OiRA tool to an enterprise "
            u"similar to yours?"),
        vocabulary=SimpleVocabulary([
            SimpleTerm(True, title=_("label_yes", default=u"Yes")),
            SimpleTerm(False, title=_("label_no", default=u"No")),
        ]),
        required=False
    )


class Company(form.SchemaForm):
    """Update the company details.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a `PathGhost` object for
    the *inventory* component of the URL.

    View name: @@company
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.template("report_company")
    grok.name("company")

    schema = CompanySchema
    company = None

    def _assertCompany(self):
        if self.company is not None:
            return
        session = SessionManager.session
        if session.company is None:
            session.company = model.Company()
        directlyProvides(session.company, CompanySchema)
        self.company = session.company

    def countries(self):
        names = [{'id': key.lower(), 'title': value}
                 for (key, value) in
                 self.request.locale.displayNames.territories.items()]
        names.sort(key=lambda c: c["title"])
        return names

    def update(self):
        super(Company, self).update()
        self.session = SessionManager.session
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
        self.applyChanges(data)
        url = "%s/report" % self.request.survey.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler(u"Next")
    def handleNext(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        url = "%s/report/view" % self.request.survey.absolute_url()
        self.request.response.redirect(url)
