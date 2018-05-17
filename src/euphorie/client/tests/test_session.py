from .. import model
from ..session import SessionManagerFactory
from ..utils import setRequest
from .database import DatabaseTests
from .test_update import TreeTests
from .utils import testRequest
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from euphorie.client import session
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from zope.testing.cleanup import cleanUp

import mock
import unittest
import zope.component


class Mock(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)


class CachingTests(unittest.TestCase):

    def testCachedSession(self):
        request = testRequest()
        marker = []
        request.other["euphorie.session"] = marker
        mgr = session.SessionManagerFactory()

        setRequest(request)
        try:
            self.failUnless(mgr.session is marker)
        finally:
            setRequest(None)

    def testCachedSessionId(self):
        request = testRequest()
        marker = []
        ses = Mock(id=marker)
        request.other["euphorie.session"] = ses
        mgr = session.SessionManagerFactory()
        setRequest(request)
        try:
            self.failUnless(mgr.id is marker)
        finally:
            setRequest(None)


class SessionCreationTests(DatabaseTests):

    def setUp(self):
        super(SessionCreationTests, self).setUp()
        zope.component.provideUtility(self, ISiteRoot)

    def tearDown(self):
        super(SessionCreationTests, self).tearDown()
        cleanUp()

    def testNewSession(self):

        request = testRequest()
        mgr = session.SessionManagerFactory()
        request.client = survey = object()
        setRequest(request)
        try:
            account = model.Account(loginname="jane", password=u"john")
            with mock.patch('euphorie.client.session.create_survey_session') \
                    as mock_create:
                survey_session = mock.Mock()
                survey_session.id = 43
                mock_create.return_value = survey_session
                ses = mgr.start(u"Test session", survey, account)
                self.assertTrue(ses is survey_session)
                self.failUnless(request.other["euphorie.session"] is ses)
        finally:
            setRequest(None)


class SessionManagerFactoryTests(TreeTests):

    def setUp(self):
        setRequest(testRequest())
        super(SessionManagerFactoryTests, self).setUp()

    def tearDown(self):
        setRequest(None)
        super(SessionManagerFactoryTests, self).tearDown()

    def SessionManagerFactory(self, *a):
        return SessionManagerFactory(*a)

    def test_session_no_session_open(self):
        with mock.patch(
            'euphorie.client.session.SessionManagerFactory.id',
            new_callable=mock.PropertyMock
        ) as mock_id:
            mock_id.return_value = None
            mgr = self.SessionManagerFactory()
            self.assertEqual(mgr.session, None)

    def test_session_valid_session_open(self):
        session = self.createSurveySession()
        with mock.patch(
            'euphorie.client.session.SessionManagerFactory.id',
            new_callable=mock.PropertyMock
        ) as mock_id:
            mock_id.return_value = session.id
            mgr = self.SessionManagerFactory()
            sm = getSecurityManager()
            try:
                newSecurityManager(None, session.account)
                self.assertTrue(mgr.session is session)
            finally:
                setSecurityManager(sm)

    def test_resume_enforce_same_account(self):
        mgr = self.SessionManagerFactory()
        victim = model.Account(loginname="test", password=u"test")
        attacker = model.Account(loginname="evil", password=u"layer")
        session = model.SurveySession(account=victim)
        with self._get_view('webhelpers', self.portal):
            with api.env.adopt_user(user=attacker):
                self.assertRaises(ValueError, mgr.resume, session)
