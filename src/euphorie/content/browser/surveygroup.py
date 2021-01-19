# coding=utf-8
from ..surveygroup import ISurveyGroup
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.content import MessageFactory as _
from euphorie.content.interfaces import SurveyUnpublishEvent
from euphorie.content.survey import ISurvey
from OFS.event import ObjectClonedEvent
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from six.moves.urllib.parse import urlencode
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.event import notify

import datetime
import logging


log = logging.getLogger(__name__)


class SurveyGroupView(BrowserView):
    def surveys(self):
        templates = [
            dict(title=survey.title, url=survey.absolute_url())
            for survey in self.context.values()
            if ISurvey.providedBy(survey)
        ]
        return templates


class AddForm(DefaultAddForm):
    """Custom add form for :obj:`Survey` instances. This add form adds a
    the :obj:`ITemplateSchema` schema, which allows users to pick a template
    survey to use as a basis for the new survey.
    """

    portal_type = "euphorie.surveygroup"
    schema = ISurveyGroup
    template = ViewPageTemplateFile("templates/surveygroup_add.pt")

    def update(self):
        super(AddForm, self).update()
        sector = aq_inner(self.context)
        country = aq_parent(sector)
        self.my_country = country.id
        self.my_sector = sector.id

    def buildSurveyTree(self):
        site = getUtility(ISiteRoot)
        catalog = api.portal.get_tool("portal_catalog")
        startPath = "%s/sectors" % "/".join(site.getPhysicalPath())
        startPathDepth = startPath.count("/") + 1
        query = {
            "path": {"query": startPath, "depth": 4, "navtree": True},
            "portal_type": [
                "euphorie.country",
                "euphorie.sector",
                "euphorie.surveygroup",
                "euphorie.survey",
            ],
            "sort_on": "path",
            "sort_order": "asc",
        }
        tree = {}
        for brain in catalog.searchResults(query):
            path = brain.getPath().split("/")[startPathDepth:]
            if brain.portal_type == "euphorie.country":
                tree[brain.id] = dict(
                    id=brain.id, title=brain.Title, path=brain.getPath(), sectors={}
                )
            elif brain.portal_type == "euphorie.sector":
                country = tree[path[0]]
                country["sectors"][brain.id] = dict(
                    id=brain.id, title=brain.Title, path=brain.getPath(), groups={}
                )
            elif brain.portal_type == "euphorie.surveygroup":
                country = tree[path[0]]
                sector = country["sectors"][path[1]]
                sector["groups"][brain.id] = dict(
                    id=brain.id, title=brain.Title, path=brain.getPath(), surveys={}
                )
            elif brain.portal_type == "euphorie.survey":
                country = tree[path[0]]
                sector = country["sectors"][path[1]]
                group = sector["groups"][path[2]]
                group["surveys"][brain.id] = dict(
                    id=brain.id,
                    title=brain.Title,
                    path=brain.getPath(),
                    url=brain.getURL(),
                )
        my_sector_path = tree[self.my_country]["sectors"][self.my_sector]["path"]
        countries = sorted(tree.values(), key=lambda x: x["title"])
        self.my_group = None
        for country in countries:
            country["sectors"] = sectors = sorted(
                country["sectors"].values(), key=lambda x: x["title"]
            )

            for sector in sectors:
                sector["groups"] = groups = sorted(
                    sector["groups"].values(), key=lambda x: x["title"]
                )

                if sector["path"] == my_sector_path and sector["groups"]:
                    self.my_group = sector["groups"][0]["id"]
                for group in groups:
                    group["surveys"] = sorted(
                        group["surveys"].values(), key=lambda x: x["title"]
                    )

                sector["groups"] = [g for g in groups if g["surveys"]]
            country["sectors"] = [s for s in sectors if s["groups"]]
        countries = [c for c in countries if c["sectors"]]
        return countries

    def copyTemplate(self, source, target):
        target = self.context[target.id]  # Acquisition-wrap
        try:
            source._notifyOfCopyTo(target, op=0)
        except ConflictError:
            raise

        copy = source._getCopy(target)

        today = datetime.date.today()
        title = self.request.locale.dates.getFormatter("date", length="long").format(
            datetime.date.today()
        )
        copy.id = today.isoformat()
        copy.title = title
        source_algorithm = aq_parent(source).evaluation_algorithm
        target_algorithm = self.request.form.get(
            "form.widgets.evaluation_algorithm", [source_algorithm]
        ).pop()
        target.evaluation_algorithm = target_algorithm
        target._setObject(copy.id, copy)
        if source_algorithm != target_algorithm:
            from euphorie.content.risk import EnsureInterface
            from euphorie.content.risk import IRisk

            risks = [
                item
                for (id, item) in target.ZopeFind(target, search_sub=1)
                if IRisk.providedBy(item)
            ]
            for risk in risks:
                EnsureInterface(risk)

        if hasattr(copy, "published"):
            delattr(copy, "published")
        copy = target[copy.id]  # Acquisition-wrap
        copy.wl_clearLocks()
        copy._postCopy(target, op=0)

        wt = api.portal.get_tool("portal_workflow")
        if wt.getInfoFor(copy, "review_state") == "published":
            wt.doActionFor(copy, "retract")

        notify(ObjectClonedEvent(target[copy.id]))
        return copy

    def createAndAdd(self, data):
        obj = super(AddForm, self).createAndAdd(data)
        obj = aq_inner(self.context)[obj.id]

        form = self.request.form
        if form["source"] != "scratch":
            sector = aq_inner(self.context)
            if form["source"] == "other":
                country_id = form["country"]
                country = aq_parent(aq_parent(sector))[country_id]
                bits = form["sector.%s" % country_id].split(".", 1)
                sector = country[bits[0]]
                surveygroup = sector[bits[1]]
                survey_id = form["survey.%s.%s" % (country_id, surveygroup.id)]
                survey = surveygroup[survey_id]
            else:
                sg_local = form["surveygroup.local"]
                surveygroup = sector[sg_local]
                survey = surveygroup[form["survey.local.%s" % sg_local]]

            survey = self.copyTemplate(survey, obj)
            self.immediate_view = survey.absolute_url()
        else:
            title = api.portal.translate(_("survey_default_title", default=u"Standard"))

            obj = aq_inner(self.context)[obj.id]
            survey = createContentInContainer(obj, "euphorie.survey", title=title)

            self.immediate_view = survey.absolute_url()
        return obj


class AddView(DefaultAddView):
    form = AddForm


class Unpublish(BrowserView):
    def unpublish(self):
        context = aq_inner(self.context)
        published_survey = context[context.published]

        wt = api.portal.get_tool("portal_workflow")
        if wt.getInfoFor(published_survey, "review_state") != "published":
            log.warning(
                "Trying to unpublish survey %s which is not marked as " "published",
                "/".join(published_survey.getPhysicalPath()),
            )
        else:
            wt.doActionFor(published_survey, "retract")
        notify(SurveyUnpublishEvent(published_survey))

    def post(self):
        action = self.request.form.get("action", "cancel")
        if action == "unpublish":
            self.unpublish()
            api.portal.show_message(
                _(
                    "message_unpublish_success",
                    default=u"This OiRA Tool is now no longer available in "
                    u"the client.",
                ),
                self.request,
                "success",
            )
        else:
            api.portlal.show_message(
                _("message_unpublish_cancel", default=u"Cancelled unpublish action."),
                self.request,
                "notice",
            )

        context = aq_inner(self.context)
        self.request.response.redirect(context.absolute_url())

    def __call__(self):
        if self.request.method == "POST":
            self.post()
        else:
            return super(Unpublish, self).__call__()


class VersionCommand(BrowserView):
    def __call__(self):
        surveygroup = aq_inner(self.context)
        action = self.request.form.get("action")
        survey_id = self.request.form.get("survey")
        response = self.request.response
        if action == "publish":
            response.redirect(
                "%s/%s/@@publish" % (surveygroup.absolute_url(), survey_id)
            )
        elif action == "unpublish":
            response.redirect("%s/@@unpublish" % surveygroup.absolute_url())
        elif action == "clone":
            response.redirect(
                "%s/++add++euphorie.survey?%s"
                % (surveygroup.absolute_url(), urlencode(dict(survey=survey_id)))
            )
        else:
            log.error("Invalid version command action: %r", action)
