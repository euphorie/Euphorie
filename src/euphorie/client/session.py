"""
Session
-------

Create survey sessions.
"""

from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client import model
from euphorie.content.survey import ISurvey
from z3c.saconfig import Session
from zope.component import adapter
from zope.interface import Interface


class ISurveySessionCreator(Interface):
    """ Provides creation of a new survey session
    """


@adapter(ISurvey, Interface)
class SurveySessionCreator(object):

    model = model.SurveySession

    def __init__(self, survey, request):
        self.survey = survey
        self.request = request

    def create(self, title, account=None, **params):
        """Create a new survey session.

        :param title: title for the new session.
        :type title: unicode
        :param survey: survey for which the session is being created
        :type survey: :py:class:`euphorie.content.survey.Survey`
        :rtype: :py:class:`euphorie.client.model.SurveySession` instance
        """
        if account is None:
            account = model.get_current_account()

        session = Session()
        sector = aq_parent(aq_inner(self.survey))
        country = aq_parent(sector)
        zodb_path = '%s/%s/%s' % (country.id, sector.id, self.survey.id)
        survey_session = self.model(
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


__all__ = ["SurveySessionCreator"]
