# coding=utf-8
from Acquisition import aq_inner
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import get_current_account
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.supermodel import model
from Products.Five import BrowserView
from z3c.form.form import EditForm
from zope import schema
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent


class IStartFormSchema(model.Schema):
    title = schema.TextLine(
        title=_(
            "label_session_title",
            default=u"Enter a title for your Risk Assessment"),
        required=True,
    )


class SurveySessionsView(SessionsView):
    """ Template corresponds to proto:_layout/tool.html
    """

    @memoize
    def get_sessions(self):
        """ Filter user's sessions to match only those from the current survey
        """
        sessions = super(SurveySessionsView, self).get_sessions()
        survey = aq_inner(self.context)
        my_path = utils.RelativePath(self.request.client, survey)
        my_sessions = [x for x in sessions if x.zodb_path == my_path]
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
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.message_required = translate(
            _(
                u"message_field_required",
                default=u"Please fill out this field."
            ),
            target_language=lang
        )
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
        # Optimize: if the form was auto-submitted, we know that we want to
        # show the "start" page again
        if "form.button.submit" not in self.request:
            self.request.response.redirect(
                "%s/@@start" % self.context.absolute_url()
            )
        else:
            self.request.response.redirect(
                "%s/@@profile" % self.context.absolute_url()
            )


class PublicationMenu(BrowserView):

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view(
            'webhelpers',
            self.context,
            self.request,
        )

    @property
    @memoize_contextless
    def portal(self):
        ''' The currenttly authenticated account
        '''
        return api.portal.get()

    def notify_modified(self, session):
        notify(ObjectModifiedEvent(session))

    def redirect(self):
        target = (
            self.request.get('HTTP_REFERER') or self.context.absolute_url()
        )
        return self.request.response.redirect(target)

    def reset_date(self, sessionid):
        ''' Reset the session date to now
        '''
        session = self.session(sessionid)
        session.published = datetime.now()
        session.last_publisher = get_current_account()
        self.notify_modified(session)
        return self.redirect()

    def set_date(self, sessionid):
        ''' Set the session date to now
        '''
        return self.reset_date(sessionid)

    def unset_date(self, sessionid):
        ''' Unset the session date
        '''
        session = self.session(sessionid)
        session.published = None
        session.last_publisher = None
        self.notify_modified(session)
        return self.redirect()

    @memoize
    def session(self, sessionid):
        return self.webhelpers.session_by_id(sessionid)
        # return SessionManager.session
