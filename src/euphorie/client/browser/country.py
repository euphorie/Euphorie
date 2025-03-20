from Acquisition import aq_inner
from anytree import NodeMixin
from anytree.node.util import _repr
from euphorie import MessageFactory as _
from euphorie.client import utils
from euphorie.client.country import IClientCountry
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import get_current_account
from euphorie.client.sector import IClientSector
from euphorie.content.survey import ISurvey
from euphorie.content.utils import getRegionTitle
from logging import getLogger
from plone import api
from plone.base.utils import safe_text
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.Five import BrowserView
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope.deprecation import deprecate
from zope.interface import directlyProvides

import json


logger = getLogger(__name__)


def capitalize(text):
    if text:
        return f"{text[0].upper()}{text[1:]}"


class Node(NodeMixin):
    def __init__(self, context, parent=None, **kwargs):
        self.__dict__.update(kwargs)
        self.context = context
        self.parent = parent

    @property
    def groups(self):
        """Assume childrens are groups and return them sorted by title."""
        return sorted(self.children, key=lambda x: x.title)

    @property
    def sessions(self):
        """Assume childrens are sessions and return them sorted by reversed
        modification date."""
        return sorted(self.children, key=lambda x: x.context.modified, reverse=True)

    @property
    def survey_templates(self):
        """Return all children that are survey_templates, sorted by title."""
        return sorted(
            (item for item in self.children if item.type == "survey_template"),
            key=lambda x: x.title.lower(),
        )

    @property
    def categories(self):
        """Return all children that are categories, sorted by title."""
        return sorted(
            (item for item in self.children if item.type == "category"),
            key=lambda x: x.title,
        )

    def __repr__(self):
        args = [
            "%r"
            % self.separator.join([""] + [repr(node.context) for node in self.path])
        ]
        return _repr(self, args=args, nameblacklist=["context"])


class SurveyTemplatesMixin:
    # Here, we assemble the list of available tools for starting a new session

    @property
    @memoize
    def survey_templates_root(self):
        return Node(None, title="", type="root")

    @memoize
    def get_survey_category_node(self, category):
        if category is None:
            # Everything is grouped under the survey_templates_root node
            return self.survey_templates_root
        return Node(
            category,
            parent=self.get_survey_category_node(None),
            title=category,
            type="category",
        )

    @memoize
    def get_survey_template_node(self, survey_item):
        category, survey, id = survey_item
        return Node(
            survey,
            parent=self.get_survey_category_node(category),
            title=survey.title,
            type="survey_template",
            id=id,
        )

    @memoize
    def get_survey_templates_tree_root(self):
        survey_items = self.get_survey_templates()
        list(map(self.get_survey_template_node, survey_items))
        return self.survey_templates_root

    @memoize
    def get_survey_templates(self):
        # this is a list of tuples of the form
        # (category name, survey object, survey id)
        survey_items = []
        language = self.request.locale.id.language or ""
        for sector in aq_inner(self.context).values():
            if not IClientSector.providedBy(sector):
                continue

            for survey in sector.values():
                if not ISurvey.providedBy(survey):
                    continue
                if getattr(survey, "preview", False):
                    continue
                if (
                    survey.language
                    and survey.language != language
                    and not survey.language.strip().startswith(language)
                ):
                    continue
                if getattr(survey, "obsolete", False):
                    continue
                categories = getattr(survey, "tool_category", None)
                id = f"{sector.id}/{survey.id}"
                if not isinstance(categories, list):
                    categories = [categories]
                if not categories:
                    categories = ["None"]
                for category in categories:
                    survey_items.append((category, survey, id))
        return sorted(survey_items, key=lambda x: (x[0] or "None", x[1].title))


class SessionsView(BrowserView, SurveyTemplatesMixin):
    variation_class = "variation-dashboard"
    form_action_name = "dashboard-switcher"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def survey_session_model(self):
        return self.webhelpers.survey_session_model

    @property
    def _portlet_names(self):
        names = ["portlet-my-ras", "portlet-available-tools"]
        if self.webhelpers.use_training_module:
            names.append("portlet-my-trainings")
        return names

    @property
    @memoize
    def portlets(self):
        return [
            api.content.get_view(name, self.context, self.request)
            for name in self._portlet_names
        ]

    @property
    @memoize
    def my_context(self):
        if IClientCountry.providedBy(self.context):
            return "country"
        elif ISurvey.providedBy(self.context):
            return "survey"

    @property
    @memoize_contextless
    def portal(self):
        return api.portal.get()

    @property
    @memoize_contextless
    def account(self):
        """The currently authenticated account."""
        return get_current_account()

    def _updateSurveys(self):
        self.surveys = []
        self.obsolete_surveys = []

        language = self.request.locale.id.language or ""
        for sector in aq_inner(self.context).values():
            if not IClientSector.providedBy(sector):
                continue

            for survey in sector.values():
                if not ISurvey.providedBy(survey):
                    continue
                if getattr(survey, "preview", False):
                    continue
                if (
                    survey.language
                    and survey.language != language
                    and not survey.language.strip().startswith(language)
                ):
                    continue
                info = {"id": f"{sector.id}/{survey.id}", "title": survey.title}
                if getattr(survey, "obsolete", False):
                    # getattr needed for surveys which were published before
                    # the obsolete flag added.
                    self.obsolete_surveys.append(info)
                else:
                    self.surveys.append(info)
        self.surveys.sort(key=lambda s: s["title"])
        self.obsolete_surveys.sort(key=lambda s: s["title"])

    def _NewSurvey(self, info, account=None):
        """Utility method to start a new survey session."""
        context = aq_inner(self.context)
        survey = info.get("survey")
        survey = context.restrictedTraverse(survey)
        if not ISurvey.providedBy(survey):
            logger.error("Tried to start invalid survey %r", info.get("survey"))
            # Things are sufficiently messed up at this point that rendering
            # breaks, so trigger a redirect to the same URL again.
            self.request.response.redirect(context.absolute_url())
            return

        title = info.get("title", "").strip()

        survey_view = api.content.get_view("index_html", survey, self.request)
        survey_session = survey_view.create_survey_session(title, account)
        self.request.response.redirect(
            f"{survey_session.absolute_url()}/@@start?initial_view=1&new_session=1"
        )

    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session = Session.query(self.survey_session_model).get(info["session"])
        extra = ""
        if info.get("new_clone", None):
            extra = "&new_clone=1"
        self.request.response.redirect(
            f"{session.absolute_url()}/@@resume?initial_view=1{extra}"
        )

    def _CloneSurvey(self, info):
        session = Session.query(self.survey_session_model).get(info["session"])
        clone_view = api.content.get_view(
            "clone-session", session.traversed_session, self.request
        )
        clone_view.clone()

    def tool_byline(self):
        title = api.portal.translate(
            _("title_tool", default="OiRA - Online interactive Risk Assessment")
        )
        return title.split("-")[-1].strip()

    def set_language(self):
        utils.setLanguage(
            self.request, self.context, getattr(self.context, "language", None)
        )

    def __call__(self):
        if not self.account:
            raise Unauthorized()

        self.set_language()
        reply = self.request.form
        action = reply.get("action")
        if action == "new":
            if self.my_context == "survey":
                reply["survey"] = "/".join(self.context.getPhysicalPath())
            return self._NewSurvey(reply)
        elif action == "continue":
            return self._ContinueSurvey(reply)
        if action == "clone":
            return self._CloneSurvey(reply)
        self._updateSurveys()
        return super().__call__()


class SessionBrowserNavigator(BrowserView):
    """Logic to build the navigator for the sessions."""

    no_splash = True

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def group_model(self):
        return self.webhelpers.group_model

    @property
    @memoize
    def survey_session_model(self):
        return self.webhelpers.survey_session_model

    @property
    @memoize
    def groupid(self):
        return self.request.get("groupid")

    @memoize
    def get_root_group(self, groupid=None):
        """Return the group that is the root of the navigation tree."""
        if not groupid:
            groupid = self.groupid
        if not groupid:
            return
        base_query = Session.query(self.group_model).order_by(
            self.group_model.short_name
        )
        return base_query.filter(self.group_model.group_id == groupid).one_or_none()

    @property
    @memoize
    def searchable_text(self):
        """Return the text we need to search in postgres already surrounded
        with '%' Allow a minimum size of 3 characters to reduce the load."""
        searchable_text = self.request.get("SearchableText")
        if not isinstance(searchable_text, str):
            return ""
        if len(searchable_text) < 3:
            return ""
        return f"%{safe_text(searchable_text)}%"

    @memoize
    def leaf_groups(self, groupid=None):
        """Nothing to do in main OiRA - to be filled in customer-specific
        packages.
        """
        return []

    @memoize
    def leaf_sessions(self):
        """The sessions we want to display in the navigation."""
        query = self.webhelpers.get_sessions_query(
            context=self.webhelpers.country_obj, searchable_text=self.searchable_text
        )
        return query.all()

    def has_content(self):
        """Checks if we have something meaningfull to display."""
        if len(self.leaf_groups()):
            return True
        if len(self.leaf_sessions()):
            return True
        return False


class Assessments(BrowserView):
    query_parameter = "SearchableText"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def form_action_name(self):
        return self.__name__

    @property
    def template(self):
        return self.index

    @property
    @memoize
    def organisations(self):
        """Return the organisations the current user is member of."""
        organisation_view = api.content.get_view(
            "organisation", self.context, self.request
        )
        return organisation_view.organisations

    @property
    def organisation_options(self):
        """Return the organisations of the current user
        for displaying in a select box."""
        selected_organisation = self.selected_organisation
        return [
            {
                "label": organisation.title,
                "value": organisation.owner_id,
                "selected": (
                    "selected" if organisation == selected_organisation else None
                ),
            }
            for organisation in self.organisations
        ]

    def is_filter_active(self):
        """True if any filters in the request parameters are different from the
        defaults."""
        return (
            self.request.get("organisation_owner_id")
            or self.request.get("sort_on", "modified") != "modified"
        )

    @property
    def selected_organisation(self):
        """Return the organisation selected in the request
        if it matches an organisation of the currently authenticated users.
        """
        organisation_value = self.request.get("organisation_owner_id", "")
        try:
            organisation_value = int(organisation_value)
        except ValueError:
            return
        for organisation in self.organisations:
            if organisation.owner_id == organisation_value:
                return organisation

    @property
    @memoize
    def sessions(self):
        searchable_text = self.request.get(self.query_parameter, None)
        if searchable_text and "%" not in searchable_text:
            searchable_text = f"%{searchable_text}%"
        sort_on_value = self.request.get("sort_on", "modified")
        if sort_on_value == "alphabetical":
            order_by = self.webhelpers.survey_session_model.title
        else:
            order_by = False

        if self.selected_organisation:
            filter_by_account = self.selected_organisation.owner_id
        else:
            # `True` means filter for current account.
            filter_by_account = True

        return self.webhelpers.get_sessions_query(
            context=self.context,
            searchable_text=searchable_text,
            include_archived=True,
            filter_by_account=filter_by_account,
            order_by=order_by,
        )

    def get_archived_label(self, session):
        if not session.is_archived:
            return ""
        return api.portal.translate(_("Archived"))


class AssessmentsJson(Assessments):
    query_parameter = "q"

    def get_title(self, session):
        title = session.title
        if not title:
            title_missing = api.portal.translate(
                _("label_missing_title", default="Title is missing")
            )
            title = f"[{title_missing}]"
        return title

    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(
            [
                {"id": session.id, "text": self.get_title(session)}
                for session in self.sessions
            ]
        )


class Surveys(BrowserView, SurveyTemplatesMixin):
    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def form_action_name(self):
        return self.__name__

    def get_filters(self):
        filters = {}
        get = self.request.form.get

        client_path = "/".join(self.request.client.getPhysicalPath())
        path = "/".join((client_path, self.country))
        sector = get("sector")
        if sector:
            path = "/".join((path, sector))
        filters["path"] = path

        language = get("Language")
        if language:
            filters["Language"] = language

        sort_on = get("sort_on", "created")
        filters["sort_on"] = sort_on
        if sort_on == "created":
            filters["sort_order"] = "reverse"

        searchable_text = get("SearchableText")
        if searchable_text:
            filters["SearchableText"] = searchable_text

        return filters

    @property
    @memoize
    def country(self):
        return self.request.form.get("country", self.context.getId())

    @property
    @memoize
    def countries(self):
        return sorted(
            [
                {
                    "id": country.getId(),
                    "Title": getRegionTitle(self.request, country.getId()),
                }
                for country in self.request.client.values()
                if (IClientCountry.providedBy(country) and len(country.objectIds()))
            ],
            key=lambda co: "0" if co["id"] == "eu" else co["Title"],
        )

    @property
    @memoize
    def sectors(self):
        country_obj = self.request.client.restrictedTraverse(self.country)
        return [
            sector
            for sector in aq_inner(country_obj).values()
            if IClientSector.providedBy(sector)
        ]

    @property
    @memoize
    def tools(self):
        filters = self.get_filters()
        tools = [
            (None, survey.getObject(), survey.getId)
            for survey in api.content.find(
                object_provides="euphorie.content.survey.ISurvey", **filters
            )
        ]
        # We must filter out tools marked as obsolete or preview
        return [
            record
            for record in tools
            if (
                not getattr(record[1], "preview", None)
                and not getattr(record[1], "obsolete", None)
            )
        ]

    @property
    @memoize
    def languages(self):
        return sorted(
            [
                {"code": code, "name": self.webhelpers.getNameForLanguageCode(code)}
                for code in api.portal.get_tool("portal_catalog").uniqueValuesFor(
                    "Language"
                )
                if code and code != "None"
            ],
            key=lambda lang: lang["code"],
        )

    def __call__(self):
        utils.setLanguage(
            self.request, self.context, getattr(self.context, "language", None)
        )
        return super().__call__()


class PortletBase(BrowserView):
    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def filter_survey(self, survey):
        if getattr(survey, "preview", False):
            return False
        if getattr(survey, "obsolete", False):
            return False
        if not survey.language:
            return True
        language = self.request.locale.id.language or ""
        if survey.language == language:
            return True
        if survey.language.strip().startswith(language):
            return True
        return False

    @property
    @memoize
    def surveys(self):
        surveys = set()
        sectors = self.context.listFolderContents(
            {"portal_type": "euphorie.clientsector"}
        )
        for sector in sectors:
            surveys.update(
                filter(
                    self.filter_survey,
                    sector.listFolderContents({"portal_type": "euphorie.survey"}),
                )
            )
        return sorted(surveys, key=lambda survey: survey.title)


class MyRAsPortlet(PortletBase):
    element_id = "portlet-my-risk-assessments"

    @property
    def columns(self):
        if self.surveys:
            return "2"
        return "3"

    @property
    def assessments_list_macro(self):
        """Get the listing macro from the assessments template."""
        request = self.request.clone()
        # This is needed, since the view might be subclassed and therefore
        # associated with a different skin-layer.
        directlyProvides(request, IClientSkinLayer)
        view = api.content.get_view("assessments", self.context, request)
        return view.template.macros["assessments_list"]

    @property
    @memoize_contextless
    def hide_archived(self):
        """By default we hide the archived session and we have a checkbox that
        shows with a sibling hide_archived_marker input field."""
        if self.request.get("hide_archived_marker"):
            if not self.request.get("hide_archived"):
                return False
        return True

    @property
    @memoize
    def organisation_view(self):
        """Get the organisation view to reuse its methods."""
        return api.content.get_view("organisation", self.context, self.request)

    @property
    @memoize
    @deprecate(
        "Replace with self.sessions_by_organisation (which is a dict), "
        "deprecated in version 14.2"
    )
    def sessions(self):
        """We want the archived sessions."""
        return (
            self.webhelpers.get_sessions_query(
                context=self.context, include_archived=not self.hide_archived
            )
            .limit(5)
            .all()
        )

    @property
    @memoize
    def sessions_by_organisation(self):
        """Return the sessions grouped by organisation."""
        base_query = self.webhelpers.get_sessions_query(
            context=self.context, include_archived=not self.hide_archived
        )

        account_id_column = self.webhelpers.survey_session_model.account_id

        sessions_by_organisation = []
        known_owner_ids = set()
        for organisation in self.organisation_view.organisations:
            known_owner_ids.add(organisation.owner_id)
            sessions = (
                base_query.filter(account_id_column == organisation.owner_id)
                .limit(5)
                .all()
            )
            if sessions:
                sessions_by_organisation.append((organisation, sessions))

        account = self.webhelpers.get_current_account()
        if not account.organisation:
            sessions = (
                base_query.filter(account_id_column.notin_(known_owner_ids))
                .limit(5)
                .all()
            )
            if sessions:
                sessions_by_organisation.insert(0, (None, sessions))

        return dict(sessions_by_organisation)

    @property
    def label_start_session(self):
        label = api.portal.translate(
            _("link_start_session", default="Start a new risk assessment")
        )
        return capitalize(label)


class AvailableToolsPortlet(PortletBase, SurveyTemplatesMixin):
    element_id = "portlet-available-tools"
