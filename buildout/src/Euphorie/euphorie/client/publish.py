import datetime
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from zope.event import notify
from Products.Five.browser import BrowserView
from plone.dexterity.interfaces import IDexterityContainer
from euphorie.client import MessageFactory as _
from euphorie.client import utils
from euphorie.content.behaviour.deprecation import IDeprecatable
from euphorie.content.behaviour.publish import ObjectPublishedEvent
from zope.component import getUtility
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage



class PublishSurvey(BrowserView):
    """Publish a survey.

    Publish a survey copies it from the content editing environment to the
    public client environment and makes several changes to prepare it for
    use by the client. The client environment is assumed to be located in
    a container with id ''client'' at the root of the site.
    """

    preview = False

    def CopyToPublicArea(self):
        """Copy the survey to the public area.

        The public area is hardcoded to be a container with id `client`
        within the site root.

        The ''id'' and ''title'' of the survey group will be used for the
        published survey. If another object with the same ''id'' already exists
        it will be removed first. Any missing country and sector folders are
        created if needed.

        Returns the new public survey instance.
        """
        # This is based on OFS.CopyContainer.manage_clone, modified to
        # use the sector id and title, skip security checks and remove
        # an existing object with the same id.

        client=getUtility(ISiteRoot).client

        source=aq_inner(self.context)
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
            target.main_foreground_colour=utils.MatchColour(target.main_background_colour)
            target.main_background_bright=utils.IsBright(target.main_background_colour)
        target.support_background_colour=getattr(sector, "support_colour", None)
        if target.support_background_colour:
            target.support_foreground_colour=utils.MatchColour(target.support_background_colour)
            target.support_background_bright=utils.IsBright(target.support_background_colour)

        copy=source._getCopy(target)
        if self.preview:
            copy.id="preview"
        else:
            copy.id=surveygroup.id
        copy.title=surveygroup.title
        copy.language=surveygroup.language
        copy.published=datetime.datetime.now()
        copy.preview=self.preview

        if copy.id in target:
            # We must suppress events to prevent the can-not-delete-published-
            # content check from blocking us.
            target._delObject(copy.id, suppress_events=True)

        target._setObject(copy.id, copy)
        copy=target[copy.id]
        copy._postCopy(target, op=0)

        notify(ObjectPublishedEvent(source))

        return copy


    def IsDeprecated(self, obj):
        info=IDeprecatable(obj, None)
        if info is None:
            return False
        return info.deprecated



    def Update(self, root):
        """Update all items in a survey being published.

        This process does several things:

        * all deprecated items are removed
        """
        for (key,item) in root.items():
            if self.IsDeprecated(item):
                del root[key]
                continue

            if IDexterityContainer.providedBy(item):
                self.Update(item)


    def getClientUser(self):
        pas=getToolByName(self.context, "acl_users")
        return pas.getUserById("client")


    def __call__(self):
        sm=getSecurityManager()
        try:
            newSecurityManager(None, self.getClientUser())
            survey=self.CopyToPublicArea()
            self.copy=[survey]
            self.Update(survey)
            IStatusMessage(self.request).addStatusMessage(
                    _(u"Succesfully published the survey"), type="info")
            state=getMultiAdapter((aq_inner(self.context), self.request), name="plone_context_state")
            self.request.response.redirect(state.view_url())
        finally:
            setSecurityManager(sm)



class PreviewSurvey(PublishSurvey):
    """Generate a preview for a survey. A preview is exactly like a normally
    published survey, except for two differences: there can only be one preview
    for a sector, which has the id `preview`, and after previewing the user is
    redirected to the preview instead of the original context.
    """

    preview = True

    def __call__(self):
        super(PreviewSurvey, self).__call__()
        self.request.response.redirect(aq_inner(self.copy[0]).absolute_url())

