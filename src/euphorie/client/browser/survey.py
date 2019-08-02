# coding=utf-8
from Acquisition import aq_inner
from euphorie.client import utils
from euphorie.client.browser.country import SessionsView
from plone.memoize.view import memoize


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
