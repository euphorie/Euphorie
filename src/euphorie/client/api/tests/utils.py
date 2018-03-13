# coding=utf-8
from euphorie.client.profile import set_session_profile
from euphorie.client.session import create_survey_session
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY


def _setup_session(portal):
    addSurvey(portal, BASIC_SURVEY)
    survey = portal.client['nl']['ict']['software-development']
    account = addAccount(password='secret')
    survey_session = create_survey_session(u'Dummy session', survey, account)
    survey_session = set_session_profile(survey, survey_session, {})
    return (account, survey, survey_session)
