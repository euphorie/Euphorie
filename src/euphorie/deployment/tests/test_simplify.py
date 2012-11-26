from euphorie.deployment.tests.functional import EuphorieTestCase


class SimplifiedPloneTests(EuphorieTestCase):
    def testRedirectStorageRemoved(self):
        from zope.component import queryUtility
        from plone.app.redirector.interfaces import IRedirectionStorage
        self.failUnless(queryUtility(IRedirectionStorage) is None)

    def testRedirectViewStillValid(self):
        from zope.component import queryMultiAdapter
        from plone.app.redirector.interfaces import IFourOhFourView
        from zope.interface.verify import verifyObject
        view = queryMultiAdapter(
                (self.portal, self.portal.REQUEST),
                name="plone_redirector_view")
        self.failUnless(verifyObject(IFourOhFourView, view))

# XXX Disabled for now: in Plone 4 the test setup loads all Plone zcml before
# the Euphorie test layer is setup, so the <exclude> directories in the
# euphorie.deployment zcml have no effect.
    def XtestNoContentRulesRegistered(self):
        # Testing for event subscribers would be the cleanest approach, but is
        # hard to do. Instead we test for extra marker interfaces set by the
        # plone.app.contentrules zcml.
        from plone.contentrules.engine.interfaces import IRuleAssignable
        self.failUnless(not IRuleAssignable.providedBy(self.portal))

    def testNoContentRulesAction(self):
        action = self.portal.portal_actions.object.contentrules
        self.assertEqual(action.visible, False)
