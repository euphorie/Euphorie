# coding=utf-8
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from euphorie import MessageFactory as _
from euphorie.client import config
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import ACTION_PLAN_FILTER
from euphorie.client.model import ActionPlan
from euphorie.client.model import get_current_account
from euphorie.client.model import Module
from euphorie.client.model import MODULE_WITH_RISK_OR_TOP5_FILTER
from euphorie.client.model import Risk
from euphorie.client.model import RISK_PRESENT_OR_TOP5_FILTER
from euphorie.client.model import SKIPPED_PARENTS
from euphorie.client.model import SurveyTreeItem
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.profile import extractProfile
from euphorie.client.survey import _StatusHelper
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.supermodel import model
from Products.CMFPlone import PloneLocalesMessageFactory
from Products.Five import BrowserView
from sqlalchemy import sql
from z3c.appconfig.interfaces import IAppConfig
from z3c.form.form import EditForm
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope import schema
from zope.component import getUtility
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent

import re
import urllib


class IStartFormSchema(model.Schema):
    title = schema.TextLine(
        title=_(
            "label_session_title", default=u"Enter a title for your Risk Assessment"
        ),
        required=True,
    )


class SurveySessionsView(SessionsView):
    """ Template corresponds to proto:_layout/tool.html
    """

    variation_class = ""

    @memoize
    def get_sessions(self):
        """ Filter user's sessions to match only those from the current survey
        """
        sessions = super(SurveySessionsView, self).get_sessions()
        survey = aq_inner(self.context)
        my_path = utils.RelativePath(self.request.client, survey)
        my_sessions = sorted(
            [x for x in sessions if x.zodb_path == my_path],
            key=lambda s: s.modified,
            reverse=True,
        )
        return my_sessions


class Start(AutoExtensibleForm, EditForm):
    """Survey start screen.

    This view shows basic introduction text and any extra information provided
    the sector if present. After viewing this page the user is forwarded to the
    profile page.

    View name: @@start
    """

    ignoreContext = True
    schema = IStartFormSchema
    variation_class = "variation-risk-assessment"

    @property
    def template(self):
        return self.index

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def survey(self):
        """ This is the survey dexterity object
        """
        return self.context.aq_parent

    @property
    @memoize
    def session(self):
        return self.context.session

    @property
    @memoize
    def can_view_session(self):
        account = self.webhelpers.get_current_account()
        if not account:
            return False
        session = self.session
        return session in account.sessions or session in account.acquired_sessions

    @property
    @memoize
    def can_edit_session(self):
        return self.can_view_session

    @property
    @memoize
    def can_publish_session(self):
        return self.can_edit_session

    @property
    @memoize
    def can_delete_session(self):
        return self.can_edit_session

    def is_new_session(self):
        if self.request.get("new_session"):
            return True
        return self.session.children().count() == 0

    @property
    @memoize
    def has_profile(self):
        return len(self.survey.ProfileQuestions())

    @memoize
    def has_introduction(self):
        survey = aq_inner(self.context)
        return utils.HasText(getattr(survey, "introduction", None))

    def update(self):
        super(Start, self).update()
        lang = getattr(self.request, "LANGUAGE", "en")
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.message_required = translate(
            _(u"message_field_required", default=u"Please fill out this field."),
            target_language=lang,
        )
        if self.request.environ["REQUEST_METHOD"] != "POST":
            return
        data, errors = self.extractData()
        if errors:
            return
        session = self.session
        changed = False
        for key in data:
            value = data[key]
            if getattr(session, key, None) != value:
                changed = True
                setattr(session, key, value)

        if changed:
            api.portal.show_message(
                _("Session data successfully updated"),
                request=self.request,
                type="success",
            )
        # Optimize: if the form was auto-submitted, we know that we want to
        # show the "start" page again
        if "form.button.submit" not in self.request:
            return
        self.request.response.redirect("%s/@@profile" % self.context.absolute_url())


class Profile(AutoExtensibleForm, EditForm):
    """Determine the profile for the current survey and build the session tree.

    All profile questions in the survey are shown to the user in one screen.
    The user can then determine the profile for his organisation. If there
    are no profile questions user is directly forwarded to the inventory
    phase.

    This view assumes there already is an active session for the current
    survey.
    """

    id_patt = re.compile("pq([0-9]*)\.present")
    variation_class = "variation-risk-assessment"
    next_view_name = "@@identification"

    @property
    def template(self):
        return self.index

    def getDesiredProfile(self):
        """Get the requested profile from the request.

        The profile is returned as a dictionary. The id of the profile
        questions are used as keys. For optional profile questions the value is
        a boolean.  For repetable profile questions the value is a list of
        titles as provided by the user. This format is compatible with
        :py:func:`extractProfile`.

        :rtype: dictionary with profile answers
        """
        profile = {}
        for (id, answer) in self.request.form.items():
            match = self.id_patt.match(id)
            if match:
                id = match.group(1)
            question = self.context.get(id)
            if not IProfileQuestion.providedBy(question):
                continue
            if getattr(question, "use_location_question", True):
                # Ignore questions found via the id pattern if they profile
                # is repeatable
                if match:
                    continue
                if not self.request.form.get("pq{0}.present".format(id), "") == "yes":
                    continue
                if isinstance(answer, list):
                    profile[id] = filter(None, (a.strip() for a in answer))
                    if (
                        not self.request.form.get("pq{0}.multiple".format(id), "")
                        == "yes"
                    ):
                        profile[id] = profile[id][:1]
                else:
                    profile[id] = answer
            else:
                profile[id] = answer in (True, "yes")
        return profile

    def setupSession(self):
        """Setup the session for the context survey. This will rebuild the
        session tree if the profile has changed.
        """
        return self.session  # XXX this has to be checked
        # survey = self.context.aq_parent
        # new_profile = self.getDesiredProfile()
        # return set_session_profile(survey, self.session, new_profile)

    @property
    @memoize
    def profile_questions(self):
        """Return information for all profile questions in this survey.

        The data is returned as a list of dictionaries with the following
        keys:

        - ``id``: object id of the question
        - ``title``: title of the question
        - ``question``: question about the general occurance
        - ``label_multiple_present``: question about single or multiple
          occurance
        - ``label_single_occurance``: label for single occurance
        - ``label_multiple_occurances``: label for multiple occurance
        """
        return [
            {
                "id": child.id,
                "title": child.title,
                "question": child.question or child.title,
                "use_location_question": getattr(child, "use_location_question", True),
                "label_multiple_present": getattr(
                    child,
                    "label_multiple_present",
                    _(u"Does this happen in multiple places?"),
                ),
                "label_single_occurance": getattr(
                    child,
                    "label_single_occurance",
                    _(u"Enter the name of the location"),
                ),
                "label_multiple_occurances": getattr(
                    child,
                    "label_multiple_occurances",
                    _(u"Enter the names of each location"),
                ),
            }
            for child in self.context.ProfileQuestions()
        ]

    @property
    def session(self):
        return self.context.session

    @property
    @memoize
    def current_profile(self):
        return extractProfile(self.context.aq_parent, self.session)

    def update(self):
        lang = getattr(self.request, "LANGUAGE", "en")
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.message_required = translate(
            _(u"message_field_required", default=u"Please fill out this field."),
            target_language=lang,
        )
        if not self.profile_questions or self.request.method == "POST":
            new_session = self.setupSession()
            self.request.response.redirect(
                "{base_url}/++session++{session_id}/{target}".format(
                    base_url=self.context.aq_parent.absolute_url(),
                    session_id=new_session.id,
                    target=self.next_view_name,
                )
            )


class Update(Profile):
    """Update a survey session after a survey has been republished. If a
    the survey has a profile the user is asked to confirm the current
    profile before continuing.

    The behaviour is exactly the same as the normal start page for a session
    (see the :py:class:`Profile` view), but uses a different template with more
    detailed instructions for the user.
    """

    next_view_name = "@@identification"


class Identification(BrowserView):
    """Survey identification start page.

    This view shows the introduction text for the identification phase. This
    includes an option to print a report with all questions.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object
    for the *identification* component of the URL.

    View name: @@identification
    """

    variation_class = "variation-risk-assessment"

    question_filter = None

    @property
    def next_url(self):
        return "{context_url}/{question_path}/@@{view}".format(
            context_url=self.context.absolute_url(),
            question_path=self.first_question.id,
            view=self.__name__,
        )

    @property
    @memoize
    def first_question(self):
        session = self.context.session
        query = (
            Session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session == session)
            .filter(sql.not_(SKIPPED_PARENTS))
        )
        if self.question_filter:
            query = query.filter(self.question_filter)
        return query.order_by(SurveyTreeItem.path).first()

    @property
    def tree(self):
        question = self.first_question
        if not question:
            return
        return getTreeData(self.request, question, survey=self.context.aq_parent)

    @property
    def extra_text(self):
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get("euphorie")
        have_extra = settings.get("extra_text_identification", False)
        if not have_extra:
            return None
        lang = getattr(self.request, "LANGUAGE", "en")
        # Special handling for Flemish, for which LANGUAGE is "nl-be". For
        # translating the date under plone locales, we reduce to generic "nl".
        # For the specific oira translation, we rewrite to "nl_BE"
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        return translate(
            _(u"extra_text_identification", default=u""), target_language=lang
        )


class DeleteSession(BrowserView):
    """View name: @@delete-session
    """

    def __call__(self):
        start_view = api.content.get_view("start", self.context, self.request)
        if not start_view.can_delete_session:
            raise Unauthorized()

        Session.delete(self.context.session)
        api.portal.show_message(
            _(
                u"Session `${name}` has been deleted.",
                mapping={"name": self.context.session.title},
            ),
            self.request,
            "success",
        )
        self.request.response.redirect(self.context.aq_parent.absolute_url())


class PublicationMenu(BrowserView):

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize_contextless
    def portal(self):
        """ The currenttly authenticated account
        """
        return api.portal.get()

    def notify_modified(self):
        notify(ObjectModifiedEvent(self.context.session))

    def redirect(self):
        target = self.request.get("HTTP_REFERER") or self.context.absolute_url()
        return self.request.response.redirect(target)

    def reset_date(self):
        """ Reset the session date to now
        """
        session = self.context.session
        session.published = datetime.now()
        session.last_publisher = get_current_account()
        self.notify_modified()
        return self.redirect()

    def set_date(self):
        """ Set the session date to now
        """
        return self.reset_date()

    def unset_date(self):
        """ Unset the session date
        """
        session = self.context.session
        session.published = None
        session.last_publisher = None
        self.notify_modified()
        return self.redirect()


class ActionPlanView(BrowserView):
    """Survey action plan start page.

    This view shows the introduction text for the action plan phase.
    """

    variation_class = "variation-risk-assessment"

    # The question filter will find modules AND risks
    question_filter = ACTION_PLAN_FILTER
    # The risk filter will only find risks
    risk_filter = RISK_PRESENT_OR_TOP5_FILTER

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def tree(self):
        return getTreeData(
            self.request,
            self.first_question,
            filter=self.question_filter,
            phase=self.__name__,
            survey=self.context.aq_parent,
        )

    @property
    @memoize
    def first_question(self):
        return FindFirstQuestion(
            dbsession=self.context.session, filter=self.risk_filter
        )

    @property
    @memoize
    def next_url(self):
        # We fetch the first actual risk, so that we can jump directly to it.
        question = self.first_question
        if question is None:
            return
        return "{session_url}/{id}/@@actionplan".format(
            session_url=self.context.absolute_url(), id=question.id
        )

    def __call__(self):
        """ Render the page only if the user has edit rights,
        otherwise redirect to the start page of the session.
        """
        start_view = api.content.get_view("start", self.context, self.request)
        if not start_view.can_edit_session:
            return self.request.response.redirect(
                self.context.absolute_url() + "/@@start"
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return
        return super(ActionPlanView, self).__call__()


class Report(BrowserView):
    """Intro page for report phase.

    View name: @@report
    """

    variation_class = "variation-risk-assessment"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def __call__(self):
        if self.webhelpers.redirectOnSurveyUpdate():
            return

        session = self.context.session
        if self.request.method == "POST":
            session.report_comment = self.request.form.get("comment")

            url = "%s/@@report_company" % self.context.absolute_url()
            if (
                getattr(session, "company", None) is not None
                and getattr(session.company, "country") is not None
            ):
                url = "%s/report_view" % self.context.absolute_url()

            user = getSecurityManager().getUser()
            if getattr(user, "account_type", None) == config.GUEST_ACCOUNT:
                url = "%s/@@register?report_blurb=1&came_from=%s" % (
                    self.request.survey.absolute_url(),
                    urllib.quote(url, ""),
                )
            return self.request.response.redirect(url)

        return super(Report, self).__call__()


class Status(BrowserView, _StatusHelper):
    """Show survey status information.
    """

    variation_class = "variation-risk-assessment"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def session(self):
        return self.context.session

    def update(self):
        def default_risks_by_status():
            return {
                "present": {"high": [], "medium": [], "low": []},
                "possible": {"postponed": [], "todo": []},
            }

        self.risks_by_status = defaultdict(default_risks_by_status)
        now = datetime.now()
        lang = date_lang = getattr(self.request, "LANGUAGE", "en")
        # Special handling for Flemish, for which LANGUAGE is "nl-be". For
        # translating the date under plone locales, we reduce to generic "nl".
        # For the specific oira translation, we rewrite to "nl_BE"
        if "-" in lang:
            date_lang = lang.split("-")[0]
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.date = u"{0} {1} {2}".format(
            now.strftime("%d"),
            translate(
                PloneLocalesMessageFactory(
                    "month_{0}".format(now.strftime("%b").lower()),
                    default=now.strftime("%B"),
                ),
                target_language=date_lang,
            ),
            now.strftime("%Y"),
        )
        self.label_page = translate(
            _(u"label_page", default=u"Page"), target_language=lang
        )
        self.label_page_of = translate(
            _(u"label_page_of", default=u"of"), target_language=lang
        )
        session = self.context.session
        if session.title != (
            callable(getattr(self.context, "Title", None))
            and self.context.Title()
            or ""
        ):
            self.session_title = session.title
        else:
            self.session_title = None

    def getStatus(self):
        """ Gather a list of the modules and locations in this survey as well
            as data around their state of completion.
        """
        session = Session()
        total_ok = 0
        total_with_measures = 0
        modules = self.getModules()
        filtered_risks = self.getRisks([m["path"] for m in modules.values()])
        for (module, risk) in filtered_risks:
            module_path = module.path
            has_measures = False
            if risk.identification in ["yes", "n/a"]:
                total_ok += 1
                modules[module_path]["ok"] += 1
            elif risk.identification == "no":
                measures = session.query(ActionPlan.id).filter(
                    ActionPlan.risk_id == risk.id
                )
                if measures.count():
                    has_measures = True
                    modules[module_path]["risk_with_measures"] += 1
                    total_with_measures += 1
                else:
                    modules[module_path]["risk_without_measures"] += 1
            elif risk.postponed:
                modules[module_path]["postponed"] += 1
            else:
                modules[module_path]["todo"] += 1

            self.add_to_risk_list(risk, module_path, has_measures=has_measures)

        for key, m in modules.items():
            if (
                m["ok"]
                + m["postponed"]
                + m["risk_with_measures"]
                + m["risk_without_measures"]
                + m["todo"]
                == 0
            ):
                del modules[key]
                del self.tocdata[key]
        self.percentage_ok = (
            not len(filtered_risks)
            and 100
            or int(
                (total_ok + total_with_measures) / Decimal(len(filtered_risks)) * 100
            )
        )
        self.status = modules.values()
        self.status.sort(key=lambda m: m["path"])
        self.toc = self.tocdata.values()
        self.toc.sort(key=lambda m: m["path"])

    def add_to_risk_list(self, risk, module_path, has_measures=False):
        if self.is_skipped_from_risk_list(risk):
            return

        risk_title = self.get_risk_title(risk)

        url = "{session_url}/{risk_id}/@@actionplan".format(
            session_url=self.context.absolute_url(),
            risk_id=risk.id,
        )
        if risk.identification != "no":
            status = risk.postponed and "postponed" or "todo"
            self.risks_by_status[module_path]["possible"][status].append(
                {"title": risk_title, "path": url}
            )
        else:
            self.risks_by_status[module_path]["present"][risk.priority or "low"].append(
                {"title": risk_title, "path": url, "has_measures": has_measures}
            )

    def get_risk_title(self, risk):
        if risk.is_custom_risk:
            risk_title = risk.title
        else:
            risk_obj = self.context.aq_parent.restrictedTraverse(
                risk.zodb_path.split("/")
            )
            if not risk_obj:
                return
            if risk.identification == "no":
                risk_title = risk_obj.problem_description
            else:
                risk_title = risk.title
        return risk_title

    def is_skipped_from_risk_list(self, risk):
        if risk.priority == "high":
            if risk.identification != "no":
                if risk.risk_type not in ["top5"]:
                    return True
        else:
            return True

    def __call__(self):
        if self.webhelpers.redirectOnSurveyUpdate():
            return
        self.update()
        self.getStatus()
        return super(Status, self).__call__()


class RisksOverview(Status):
    """ Implements the "Overview of Risks" report, see #10967
    """

    def is_skipped_from_risk_list(self, risk):
        if risk.identification == "yes":
            return True


class MeasuresOverview(Status):
    """ Implements the "Overview of Measures" report, see #10967
    """

    def update(self):
        super(MeasuresOverview, self).update()
        lang = getattr(self.request, "LANGUAGE", "en")
        if "-" in lang:
            lang = lang.split("-")[0]
        now = datetime.now()
        next_month = datetime(now.year, (now.month + 1) % 12 or 12, 1)
        month_after_next = datetime(now.year, (now.month + 2) % 12 or 12, 1)
        self.months = []
        self.months.append(now.strftime("%b"))
        self.months.append(next_month.strftime("%b"))
        self.months.append(month_after_next.strftime("%b"))
        self.monthstrings = [
            translate(
                PloneLocalesMessageFactory(
                    "month_{0}_abbr".format(month.lower()), default=month
                ),
                target_language=lang,
            )
            for month in self.months
        ]

        query = (
            Session.query(Module, Risk, ActionPlan)
            .filter(
                sql.and_(
                    Module.session == self.session,
                    Module.profile_index > -1,
                )
            )
            .filter(sql.not_(SKIPPED_PARENTS))
            .filter(
                sql.or_(
                    MODULE_WITH_RISK_OR_TOP5_FILTER,
                    RISK_PRESENT_OR_TOP5_FILTER,
                )
            )
            .join(
                (
                    Risk,
                    sql.and_(
                        Risk.path.startswith(Module.path),
                        Risk.depth == Module.depth + 1,
                        Risk.session == self.session,
                    ),
                )
            )
            .join((ActionPlan, ActionPlan.risk_id == Risk.id))
            .order_by(
                sql.case(
                    value=Risk.priority, whens={"high": 0, "medium": 1}, else_=2
                ),
                Risk.path,
            )
        )
        measures = [
            t
            for t in query.all()
            if (
                (
                    t[-1].planning_start is not None
                    and t[-1].planning_start.strftime("%b") in self.months
                )
                and (
                    t[-1].planning_end is not None
                    or t[-1].responsible is not None
                    or t[-1].prevention_plan is not None
                    or t[-1].requirements is not None
                    or t[-1].budget is not None
                    or t[-1].action_plan is not None
                )
            )
        ]

        modulesdict = defaultdict(lambda: defaultdict(list))
        for module, risk, action in measures:
            if "custom-risks" not in risk.zodb_path:
                risk_obj = self.request.survey.restrictedTraverse(
                    risk.zodb_path.split("/")
                )
                title = risk_obj and risk_obj.problem_description or risk.title
            else:
                title = risk.title
            modulesdict[module][risk.priority].append(
                {
                    "title": title,
                    "description": action.action_plan,
                    "months": [
                        action.planning_start and action.planning_start.month == m.month
                        for m in [now, next_month, month_after_next]
                    ],
                }
            )

        main_modules = {}
        for module, risks in sorted(modulesdict.items(), key=lambda m: m[0].zodb_path):
            module_obj = self.request.survey.restrictedTraverse(
                module.zodb_path.split("/")
            )
            if (
                IProfileQuestion.providedBy(module_obj)
                or ICustomRisksModule.providedBy(module_obj)
                or module.depth >= 3
            ):
                path = module.path[:6]
            else:
                path = module.path[:3]
            if path in main_modules:
                for prio in risks.keys():
                    if prio in main_modules[path]["risks"]:
                        main_modules[path]["risks"][prio].extend(risks[prio])
                    else:
                        main_modules[path]["risks"][prio] = risks[prio]
            else:
                title = module.title
                number = module.number
                if "custom-risks" in module.zodb_path:
                    num_elems = number.split(".")
                    number = u".".join([u"Ω"] + num_elems[1:])
                main_modules[path] = {"name": title, "number": number, "risks": risks}

        self.modules = []
        for key in sorted(main_modules.keys()):
            self.modules.append(main_modules[key])
