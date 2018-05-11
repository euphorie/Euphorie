# coding=utf-8
from datetime import datetime
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from lxml import html
from time import sleep


class TestSurveyViews(EuphorieIntegrationTestCase):

    def test_survey_publication_date_views(self):
        ''' We have some views to display and set the published column
        for a survey session
        '''
        survey = addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = model.SurveySession(
            title=u'Dummy session',
            created=datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime(2012, 4, 23, 11, 50, 30),
            zodb_path='nl/ict/software-development',
            account=account,
            company=model.Company(
                country='nl', employees='1-9', referer='other'
            )
        )
        model.Session.add(survey_session)
        survey = self.portal.client.nl.ict['software-development']

        with self._get_view(
            'publication_date', survey, survey_session
        ) as view:  # noqa: E501
            session = view.session
            # The view is not callable but as traversable  allowed attributes
            self.assertRaises(TypeError, view)
            self.assertEqual(session.published, None)
            self.assertEqual(session.review_state, 'private')
            # Calling set_date will reult in having this session published
            # and the publication time will be recorded
            # If no referer is set the methods will redirect to the context url
            self.assertEqual(view.set_date(), survey.absolute_url())
            self.assertIsInstance(session.published, datetime)
            self.assertEqual(session.review_state, 'published')
            old_published = session.published
            # Changing the HTTP_REFERER will redirect there
            # and calling reset_date will update the published date
            view.request.set('HTTP_REFERER', 'foo')
            # We need to wait at least one second because the datetime
            # is stored with that accuracy
            sleep(1)
            self.assertEqual(view.reset_date(), 'foo')
            self.assertTrue(session.published > old_published)
            # Calling unset_date will restore the publication date to None
            self.assertEqual(view.unset_date(), 'foo')
            self.assertEqual(session.published, None)
            self.assertEqual(session.review_state, 'private')

        # We also have a menu view
        with self._get_view(
            'publication_menu', survey, survey_session
        ) as view:  # noqa: E501
            soup = html.fromstring(view())
            self.assertListEqual(
                ['publication_date/set_date#content'],
                [
                    el.attrib['action'].rpartition('@@')[-1]
                    for el in soup.cssselect('form')
                ],
            )
            # We trigger the session to be private
            survey_session.published = 'foo'
            soup = html.fromstring(view())
            self.assertListEqual(
                [
                    'publication_date/unset_date#content',
                    'publication_date/reset_date#content',
                ],
                [
                    el.attrib['action'].rpartition('@@')[-1]
                    for el in soup.cssselect('form')
                ],
            )
