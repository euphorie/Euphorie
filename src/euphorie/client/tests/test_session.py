import unittest
from euphorie.client.tests.database import DatabaseTests
from euphorie.client import session
from euphorie.client import model
from z3c.saconfig import Session

class Mock(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)



class CachingTests(unittest.TestCase):
    def callSession(self, request, manager):
        locals.request=request
        try:
            return manager.session
        finally:
            del locals.request
        

    def testCachedSession(self):
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.utils import locals
        request=testRequest()
        marker=[]
        request.other["euphorie.session"]=marker
        mgr=session.SessionManagerFactory()

        locals.request=request
        try:
            self.failUnless(mgr.session is marker)
        finally:
            del locals.request

    def testCachedSessionId(self):
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.utils import locals
        request=testRequest()
        marker=[]

        ses=Mock(id=marker)
        request.other["euphorie.session"]=ses
        mgr=session.SessionManagerFactory()
        locals.request=request
        try:
            self.failUnless(mgr.id is marker)
        finally:
            del locals.request



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
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.utils import locals

        request=testRequest()
        mgr=session.SessionManagerFactory()
        request.client=survey=object()
        locals.request=request
        try:
            account = model.Account(loginname="jane", password=u"john")
            mgr.start(u"Test session", survey, account)
            query=Session.query(model.SurveySession)
            self.assertEqual(query.count(), 1)
            s=query.first()
            self.assertEqual(s.title, u"Test session")
            self.failUnless("euphorie.session" in request.other)
            self.failUnless(request.other["euphorie.session"] is s)
        finally:
            del locals.request

