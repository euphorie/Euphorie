"""
Survey Group
------------

A Survey Group is a container for several Survey versions.

https://admin.oiraproject.eu/sectors/eu/eu-private-security/private-security-eu
"""

import datetime
import logging
import urllib
from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.event import ObjectClonedEvent
from ZODB.POSException import ConflictError
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import getUtility
from zope.event import notify
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from .. import MessageFactory as _
from euphorie.content.interfaces import SurveyUnpublishEvent
from euphorie.content.survey import ISurvey
from five import grok
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.utils import createContentInContainer
from plone.directives import dexterity
from plone.directives import form
from plonetheme.nuplone.skin.interfaces import NuPloneSkin


grok.templatedir("templates")

log = logging.getLogger(__name__)


class ISurveyGroup(form.Schema, IBasic):
    title = schema.TextLine(
            title=_("label_title", default=u"Title"),
            description=_("help_surveygroup_title",
                default=u"The title of this OiRA Tool. This title is used in "
                        u"the OiRA Tool overview in the clients."),
            required=True)
    form.order_before(title="*")

    form.omitted("description")

    obsolete = schema.Bool(
            title=_("label_survey_obsolete",
                default=u"Obsolete OiRA tool"),
            description=_("help_survey_obsolete",
                default=u"This OiRA Tool is obsolete; it has been retired or "
                        u"replaced with another OiRA Tool."),
            default=False,
            required=False)

    form.omitted(IEditForm, 'evaluation_algorithm')
    evaluation_algorithm = schema.Choice(
            title=_("label_survey_evaluation_algorithm",
                default=u"Evaluation algorithm"),
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"kinney",
                    title=_("algorithm_kinney",
                        default=u"Standard three criteria")),
                SimpleTerm(u"french",
                    title=_("french", default=u"Simplified two criteria")),
                ]),
            default=u"kinney",
            required=True)


class SurveyGroup(dexterity.Container):
    grok.name("euphorie.surveygroup")
    implements(ISurveyGroup)

    published = None
    evaluation_algorithm = u"kinney"
    obsolete = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return op


class View(grok.View):
    grok.context(ISurveyGroup)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")

    def render(self):
        latest = aq_inner(self.context).values()[0]
        self.request.response.redirect(latest.absolute_url())


class AddForm(dexterity.AddForm):
    """Custom add form for :obj:`Survey` instances. This add form adds a
    the :obj:`ITemplateSchema` schema, which allows users to pick a template
    survey to use as a basis for the new survey.
    """
    grok.context(ISurveyGroup)
    grok.name("euphorie.surveygroup")
    grok.require("euphorie.content.AddNewRIEContent")

    template = ViewPageTemplateFile("templates/surveygroup_add.pt")

    def update(self):
        super(AddForm, self).update()
        sector = aq_inner(self.context)
        country = aq_parent(sector)
        self.my_country = country.id
        self.my_sector = sector.id

    def buildSurveyTree(self):
        site = getUtility(ISiteRoot)
        catalog = getToolByName(self.context, "portal_catalog")
        startPath = "%s/sectors" % "/".join(site.getPhysicalPath())
        startPathDepth = startPath.count("/") + 1
        query = \
            {"path": {'query': startPath,
                      'depth': 4,
                    'navtree': True},
             "portal_type": ["euphorie.country",
                             "euphorie.sector",
                             "euphorie.surveygroup",
                             "euphorie.survey"],
             "sort_on": "path",
             "sort_order": "asc"}
        tree = {}
        for brain in catalog.searchResults(query):
            path = brain.getPath().split("/")[startPathDepth:]
            if brain.portal_type == "euphorie.country":
                tree[brain.id] = dict(id=brain.id,
                                    title=brain.Title,
                                    path=brain.getPath(),
                                    sectors={})
            elif brain.portal_type == "euphorie.sector":
                country = tree[path[0]]
                country["sectors"][brain.id] = dict(id=brain.id,
                                                    title=brain.Title,
                                                    path=brain.getPath(),
                                                    groups={})
            elif brain.portal_type == "euphorie.surveygroup":
                country = tree[path[0]]
                sector = country["sectors"][path[1]]
                sector["groups"][brain.id] = dict(id=brain.id,
                                                title=brain.Title,
                                                path=brain.getPath(),
                                                surveys={})
            elif brain.portal_type == "euphorie.survey":
                country = tree[path[0]]
                sector = country["sectors"][path[1]]
                group = sector["groups"][path[2]]
                group["surveys"][brain.id] = dict(id=brain.id,
                                                title=brain.Title,
                                                path=brain.getPath(),
                                                url=brain.getURL())
        my_sector_path = tree[self.my_country]["sectors"][
                self.my_sector]["path"]
        countries = sorted(tree.values(), key=lambda x: x["title"])
        self.my_group = None
        for country in countries:
            country["sectors"] = sectors = \
                sorted(country["sectors"].values(), key=lambda x: x["title"])

            for sector in sectors:
                sector["groups"] = groups = \
                    sorted(sector["groups"].values(), key=lambda x: x["title"])

                if sector["path"] == my_sector_path and sector["groups"]:
                    self.my_group = sector["groups"][0]["id"]
                for group in groups:
                    group["surveys"] = sorted(
                                        group["surveys"].values(),
                                        key=lambda x: x["title"]
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
        title = self.request.locale.dates.getFormatter("date", length="long")\
                .format(datetime.date.today())
        copy.id = today.isoformat()
        copy.title = title
        target.evaluation_algorithm = aq_parent(source).evaluation_algorithm
        target._setObject(copy.id, copy)

        if hasattr(copy, "published"):
            delattr(copy, "published")
        copy = target[copy.id]  # Acquisition-wrap
        copy.wl_clearLocks()
        copy._postCopy(target, op=0)

        wt = getToolByName(copy, "portal_workflow")
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
            title = translate(
                        _("survey_default_title", default=u"Standard"),
                        context=self.request)

            obj = aq_inner(self.context)[obj.id]
            survey = createContentInContainer(
                            obj, "euphorie.survey", title=title)

            self.immediate_view = survey.absolute_url()
        return obj


class Unpublish(grok.View):
    grok.context(ISurveyGroup)
    grok.require("cmf.ModifyPortalContent")
    grok.name("unpublish")
    grok.template("unpublish")

    def unpublish(self):
        context = aq_inner(self.context)
        published_survey = context[context.published]

        wt = getToolByName(context, "portal_workflow")
        if wt.getInfoFor(published_survey, "review_state") != "published":
            log.warning("Trying to unpublish survey %s which is not marked as "
                        "published",
                        "/".join(published_survey.getPhysicalPath()))
        else:
            wt.doActionFor(published_survey, "retract")
        notify(SurveyUnpublishEvent(published_survey))

    def post(self):
        action = self.request.form.get("action", "cancel")
        flash = IStatusMessage(self.request).addStatusMessage
        if action == "unpublish":
            self.unpublish()
            flash(_("message_unpublish_success",
                default=u"This OiRA Tool is now no longer available in "
                        u"the client."), "success")
        else:
            flash(_("message_unpublish_cancel",
                default=u"Cancelled unpublish action."), "notice")

        context = aq_inner(self.context)
        self.request.response.redirect(context.absolute_url())

    def update(self):
        super(Unpublish, self).update()
        if self.request.method == "POST":
            self.post()


class VersionCommand(grok.View):
    grok.context(ISurveyGroup)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("version-command")

    def render(self):
        surveygroup = aq_inner(self.context)
        action = self.request.form.get("action")
        survey_id = self.request.form.get("survey")
        response = self.request.response
        if action == "publish":
            response.redirect("%s/%s/@@publish" %
                    (surveygroup.absolute_url(), survey_id))
        elif action == "unpublish":
            response.redirect("%s/@@unpublish" % surveygroup.absolute_url())
        elif action == "clone":
            response.redirect("%s/++add++euphorie.survey?%s" %
                    (surveygroup.absolute_url(),
                     urllib.urlencode(dict(survey=survey_id))))
        else:
            log.error("Invalid version command action: %r", action)


@grok.subscribe(ISurvey, IActionSucceededEvent)
def handleSurveyPublish(survey, event):
    """Event handler (subscriber) for succesfull workflow transitions for
    :py:obj:`ISurvey` objects. This handler performs necessary housekeeping
    tasks on the parent :py:class:`SurveyGroup`.

    If the workflow action is ``publish`` or ``update`` the ``published``
    attribute of the SurveyGroup is set to the id of the published
    survey instance.
    """
    if event.action not in ["publish", "update"]:
        return
    surveygroup = aq_parent(aq_inner(survey))
    surveygroup.published = survey.id


@grok.subscribe(ISurvey, IObjectRemovedEvent)
def handleSurveyRemoved(survey, event):
    """Event handler (subscriber) for deletion of
    :py:obj:`ISurvey` objects. This handler performs necessary houskeeping
    tasks on the parent :py:class:`SurveyGroup`.

    The 'published' attr on the surveygroup states the name of the currently
    published survey.

    If this survey gets deleted, we need to clear this attr.
    """
    parent = aq_parent(survey)
    if ISurveyGroup.providedBy(parent) and parent.published == survey.id:
        parent.published = None
