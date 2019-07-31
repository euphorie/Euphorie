# coding=utf-8
from Acquisition import aq_inner
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import ACTION_PLAN_FILTER
from euphorie.client.model import get_current_account
from euphorie.client.model import RISK_PRESENT_OR_TOP5_FILTER
from euphorie.client.model import SKIPPED_PARENTS
from euphorie.client.model import SurveyTreeItem
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.profile import extractProfile
from euphorie.content.profilequestion import IProfileQuestion
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.supermodel import model
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

    def notify_modified(self, session):
        notify(ObjectModifiedEvent(session))

    def redirect(self):
        target = self.request.get("HTTP_REFERER") or self.context.absolute_url()
        return self.request.response.redirect(target)

    def reset_date(self, sessionid):
        """ Reset the session date to now
        """
        session = self.session(sessionid)
        session.published = datetime.now()
        session.last_publisher = get_current_account()
        self.notify_modified(session)
        return self.redirect()

    def set_date(self, sessionid):
        """ Set the session date to now
        """
        return self.reset_date(sessionid)

    def unset_date(self, sessionid):
        """ Unset the session date
        """
        session = self.session(sessionid)
        session.published = None
        session.last_publisher = None
        self.notify_modified(session)
        return self.redirect()


class ActionPlan(BrowserView):
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
            session_url=self.context.absolute_url(),
            id=question.id,
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
        return super(ActionPlan, self).__call__()
