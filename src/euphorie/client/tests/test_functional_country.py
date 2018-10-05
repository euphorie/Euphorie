# coding=utf-8
from ..model import Account
from ..model import Group
from ..model import SurveySession
from AccessControl.SecurityManagement import newSecurityManager
from anytree import RenderTree
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from z3c.saconfig import Session

import datetime
import urllib


class CountryTests(EuphorieIntegrationTestCase):

    maxDiff = None

    def test_sessions_ordering(self):
        addSurvey(self.portal, BASIC_SURVEY)
        session = Session()
        account = Account(
            loginname='johny',
            sessions=[
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'One',
                    modified=datetime.datetime(2012, 12, 10)
                ),
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'Three',
                    modified=datetime.datetime(2012, 12, 12)
                ),
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'Two',
                    modified=datetime.datetime(2012, 12, 11)
                )
            ]
        )
        session.add(account)
        newSecurityManager(None, account)
        with self._get_view('view', self.portal.client['nl']) as view:
            root = view.get_sessions_tree_root()
            self.assertListEqual(
                [x.title for x in root.descendants],
                [u'Software development', u'One', u'Three', u'Two'],
            )

            survey = root.children[0]
            # Ensure that the nodes are sorted by title
            # when getting the groups...
            self.assertListEqual(
                [x.title for x in survey.groups],
                [u'One', u'Three', u'Two'],
            )
            # ... or by reversed modification date when getting the sessions
            self.assertListEqual(
                [x.title for x in survey.sessions],
                [u'Three', u'Two', 'One'],
            )

    def test_complex_tree(self):
        # First we create a couple of surveys
        ANOTHER_BASIC_SURVEY = BASIC_SURVEY.replace(
            'Software development', 'Hardware development'
        )
        addSurvey(self.portal, BASIC_SURVEY)
        addSurvey(self.portal, ANOTHER_BASIC_SURVEY)

        # Then we create our group hierarchy
        session = Session()
        group1 = Group(group_id='1', short_name=u'Group 1')
        session.add(group1)
        group2 = Group(group_id='2', short_name=u'Group 2')
        session.add(group2)
        group2.parent = group1

        john = Account(
            loginname='john',
            sessions=[
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'John SW Group 1',
                    modified=datetime.datetime(2012, 12, 10),
                    group_id=group1.group_id,
                ),
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'John SW Group 2',
                    modified=datetime.datetime(2012, 12, 12),
                    group_id=group2.group_id,
                ),
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'John SW No group',
                    modified=datetime.datetime(2012, 12, 11),
                ),
            ]
        )
        john.group = group1
        jane = Account(
            loginname='jane',
            sessions=[
                SurveySession(
                    zodb_path='nl/ict-1/hardware-development',
                    title=u'Jane HW No group',
                    modified=datetime.datetime(2011, 12, 10)
                ),
                SurveySession(
                    zodb_path='nl/ict-1/hardware-development',
                    title=u'Jane HW Group 2',
                    modified=datetime.datetime(2011, 12, 12),
                    group_id=group2.group_id,
                ),
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'Jane SW Group 2',
                    modified=datetime.datetime(2011, 12, 11),
                    group_id=group2.group_id,
                ),
                SurveySession(
                    zodb_path='nl/ict/software-development',
                    title=u'Jane SW Group 2 (another one)',
                    modified=datetime.datetime(2011, 12, 12),
                    group_id=group2.group_id,
                ),
            ]
        )
        jane.group = group2
        session.add(john)
        session.add(jane)

        # By default John can see his sessions
        newSecurityManager(None, john)
        with self._get_view('view', self.portal.client['nl']) as view:
            root = view.get_sessions_tree_root()
            self.assertListEqual(
                RenderTree(root).by_attr("title").splitlines(),
                [
                    u'',
                    u'├── Group 1 (1)',
                    u'│   ├── Software development',
                    u'│   │   └── John SW Group 1',
                    u'│   └── Group 2 (2)',
                    u'│       └── Software development',
                    u'│           └── John SW Group 2',
                    u'└── Software development',
                    u'    └── John SW No group',
                ],
            )

        # but he can also see Jane's ones that have been filed its groups
        with self._get_view('view', self.portal.client['nl']) as view:
            view.request.set('scope', 'all')
            root = view.get_sessions_tree_root()
            self.assertListEqual(
                RenderTree(root).by_attr("title").splitlines(),
                [
                    u'',
                    u'├── Group 1 (1)',
                    u'│   ├── Software development',
                    u'│   │   └── John SW Group 1',
                    u'│   └── Group 2 (2)',
                    u'│       ├── Software development',
                    u'│       │   ├── John SW Group 2',
                    u'│       │   ├── Jane SW Group 2',
                    u'│       │   └── Jane SW Group 2 (another one)',
                    u'│       └── Hardware development',
                    u'│           └── Jane HW Group 2',
                    u'└── Software development',
                    u'    └── John SW No group',
                ],
            )
        # Jane can see her Sessions by default
        newSecurityManager(None, jane)
        with self._get_view('view', self.portal.client['nl']) as view:
            root = view.get_sessions_tree_root()
            self.assertListEqual(
                RenderTree(root).by_attr("title").splitlines(),
                [
                    u'',
                    u'├── Hardware development',
                    u'│   └── Jane HW No group',
                    u'└── Group 1 (1)',
                    u'    └── Group 2 (2)',
                    u'        ├── Hardware development',
                    u'        │   └── Jane HW Group 2',
                    u'        └── Software development',
                    u'            ├── Jane SW Group 2',
                    u'            └── Jane SW Group 2 (another one)',
                ],
            )
        # but cannot acquire John's sessions in group1
        # (although she can if the session is in group2)
        with self._get_view('view', self.portal.client['nl']) as view:
            view.request.set('scope', 'all')
            root = view.get_sessions_tree_root()
            self.assertListEqual(
                RenderTree(root).by_attr("title").splitlines(),
                [
                    u'',
                    u'├── Hardware development',
                    u'│   └── Jane HW No group',
                    u'└── Group 1 (1)',
                    u'    └── Group 2 (2)',
                    u'        ├── Hardware development',
                    u'        │   └── Jane HW Group 2',
                    u'        └── Software development',
                    u'            ├── Jane SW Group 2',
                    u'            ├── Jane SW Group 2 (another one)',
                    u'            └── John SW Group 2',
                ],
            )


class CountryFunctionalTests(EuphorieFunctionalTestCase):

    def test_surveys_filtered_by_language(self):
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector</title>
                      <survey>
                        <title>Survey</title>
                        <language>en</language>
                      </survey>
                    </sector>"""
        survey_nl = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Branche</title>
                    <survey>
                      <title>Vragenlijst</title>
                      <language>nl</language>
                    </survey>
                  </sector>"""  # noqa
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        addSurvey(self.portal, survey_nl)
        browser = self.get_browser()
        # Pass the language as URL parameter to ensure that we get the NL
        # version
        browser.open("%s?language=nl" % self.portal.client.absolute_url())
        registerUserInClient(browser, link="Registreer")
        # Note, this used to test that the URL was that of the client,
        # in the correct country (nl), with `?language=nl-NL` appended.
        # I don't see where in the code this language URL parameter would
        # come from, so I remove it in this test as well.
        self.assertEqual(browser.url, "http://nohost/plone/client/nl")
        self.assertEqual(
            browser.getControl(name="survey").options, ["branche/vragenlijst"]
        )
        browser.open(
            "%s?language=en" % self.portal.client["nl"].absolute_url()
        )
        self.assertEqual(
            browser.getControl(name="survey").options, ["sector/survey"]
        )

    def test_must_select_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        browser.open(self.portal.client['nl'].absolute_url())
        registerUserInClient(browser)
        data = urllib.urlencode({
            'action': 'new',
            'survey': '',
            'title:utf8:ustring': 'Foo'
        })
        browser.handleErrors = False
        browser.open(browser.url, data)
        self.assertEqual(browser.url, 'http://nohost/plone/client/nl')
