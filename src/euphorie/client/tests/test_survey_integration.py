# coding=utf-8
from datetime import datetime
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from lxml import html
from plone import api
from time import sleep
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


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

        with api.env.adopt_user(user=survey_session.account):
            with self._get_view(
                'publication_date', survey, survey_session
            ) as view:
                # The view is not callable but
                # has traversable allowed attributes
                self.assertRaises(TypeError, view)
                # We have some default values that will be changed
                # when publishing/unpublishing the session
                self.assertEqual(survey_session.last_publisher, None)
                self.assertEqual(survey_session.published, None)
                self.assertEqual(survey_session.last_modifier, None)
                self.assertEqual(survey_session.review_state, 'private')
                # Calling set_date will reult in having this session published
                # and the publication time and the publisher will be recorded
                # If no referer is set,
                # the methods will redirect to the context url
                self.assertEqual(
                    view.set_date(survey_session.id), survey.absolute_url())
                self.assertEqual(
                    survey_session.last_publisher, survey_session.account
                )
                self.assertIsInstance(survey_session.published, datetime)
                self.assertEqual(survey_session.review_state, 'published')
                old_modified = survey_session.modified
                old_published = survey_session.published
                # Changing the HTTP_REFERER will redirect there
                # and calling reset_date will update the published date
                view.request.set('HTTP_REFERER', 'foo')
                # We need to wait at least one second because the datetime
                # is stored with that accuracy
                sleep(1)
                self.assertEqual(view.reset_date(survey_session.id), 'foo')
                self.assertTrue(survey_session.modified > old_modified)
                self.assertEqual(
                    survey_session.last_publisher, survey_session.account
                )
                self.assertEqual(
                    survey_session.last_modifier, survey_session.account
                )
                self.assertTrue(survey_session.published > old_published)
                # Calling unset_date will restore the publication info
                self.assertEqual(view.unset_date(survey_session.id), 'foo')
                self.assertEqual(survey_session.last_publisher, None)
                self.assertEqual(survey_session.published, None)
                self.assertEqual(survey_session.review_state, 'private')

            # We also have a menu view
            with self._get_view(
                'publication_menu', survey, survey_session
            ) as view:
                soup = html.fromstring(view())
                self.assertListEqual(
                    ['publication_date/set_date?sessionid=1#content'],
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
                        'publication_date/unset_date?sessionid=1#content',
                        'publication_date/reset_date?sessionid=1#content',
                    ],
                    [
                        el.attrib['action'].rpartition('@@')[-1]
                        for el in soup.cssselect('form')
                    ],
                )

    def test_modify_updates_last_modifier(self):
        account = addAccount(password='secret')
        survey_session = model.SurveySession(
            title=u'Dummy session',
            account=account,
            zodb_path='',
        )
        self.assertEqual(survey_session.modified, None)
        self.assertEqual(survey_session.last_modifier, None)
        with api.env.adopt_user(user=account):
            notify(ObjectModifiedEvent(survey_session))
        self.assertIsInstance(survey_session.modified, datetime)
        self.assertEqual(survey_session.last_modifier, account)
