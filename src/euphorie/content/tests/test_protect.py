from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from z3c.saconfig import Session
from zope.interface import alsoProvides

import transaction


class BaseProtectTestCase(EuphorieIntegrationTestCase):
    """setUp and methods used by the integration and functional test case."""

    def setUp(self):
        from euphorie.content.protect import EuphorieProtectTransform

        super().setUp()
        # The transform wants a 'published' and a 'request'.
        # 'published' can be a view.  But really it is ignored, so let's take
        # the portal.
        self.transform = EuphorieProtectTransform(self.portal, self.request)
        self.session = Session()
        self._latest_group_id = 0
        self.group_id = None

    def _createItem(self):
        """Create an SQL item.

        At first I tried a SurveyTreeItem, but eventually ran into problems
        because this would then automagically create a related Risk or Module.
        A session flush in test_edit_with_flush in the functional test case
        would fail with:

            sqlalchemy.orm.exc.ObjectDeletedError: Instance '<Risk at ...>'
            has been deleted, or its row is otherwise not present.

        This error seems unrelated to what we are trying to test here.
        So I try a simpler model.
        """
        from euphorie.client.model import Group

        # There are several constraints we need to satisfy.
        self._latest_group_id += 1
        group_id = str(self._latest_group_id)
        return Group(group_id=group_id)

    def _getItem(self, group_id=None):
        from euphorie.client.model import Group

        group_id = group_id or self.group_id
        return self.session.query(Group).filter(Group.group_id == group_id).first()


class IntegrationTests(BaseProtectTestCase):

    def test_start(self):
        # Test the start situation: there are no registered objects in the
        # current ZODB transaction.
        self.assertEqual(self.transform._registered_objects(), [])

    def test_add_standard(self):
        item = self._createItem()
        self.session.add(item)
        self.assertEqual(self.transform._registered_objects(), [item])

    def test_add_with_flush(self):
        item = self._createItem()
        self.session.add(item)
        self.session.flush()
        self.assertEqual(self.transform._registered_objects(), [item])


class FunctionalTests(BaseProtectTestCase, EuphorieFunctionalTestCase):
    """Functional test so we can do commits.

    Here we want to add an item, commit this, and edit or delete it.
    """

    def setUp(self):
        super().setUp()
        item = self._createItem()
        self.session.add(item)
        transaction.commit()
        self.group_id = item.group_id

    def test_start(self):
        self.assertEqual(self.transform._registered_objects(), [])

    def test_edit_standard(self):
        # This is the start of a new transaction, so we need to get the item
        # fresh from the session.
        item = self._getItem()

        # Change a column.
        item.short_name = "changed"
        self.assertEqual(self.transform._registered_objects(), [item])

        # Check that the change is really there.
        self.assertEqual(self._getItem().short_name, "changed")

        # Check that the change stays there after a full commit.
        transaction.commit()
        self.assertEqual(self._getItem().short_name, "changed")

    def test_edit_with_flush(self):
        item = self._getItem()
        item.short_name = "changed"
        self.session.flush()
        self.assertEqual(self.transform._registered_objects(), [item])
        self.assertEqual(self._getItem().short_name, "changed")
        transaction.commit()
        self.assertEqual(self._getItem().short_name, "changed")

    def test_delete_standard(self):
        item = self._getItem()
        self.session.delete(item)
        self.assertEqual(self.transform._registered_objects(), [item])

        # Check that the item is really deleted.
        self.assertIsNone(self._getItem())
        transaction.commit()
        self.assertIsNone(self._getItem())

    def test_delete_with_flush(self):
        item = self._getItem()
        self.session.delete(item)
        self.session.flush()
        self.assertEqual(self.transform._registered_objects(), [item])
        self.assertIsNone(self._getItem())
        transaction.commit()
        self.assertIsNone(self._getItem())

    def _do_csrf_check(self):
        # Call the _check method of the transform.  This is called by
        # transformIterable, but that does too much.  We do need to prepare
        # the transform and the response a bit.
        resp = self.request.response
        resp.setHeader("Content-Type", "text/html")
        self.transform.site = self.portal

        # Do the check.
        self.transform._check()

    def test_delete_check(self):
        item = self._getItem()
        self.session.delete(item)
        self.assertEqual(self.transform._registered_objects(), [item])

        # Actually do the csrf check.
        self._do_csrf_check()

        # The write on GET was detected, so we get redirected.
        resp = self.request.response
        self.assertEqual(resp.status, 302)
        self.assertIn("confirm-action", resp.getHeader("location"))

        # The transaction was aborted, so the item still exists.
        self.assertIsNotNone(self._getItem())

    def test_delete_disable_csrf(self):
        from euphorie.content.protect import IDisableCSRFProtectionForSQL

        alsoProvides(self.request, IDisableCSRFProtectionForSQL)
        item = self._getItem()
        self.session.delete(item)
        self.assertEqual(self.transform._registered_objects(), [])

        # Actually do the csrf check.
        self._do_csrf_check()

        # The write on GET is accepted.
        resp = self.request.response
        self.assertEqual(resp.status, 200)

        # The transaction was not aborted, so the item no longer exists.
        self.assertIsNone(self._getItem())

        # Rolling back the session or aborting the transaction brings back
        # the item.
        self.session.rollback()
        self.assertIsNotNone(self._getItem())
