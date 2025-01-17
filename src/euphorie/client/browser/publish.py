"""
Publish
-------

Copy and publish Surveys from the admin to the client database.
"""

from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client import MessageFactory as _
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.interfaces import ObjectPublishedEvent
from euphorie.content.utils import IToolTypesInfo
from plone import api
from plone.scale.storage import AnnotationStorage
from plonetheme.nuplone.utils import getPortal
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.event import notify
from zope.interface import alsoProvides

import datetime
import logging
import random


log = logging.getLogger(__name__)


def CopyToClient(survey, preview=False):
    """Copy the survey to the online client part of the site.

    :param survey: the survey to copy
    :param bool preview: indicates if this is a preview or a normal publication
    :rtype: :py:class:`euphorie.content.survey.Survey`

    The public area is hardcoded to be a container with id ``client``
    within the site root.

    The ''id'' and ''title'' of the survey group will be used for the
    published survey. If another object with the same ''id'' already exists
    it will be removed first. Any missing country and sector folders are
    created if needed.

    If this is a preview (as indicated by the ``preview`` parameter) the
    id of the survey will be set to ``preview``, guaranteeing that an
    existing published survey will not be replaced. This also means only
    a sector can only have one preview online.

    This method assumes the current user has permissions to create content
    in the online client. This is normally done by using the
    :py:func:`PublishToClient` function which switches the current user
    for the copy operation.

    Returns the new public survey instance.
    """
    # This is based on OFS.CopyContainer.manage_clone, modified to
    # use the sector id and title, skip security checks and remove
    # an existing object with the same id.
    client = getPortal(survey).client

    source = aq_inner(survey)
    surveygroup = aq_parent(source)
    sector = aq_parent(surveygroup)
    country = aq_parent(sector)
    from euphorie.content.sector import ISector

    assert ISector.providedBy(sector)

    if country.id not in client:
        client.invokeFactory(
            "euphorie.clientcountry",
            country.id,
            title=country.title,
            country_type=country.country_type,
        )
    cl_country = client[country.id]

    if sector.id not in cl_country:
        cl_country.invokeFactory("euphorie.clientsector", sector.id)
    target = cl_country[sector.id]
    target.title = sector.title
    target.logo = sector.logo
    # Clear any scaled logos
    AnnotationStorage(target).storage.clear()

    if preview:
        new_id = "preview"
    else:
        new_id = surveygroup.id
    if new_id in target:
        api.content.delete(obj=target[new_id], check_linkintegrity=False)

    copy = api.content.copy(source, target, id=new_id)
    copy.title = surveygroup.title
    copy.obsolete = surveygroup.obsolete
    copy.evaluation_algorithm = surveygroup.evaluation_algorithm
    copy.version = source.id
    copy.published = datetime.datetime.now()
    copy.preview = preview
    copy.reindexObject()

    notify(ObjectPublishedEvent(source))
    return copy


def EnableCustomRisks(survey):
    """In order to allow the user to add custom risks, we create a new special
    module (marked with ICustomRisksModule) in which they may be created."""
    if not api.portal.get_registry_record("euphorie.allow_user_defined_risks"):
        return 0
    if "custom-risks" in survey.keys():
        # We don't want to create the custom risks module twice.
        return 0
    args = dict(
        container=survey,
        type="euphorie.module",
        id="custom-risks",
        title=_("label_custom_risks", default="Custom risks"),
        safe_id=False,
        description=_(
            "description_other_risks",
            default="In case you have identified "
            "risks not included in the tool, you are able to add them now:",
        ),
        optional=True,
        question=_(
            "question_other_risks",
            default="<p><strong>Important:"
            "</strong> In order to avoid duplicating risks, we strongly "
            "recommend you to go first through all the previous modules, if "
            "you have not done it yet.</p><p>If you don't need to add risks, "
            "please continue.</p>",
        ),
    )
    try:
        module = api.content.create(**args)
    except api.exc.InvalidParameterError:
        args["id"] = "custom-risks-" + str(random.randint(0, 99999999))
        module = api.content.create(**args)
    alsoProvides(module, ICustomRisksModule)
    return args["id"]


def PublishToClient(survey, preview=False):
    """Publish a survey in the online client part of the site.

    :param survey: the survey to copy
    :param bool preview: indicates if this is a preview or a normal publication
    :rtype: :py:class:`euphorie.content.survey.Survey`

    This is a wrapper around :py:func:`CopyToClient`, which temporarily changes
    the currently active Zope user to make sure content can be created in the
    client.
    """
    tti = getUtility(IToolTypesInfo)
    tool_types_info = tti()
    tool_type_data = tool_types_info.get(
        survey.tool_type, tool_types_info.get(tti.default_tool_type)
    )
    with api.env.adopt_user("client"):
        with api.env.adopt_roles(["Manager"]):
            survey = CopyToClient(survey, preview)
            if tool_type_data.get("use_omega_risks", True):
                EnableCustomRisks(survey)
    survey.published = (survey.id, survey.title, datetime.datetime.now())
    return survey


def handleSurveyPublish(survey, event):
    """Event handler (subscriber) for successfull workflow transitions for
    :py:obj:`ISurvey` objects. This handler copies the survey to the
    client.
    """
    if event.action not in ["publish", "update"]:
        return
    PublishToClient(survey, False)


def handleSurveyUnpublish(survey, event):
    """Event handler (subscriber) to take care of unpublishing a survey from
    the client."""
    surveygroup = aq_parent(survey)
    sector = aq_parent(surveygroup)
    country = aq_parent(sector)

    with api.env.adopt_user("client"):
        with api.env.adopt_roles(["Manager"]):
            client = getPortal(survey).client
            try:
                clientcountry = client[country.id]
                clientsector = clientcountry[sector.id]
                clientsector[surveygroup.id]
            except KeyError:
                log.info(
                    "Trying to unpublish unpublished survey %s",
                    "/".join(survey.getPhysicalPath()),
                )
                return

            clientsector.manage_delObjects([surveygroup.id])
            if not clientsector.keys():
                clientcountry.manage_delObjects([clientsector.id])


class PublishSurvey(form.Form):
    """Publish a survey.

    Publishing a survey copies it from the content editing environment to the
    public client environment and makes several changes to prepare it for use
    by the client. The client environment is assumed to be located in a
    container with id ''client'' at the root of the site.

    View name: @@publish
    """

    template = ViewPageTemplateFile("templates/publish.pt")

    def publish(self):
        survey = aq_inner(self.context)
        survey.published = datetime.datetime.now()
        wt = getToolByName(survey, "portal_workflow")
        state = wt.getInfoFor(survey, "review_state")
        if state == "draft":
            wt.doActionFor(survey, "publish")
        else:
            wt.doActionFor(survey, "update")

    def is_surveygroup_published(self):
        """Check if this surveygroup has been published before."""
        source = aq_inner(self.context)
        surveygroup = aq_parent(source)
        return bool(surveygroup.published)

    def is_this_survey_published(self):
        """Check if this survey is currently published."""
        source = aq_inner(self.context)
        surveygroup = aq_parent(source)
        return surveygroup.published == source.id

    def _has_same_structure(self, source, target):
        for child_id in target.objectIds():
            if child_id == "custom-risks":
                continue
            if child_id not in source:
                return False
            if not self._has_same_structure(source[child_id], target[child_id]):
                return False
        return True

    def is_structure_changed(self):
        source = aq_inner(self.context)
        surveygroup = aq_parent(source)
        sector = aq_parent(surveygroup)
        country = aq_parent(sector)

        client = getPortal(self.context).client
        if country.id not in client:
            return False
        cl_country = client[country.id]
        if sector.id not in cl_country:
            return False
        cl_sector = cl_country[sector.id]
        if surveygroup.id not in cl_sector:
            return False
        target = cl_sector[surveygroup.id]
        return not self._has_same_structure(source, target)

    def client_url(self):
        """Return the URL this survey will have after it is published."""
        client_url = api.portal.get_registry_record("euphorie.client_url", default="")
        if client_url:
            client_url = client_url.rstrip("/")
        else:
            client_url = getPortal(self.context).client.absolute_url()

        source = aq_inner(self.context)
        surveygroup = aq_parent(source)
        sector = aq_parent(surveygroup)
        country = aq_parent(sector)
        return "/".join([client_url, country.id, sector.id, surveygroup.id])

    @button.buttonAndHandler(_("button_cancel", default="Cancel"))
    def handleCancel(self, action):
        state = getMultiAdapter(
            (aq_inner(self.context), self.request), name="plone_context_state"
        )
        self.request.response.redirect(state.view_url())

    @button.buttonAndHandler(_("button_publish", default="Publish"))
    def handlePublish(self, action):
        self.publish()
        IStatusMessage(self.request).add(
            _(
                "no_translate_link_published_success",
                default=(
                    '${text_message_publish_success}: <a href="${url}">${url}</a>.'
                ),
                mapping={
                    "url": self.client_url(),
                    "text_message_publish_success": _(
                        "message_publish_success",
                        default=(
                            "Successfully published the OiRA Tool. It can be accessed "
                            "at"
                        ),
                    ),
                },
            ),
            type="success",
        )
        state = getMultiAdapter(
            (aq_inner(self.context), self.request), name="plone_context_state"
        )
        self.request.response.redirect(state.view_url())


class PreviewSurvey(form.Form):
    """Generate a preview for a survey. A preview is exactly like a normally
    published survey, except for two differences: there can only be one preview
    for a sector, which has the id `preview`, and after previewing the user is
    redirected to the preview instead of the original context.

    View name: @@preview
    """

    template = ViewPageTemplateFile("templates/preview.pt")

    def publish(self):
        survey = aq_inner(self.context)
        return PublishToClient(survey, True)

    def preview_url(self):
        """Return the URL the preview will have."""
        client_url = api.portal.get_registry_record("euphorie.client_url", default="")
        if client_url:
            client_url = client_url.rstrip("/")
        else:
            client_url = getPortal(self.context).client.absolute_url()

        source = aq_inner(self.context)
        surveygroup = aq_parent(source)
        sector = aq_parent(surveygroup)
        country = aq_parent(sector)

        return "/".join([client_url, country.id, sector.id, "preview"])

    @button.buttonAndHandler(_("button_cancel", default="Cancel"))
    def handleCancel(self, action):
        state = getMultiAdapter(
            (aq_inner(self.context), self.request), name="plone_context_state"
        )
        self.request.response.redirect(state.view_url())

    @button.buttonAndHandler(_("button_preview", default="Create preview"))
    def handlePreview(self, action):
        self.publish()
        IStatusMessage(self.request).add(
            _(
                "no_translate_link_preview_success",
                default=(
                    '${text_message_preview_success}: <a href="${url}">${url}</a>.'
                ),
                mapping={
                    "url": self.preview_url(),
                    "text_message_preview_success": _(
                        "message_preview_success",
                        default=(
                            "Successfully created a preview for the OiRA Tool. It can "
                            "be accessed at"
                        ),
                    ),
                },
            ),
            type="success",
        )
        state = getMultiAdapter(
            (aq_inner(self.context), self.request), name="plone_context_state"
        )
        self.request.response.redirect(state.view_url())
