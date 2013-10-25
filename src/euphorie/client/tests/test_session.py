import unittest
from .database import DatabaseTests
from .test_update import TreeTests


class Mock(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class CachingTests(unittest.TestCase):
    def testCachedSession(self):
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.utils import setRequest
        from euphorie.client import session
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
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.utils import setRequest
        from euphorie.client import session
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
        import zope.component
        from Products.CMFCore.interfaces import ISiteRoot
        zope.component.provideUtility(self, ISiteRoot)

    def tearDown(self):
        from zope.testing.cleanup import cleanUp
        super(SessionCreationTests, self).tearDown()
        cleanUp()

    def testNewSession(self):
        import mock
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.utils import setRequest
        from euphorie.client import model
        from euphorie.client import session

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
        from ..utils import setRequest
        from .utils import testRequest
        setRequest(testRequest())
        super(SessionManagerFactoryTests, self).setUp()

    def tearDown(self):
        from ..utils import setRequest
        setRequest(None)
        super(SessionManagerFactoryTests, self).tearDown()

    def SessionManagerFactory(self, *a):
        from ..session import SessionManagerFactory
        return SessionManagerFactory(*a)

    def test_session_no_session_open(self):
        import mock
        from .. import model
        session = self.createSurveySession()
        with mock.patch('euphorie.client.session.SessionManagerFactory.id', new_callable=mock.PropertyMock) as mock_id:
            mock_id.return_value = None
            mgr = self.SessionManagerFactory()
            self.assertEqual(mgr.session, None)

    def test_session_valid_session_open(self):
        import mock
        from .. import model
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.SecurityManagement import setSecurityManager
        from AccessControl.SecurityManagement import newSecurityManager
        session = self.createSurveySession()
        with mock.patch('euphorie.client.session.SessionManagerFactory.id', new_callable=mock.PropertyMock) as mock_id:
            mock_id.return_value = session.id
            mgr = self.SessionManagerFactory()
            sm = getSecurityManager()
            try:
                newSecurityManager(None, session.account)
                self.assertTrue(mgr.session is session)
            finally:
                setSecurityManager(sm)

    def test_resume_enforce_same_account(self):
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.SecurityManagement import setSecurityManager
        from AccessControl.SecurityManagement import newSecurityManager
        from euphorie.client import model
        sm = getSecurityManager()
        mgr = self.SessionManagerFactory()
        victim = model.Account(loginname="test", password=u"test")
        attacker = model.Account(loginname="evil", password=u"layer")
        session = model.SurveySession(account=victim)
        try:
            newSecurityManager(None, attacker)
            self.assertRaises(ValueError, mgr.resume, session)
        finally:
            setSecurityManager(sm)
