# coding=utf-8
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import get_current_account
from plone.memoize.view import memoize
from Products.Five import BrowserView
from z3c.saconfig import Session
from zExceptions import Unauthorized


class SurveySessionsView(SessionsView):
    """Template corresponds to proto:_layout/tool.html"""

    variation_class = ""

    def set_language(self):
        utils.setLanguage(self.request, self.context, self.context.language)

    @property
    @memoize
    def sessions(self):
        """Given some sessions create a tree"""
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
        zodb_path = "%s/%s/%s" % (country.id, sector.id, self.context.id)
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
    """
    Browser view that displays the default introduction text for a Suvey.
    It is used when the Survey does not define its own introduction
    """

    pass
