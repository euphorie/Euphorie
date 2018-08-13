# coding=utf-8
"""
Country
-------

The main view after login, to list existing sessions, start new sessions,
delete & rename sessions

URL: https://client-oiranew.syslab.com/eu
"""

from .. import MessageFactory as _
from AccessControl import getSecurityManager
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import SurveySession
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from Products.statusmessages.interfaces import IStatusMessage
from sqlalchemy.orm import object_session
from z3c.form import button
from z3c.saconfig import Session
from zope import schema
from zope.interface import directlyProvides
from zope.interface import implementer

import logging


grok.templatedir("templates")

log = logging.getLogger(__name__)


class IClientCountry(form.Schema, IBasic):
    """Country grouping in the online client.
    """


@implementer(IClientCountry)
class ClientCountry(dexterity.Container):

    country_type = None


class DeleteSession(grok.View):
    """View name: @@delete-session
    """
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("delete-session")

    def render(self):
        session = Session()
        ss = session.query(SurveySession).get(self.request.form["id"])
        if ss is not None:
            flash = IStatusMessage(self.request).addStatusMessage
            flash(
                _(
                    u"Session `${name}` has been deleted.",
                    mapping={
                        "name": getattr(ss, 'title')
                    }
                ), "success"
            )
            session.delete(ss)
        self.request.response.redirect(self.context.absolute_url())


class RenameSessionSchema(form.Schema):
    title = schema.TextLine(required=False)


class RenameSession(form.SchemaForm):
    """View name: @@rename-session
    """
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("rename-session")
    grok.template("rename-session")
    form.wrap(False)

    schema = RenameSessionSchema

    def getContent(self):
        try:
            session_id = int(self.request.get("id"))
        except (ValueError, TypeError):
            raise KeyError("Invalid session id")
        user = getSecurityManager().getUser()
        session = (
            object_session(user).query(SurveySession)
            .filter(SurveySession.account == user)
            .filter(SurveySession.id == session_id).first()
        )
        if session is None:
            raise KeyError("Unknown session id")
        self.original_title = session.title
        directlyProvides(session, RenameSessionSchema)
        return session

    @button.buttonAndHandler(_(u"Save"))
    def handleSave(self, action):
        (data, errors) = self.extractData()
        if errors:
            return
        if data["title"]:
            flash = IStatusMessage(self.request).addStatusMessage
            self.getContent().title = data['title']
            flash(
                _(
                    u"Session title has been changed to ${name}",
                    mapping={
                        "name": data["title"]
                    }
                ), "success"
            )
        came_from = self.request.form.get("came_from")
        if isinstance(came_from, list):
            # If came_from is both in the querystring and the form data
            came_from = came_from[0]
        if came_from:
            self.request.response.redirect(came_from)
        else:
            self.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        self.response.redirect(self.context.absolute_url())
