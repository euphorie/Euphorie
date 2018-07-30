# coding=utf-8
from Acquisition import aq_inner
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import utils
from euphorie.client.session import SessionManager
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize
from plone.supermodel import model
from Products.Five import BrowserView
from z3c.form.form import EditForm
from zope import schema
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class IStartFormSchema(model.Schema):
    title = schema.TextLine(
        title=_("Enter a name for your Risk Assessment"),
        required=True,
    )


class Start(AutoExtensibleForm, EditForm):
    """Survey start screen.

    This view shows basic introduction text and any extra information provided
    the sector if present. After viewing this page the user is forwarded to the
    profile page.

    View name: @@start
    """
    ignoreContext = True
    schema = IStartFormSchema

    @property
    def template(self):
        return self.index

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view(
            'webhelpers',
            self.context,
            self.request,
        )

    @property
    @memoize
    def has_profile(self):
        return len(self.context.ProfileQuestions())

    @memoize
    def has_introduction(self):
        survey = aq_inner(self.context)
        return utils.HasText(getattr(survey, "introduction", None))

    def update(self):
        super(Start, self).update()
        if self.request.environ["REQUEST_METHOD"] != "POST":
            return
        data, errors = self.extractData()
        if errors:
            return
        session = self.webhelpers.session
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
                type='success',
            )
        self.request.response.redirect(
            "%s/@@profile" % self.context.absolute_url()
        )


class PubblicationMenu(BrowserView):

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view(
            'webhelpers',
            self.context,
            self.request,
        )

    def notify_modified(self):
        notify(ObjectModifiedEvent(self.session))

    def redirect(self):
        target = (
            self.request.get('HTTP_REFERER') or self.context.absolute_url()
        )
        return self.request.response.redirect(target)

    def reset_date(self):
        ''' Reset the session date to now
        '''
        self.session.published = datetime.now()
        self.notify_modified()
        return self.redirect()

    def set_date(self):
        ''' Set the session date to now
        '''
        return self.reset_date()

    def unset_date(self):
        ''' Unset the session date
        '''
        self.session.published = None
        self.notify_modified()
        return self.redirect()

    @property
    @memoize
    def session(self):
        return SessionManager.session
