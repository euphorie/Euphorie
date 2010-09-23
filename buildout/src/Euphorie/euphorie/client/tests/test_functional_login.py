from euphorie.client.tests.functional import EuphorieClientTestCase

class RegisterTests(EuphorieClientTestCase):
    def afterSetUp(self):
        from zope.interface import alsoProvides
        from euphorie.client.interfaces import IClientSkinLayer
        super(RegisterTests, self).afterSetUp()
        self.loginAsPortalOwner()
        self.portal.invokeFactory("euphorie.client", "client")
        self.client=self.portal.client
        alsoProvides(self.client.REQUEST, IClientSkinLayer)

    def testConflictWithPloneAccount(self):
        view=self.client.restrictedTraverse("register")
        view.errors={}
        view.request.form["email"]=self.portal._owner[1]
        view.request.form["password1"]="secret"
        view.request.form["password2"]="secret"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

