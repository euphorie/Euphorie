from euphorie.testing import EuphorieFunctionalTestCase
from plone.app.redirector.interfaces import IFourOhFourView
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.contentrules.engine.interfaces import IRuleAssignable
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface.verify import verifyObject


class SimplifiedPloneTests(EuphorieFunctionalTestCase):
    def testRedirectStorageRemoved(self):
        self.assertTrue(queryUtility(IRedirectionStorage) is None)

    def testRedirectViewStillValid(self):
        view = queryMultiAdapter(
            (self.portal, self.portal.REQUEST), name="plone_redirector_view"
        )
        self.assertTrue(verifyObject(IFourOhFourView, view))

    # XXX Disabled for now: in Plone 4 the test setup loads all Plone zcml before
    # the Euphorie test layer is setup, so the <exclude> directories in the
    # euphorie.deployment zcml have no effect.

    def XtestNoContentRulesRegistered(self):
        # Testing for event subscribers would be the cleanest approach, but is
        # hard to do. Instead we test for extra marker interfaces set by the
        # plone.app.contentrules zcml.
        self.assertTrue(not IRuleAssignable.providedBy(self.portal))

    def testNoContentRulesAction(self):
        action = self.portal.portal_actions.object.contentrules
        self.assertEqual(action.visible, False)
