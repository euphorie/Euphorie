from ..session import SessionManagerFactory
from ..utils import setRequest
from .test_update import TreeTests
from .utils import testRequest
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from euphorie.client import session
from plone import api

import mock
import unittest


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


    # XXX
    #
    # This test uses the session manager and is obsolete.
    # Replacement??
    #
    # def test_resume_enforce_same_account(self):
    #     mgr = self.SessionManagerFactory()
    #     victim = model.Account(loginname="test", password=u"test")
    #     attacker = model.Account(loginname="evil", password=u"layer")
    #     session = model.SurveySession(account=victim)
    #     with self._get_view('webhelpers', self.portal):
    #         with api.env.adopt_user(user=attacker):
    #             self.assertRaises(ValueError, mgr.resume, session)
