from euphorie import MessageFactory as _
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import get_current_account
from euphorie.client.utils import CreateEmailTo
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from z3c.saconfig import Session
from zExceptions import Unauthorized

import logging
import smtplib


logger = logging.getLogger(__name__)


class SurveySessionsView(SessionsView):
    """Template corresponds to proto:_layout/tool.html."""

    variation_class = ""

    def set_language(self):
        utils.setLanguage(self.request, self.context, self.context.language)

    @property
    @memoize
    def sessions(self):
        """Given some sessions create a tree."""
        return self.webhelpers.get_sessions_query(context=self.context).all()

    def create_survey_session(self, title, account=None, **params):
        """Create a new survey session.

        :param title: title for the new survey session.
        :type title: unicode
        :rtype: :py:class:`cls.survey_session_model` instance
        """
        if account is None:
            account = get_current_account()

        session = Session()
        sector = self.context.aq_parent
        country = sector.aq_parent
        zodb_path = f"{country.id}/{sector.id}/{self.context.id}"
        survey_session = self.survey_session_model(
            title=title,
            zodb_path=zodb_path,
            account_id=account.id,
            group_id=account.group_id,
        )
        for key in params:
            setattr(survey_session, key, params[key])
        session.add(survey_session)
        session.refresh(account)
        session.flush()  # flush so we get a session id
        return survey_session

    def __call__(self):
        if not self.account:
            raise Unauthorized()
        self.set_language()
        return self.index()


class SurveySessionsViewAnon(SurveySessionsView):
    def __call__(self):
        self.set_language()
        return self.index()


class DefaultIntroductionView(BrowserView):
    """Browser view that displays the default introduction text for a Suvey.

    It is used when the Survey does not define its own introduction
    """

    pass


class EmailReminder(BrowserView):
    """View that allows sending a reminder email with a link to the session"""

    variation_class = "variation-risk-assessment"
    email_template = ViewPageTemplateFile("templates/email_reminder_body.pt")

    def send_email(self):
        start_url = f"{self.context.absolute_url()}/@@start"
        body = self.email_template(
            tool_name=self.context.aq_parent.title, url=start_url
        )
        subject = api.portal.translate(_("OiRA tool reminder"))
        account = get_current_account()
        email_from_name = api.portal.get_registry_record("plone.email_from_name")
        email_from_address = api.portal.get_registry_record("plone.email_from_address")
        mail = CreateEmailTo(
            email_from_name,
            email_from_address,
            account.email,
            subject,
            body,
        )
        try:
            api.portal.send_email(
                body=mail,
                subject=subject,
                recipient=account.email,
                immediate=True,
            )
            logger.info(
                "Sent email reminder to %s",
                account.email,
            )
        except MailHostError as e:
            return self.log_error(
                "MailHost error sending email reminder to %s: %s", account.email, e
            )
        except smtplib.SMTPException as e:
            return self.log_error(
                "smtplib error sending email reminder to %s: %s", account.email, e
            )
        except OSError as e:
            return self.log_error(
                "Socket error sending email reminder to %s: %s", account.email, e[1]
            )
        api.portal.show_message("Email reminder has been sent", type="info")
        return self.request.response.redirect(start_url)

    def __call__(self):
        if self.request.method == "POST":
            self.send_email()
        return super().__call__()
