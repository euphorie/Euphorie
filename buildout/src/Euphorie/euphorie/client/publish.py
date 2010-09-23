import datetime
import logging
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from zope.event import notify
from five import grok
from euphorie.content.survey import ISurvey
from euphorie.client import MessageFactory as _
from euphorie.client import utils
from euphorie.content.behaviour.publish import ObjectPublishedEvent
from zope.component import getMultiAdapter
from zope.component import getUtility
from z3c.appconfig.interfaces import IAppConfig
from z3c.form import button
from plone.directives import form
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plonetheme.nuplone.utils import getPortal

log = logging.getLogger(__name__)
grok.templatedir("templates")

def CopyToClient(survey, preview=False):
    """Copy the survey to the online client part of the site.

    :param survey: the survey to copy
    :param bool preview: indicates if this is a preview or a normal publication

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
    client=getPortal(survey).client

    source=aq_inner(survey)
    surveygroup=aq_parent(source)
    sector=aq_parent(surveygroup)
    country=aq_parent(sector)
    from euphorie.content.sector import ISector
    assert ISector.providedBy(sector)

    if country.id not in client:
        client.invokeFactory("euphorie.clientcountry", country.id, title=country.title)
    cl_country=client[country.id]

    if sector.id not in cl_country:
        cl_country.invokeFactory("euphorie.clientsector", sector.id)
    target=cl_country[sector.id]
    target.title=sector.title
    target.logo=sector.logo
    target.main_background_colour=getattr(sector, "main_colour", None)
    if target.main_background_colour:
        target.main_foreground_colour=utils.MatchColour(target.main_background_colour, 0.0, 0.6, 0.3)
        target.main_background_bright=utils.IsBright(target.main_background_colour)
    target.support_background_colour=getattr(sector, "support_colour", None)
    if target.support_background_colour:
        target.support_foreground_colour=utils.MatchColour(target.support_background_colour)
        target.support_background_bright=utils.IsBright(target.support_background_colour)

    copy=source._getCopy(target)
    if preview:
        copy.id="preview"
    else:
        copy.id=surveygroup.id
    copy.title=surveygroup.title
    copy.version=source.id
    copy.published=datetime.datetime.now()
    copy.preview=preview

    if copy.id in target:
        # We must suppress events to prevent the can-not-delete-published-
        # content check from blocking us.
        target._delObject(copy.id, suppress_events=True)

    target._setObject(copy.id, copy, suppress_events=True)
    copy=target[copy.id]
    copy._postCopy(target, op=0)

    notify(ObjectPublishedEvent(source))

    return copy


def PublishToClient(survey, preview=False):
    """Publish a survey in the online client part of the site.

    :param survey: the survey to copy
    :param bool preview: indicates if this is a preview or a normal publication

    This is a wrapper around :py:func:`CopyToClient`, which temporarily changes
    the currently active Zope user to make sure content can be created in the
    client.
    """
    pas=getToolByName(survey, "acl_users")
    clientuser=pas.getUserById("client")
    sm=getSecurityManager()
    try:
        newSecurityManager(None, clientuser)
        survey=CopyToClient(survey, False)
        now=datetime.datetime.now()
        survey.published=(survey.id, survey.title, datetime.datetime.now())
    finally:
        setSecurityManager(sm)



@grok.subscribe(ISurvey, IActionSucceededEvent)
def handleSurveyPublish(survey, event):
    """Event handler (subscriber) for succesfull workflow transitions for
    :py:obj:`ISurvey` objects. This handler copies the survey to the
    client.
    """
    if event.action not in [ "publish", "update"]:
        return

    PublishToClient(survey, False)




class PublishSurvey(form.Form):
    """Publish a survey.

    Publish a survey copies it from the content editing environment to the
    public client environment and makes several changes to prepare it for
    use by the client. The client environment is assumed to be located in
    a container with id ''client'' at the root of the site.
    """

    grok.context(ISurvey)
    grok.require("euphorie.client.PublishSurvey")
    grok.name("publish")
    grok.template("publish")

    preview = False


    def publish(self):
        survey=aq_inner(self.context)

        if self.preview:
            PublishToClient(survey, False)
        else:
            survey.published=datetime.datetime.now()
            wt=getToolByName(survey, "portal_workflow")
            state=wt.getInfoFor(survey, "review_state")
            if state=="draft":
                wt.doActionFor(survey, "publish")
            else:
                wt.doActionFor(survey, "update")

    def is_surveygroup_published(self):
        """Check if this surveygroup has been published before."""
        source=aq_inner(self.context)
        surveygroup=aq_parent(source)
        return bool(surveygroup.published)


    def is_this_survey_published(self):
        """Check if this survey is currently published."""
        source=aq_inner(self.context)
        surveygroup=aq_parent(source)
        return surveygroup.published==source.id


    def client_url(self):
        """Return the URL this survey will have after it is published."""
        config=getUtility(IAppConfig)
        client_url=config.get("euphorie", {}).get("client")
        if client_url:
            client_url=client_url.rstrip("/")
        else:
            client_url=getPortal(self.context).client.absolute_url()

        source=aq_inner(self.context)
        surveygroup=aq_parent(source)
        sector=aq_parent(surveygroup)
        country=aq_parent(sector)

        return "/".join([client_url, country.id, sector.id,
            "preview" if self.preview else surveygroup.id])




    @button.buttonAndHandler(_(u"button_cancel", default=u"Cancel"))
    def handleCancel(self, action):
        state=getMultiAdapter((aq_inner(self.context), self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())


    @button.buttonAndHandler(_(u"button_publish", default=u"Publish"))
    def handlePublish(self, action):
        self.publish()
        IStatusMessage(self.request).addStatusMessage(
                _(u"Succesfully published the survey"), type="success")
        state=getMultiAdapter((aq_inner(self.context), self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())



class PreviewSurvey(PublishSurvey):
    """Generate a preview for a survey. A preview is exactly like a normally
    published survey, except for two differences: there can only be one preview
    for a sector, which has the id `preview`, and after previewing the user is
    redirected to the preview instead of the original context.
    """
    grok.name("preview")

    def __call__(self):
        self.publish(preview=True)
        config=getUtility(IAppConfig)

        preview_url=self.copy[0].absolute_url()
        admin_client_url=getPortal(self.context).client.absolute_url()
        client_url=config["euphorie"]["client"]
        if client_url.endswith("/"):
            client_url=client_url[:-1]
        preview_url=preview_url.replace(admin_client_url, client_url)


        self.request.response.redirect(preview_url)

