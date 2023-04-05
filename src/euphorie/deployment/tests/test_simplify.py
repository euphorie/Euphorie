from euphorie.testing import EuphorieFunctionalTestCase
from plone.contentrules.engine.interfaces import IRuleAssignable


class SimplifiedPloneTests(EuphorieFunctionalTestCase):
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
