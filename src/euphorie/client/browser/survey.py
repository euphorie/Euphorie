# coding=utf-8
from Acquisition import aq_inner
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import get_current_account
from euphorie.client.model import SurveySession
from plone.memoize.view import memoize
from z3c.saconfig import Session


class SurveySessionsView(SessionsView):
    """ Template corresponds to proto:_layout/tool.html
    """

    variation_class = ""

    @memoize
    def get_sessions(self):
        """ Filter user's sessions to match only those from the current survey
        """
        sessions = super(SurveySessionsView, self).get_sessions()
        survey = aq_inner(self.context)
        my_path = utils.RelativePath(self.request.client, survey)
        my_sessions = sorted(
            [x for x in sessions if x.zodb_path == my_path],
            key=lambda s: s.modified,
            reverse=True,
        )
        return my_sessions

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
        zodb_path = '%s/%s/%s' % (country.id, sector.id, self.context.id)
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
