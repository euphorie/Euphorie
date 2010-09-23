import binascii
import unittest
from euphorie.client.tests.database import DatabaseTests
from euphorie.client import session
from euphorie.client import model
from zope.testing.cleanup import CleanUp
from z3c.saconfig import Session


class Mock:
    def __init__(self, **kw):
        self.__dict__.update(kw)

class MockRequest:
    url=None
    def __init__(self, cookie=None):
        self.other={}
        if cookie is None:
            self.cookies={}
        else:
            self.cookies=dict(euphorie=cookie)

    def redirect(self, url):
        self.url=url

    @property
    def response(self):
        return self

    def setCookie(self, name, value, **kw):
        self.name=name
        self.value=value
        self.kw=kw


class SessionTests(CleanUp):
    def setUp(self):
        super(SessionTests, self).setUp()
        import zope.component
        from Products.CMFCore.interfaces import ISiteRoot
        zope.component.provideUtility(self, ISiteRoot)

    def setRequest(self, request):
        import euphorie.client.utils
        euphorie.client.utils.locals.request=request
        


class CachingTests(SessionTests):
    def testCachedSession(self):
        self.setRequest(MockRequest())
        marker=[]
        self.request.other["euphorie.session"]=marker
        mgr=session.SessionManagerFactory()
        self.failUnless(mgr.session is marker)

    def testCachedSessionId(self):
        self.setRequest(MockRequest())
        marker=[]
        ses=Mock(id=marker)
        self.request.other["euphorie.session"]=ses
        mgr=session.SessionManagerFactory()
        self.failUnless(mgr.id is marker)



class CookieTests(SessionTests):
    def testNoCookie(self):
        self.setRequest(MockRequest())
        mgr=session.SessionManagerFactory()
        self.failUnless(mgr.id is None)

    def testBadBase64(self):
        self.setRequest(MockRequest("invalid"))
        mgr=session.SessionManagerFactory()
        self.failUnless(mgr.id is None)

    def testInvalidFormat(self):
        self.setRequest(MockRequest(binascii.b2a_base64("invalid").rstrip()))
        mgr=session.SessionManagerFactory()
        self.failUnless(mgr.id is None)

    def testInvalidSignature(self):
        self.setRequest(MockRequest(binascii.b2a_base64("1 invalid").rstrip()))
        mgr=session.SessionManagerFactory()
        self.failUnless(mgr.id is None)

    def testInvalidNumber(self):
        mgr=session.SessionManagerFactory()
        signature=mgr._GenerateSignature("A")
        self.setRequest(MockRequest(binascii.b2a_base64("A %s" % signature).rstrip()))
        self.failUnless(mgr.id is None)

    def testValidSignature(self):
        mgr=session.SessionManagerFactory()
        signature=mgr._GenerateSignature(1)
        self.setRequest(MockRequest(binascii.b2a_base64("1 %s" % signature).rstrip()))
        self.assertEqual(mgr.id, 1)


class SessionCreationTests(DatabaseTests, SessionTests):
    def setUp(self):
        SessionTests.setUp(self)
        DatabaseTests.setUp(self)

    def tearDown(self):
        DatabaseTests.tearDown(self)
        SessionTests.tearDown(self)

    def testNewSession(self):
        request=MockRequest()
        mgr=session.SessionManagerFactory()
        request.client=survey=object()
        self.setRequest(request)
        account = model.Account(loginname="jane", password=u"john")
        mgr.start(u"Test session", survey, account)
        query=Session.query(model.SurveySession)
        self.assertEqual(query.count(), 1)
        s=query.first()
        self.assertEqual(s.title, u"Test session")
        self.failUnless("euphorie.session" in request.other)
        self.failUnless(request.other["euphorie.session"] is s)



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

