from contextlib import contextmanager
from euphorie.client.model import Organisation
from euphorie.client.model import Session
from euphorie.client.tests.utils import addAccount
from euphorie.client.utils import getRequest
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from time import time
from zExceptions import NotFound

import re


class TestOrganisations(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.account = addAccount(password="secret")
        self.organisation = Organisation(
            owner_id=self.account.id,
            title="Acme",
        )
        Session.add(self.organisation)

    @contextmanager
    def _get_view(self, *args, post=False, **kwargs):
        with super()._get_view(*args, **kwargs) as view:
            if post:
                request = getRequest()
                request.method = "POST"
                request.form["submit"] = "accept"
            yield view

    def test_add_user_panel(self):
        with api.env.adopt_user("admin"):
            api.content.create(
                container=self.portal.sectors, type="euphorie.country", id="eu"
            )
            client_country = api.content.create(
                container=self.portal.client, type="euphorie.clientcountry", id="eu"
            )

        with api.env.adopt_user(user=self.account):
            with self._get_view(
                "panel-add-user-to-organisation", self.portal.client.eu
            ) as view:
                view.publishTraverse(view.request, self.organisation.organisation_id)
                # Check we have a toke
                token = view.token
                self.assertRegex(view.token, re.compile(r"[0-9a-f]{32}"))
                # Check the token is cached
                self.assertEqual(token, view.token)

                # Check token related data
                token_data = view.storage[token]
                expected_keys = {"userid", "expires", "role", "organisation_id"}
                self.assertEqual(set(token_data), expected_keys)
                self.assertEqual(token_data["userid"], self.account.id)
                self.assertEqual(
                    token_data["organisation_id"], self.organisation.organisation_id
                )
                self.assertTrue(token_data["expires"] > time())
                self.assertEqual(token_data["expires"] // time(), 1)
                self.assertEqual(token_data["role"], "member")

                # Check that the body contains the link
                self.assertIn(
                    (
                        f"{client_country.absolute_url()}/"
                        f"@@confirm-organisation-invite/{token}"
                    ),
                    api.portal.translate(view.body),
                )

    def test_confirmation_link(self):
        with api.env.adopt_user("admin"):
            api.content.create(
                container=self.portal.sectors, type="euphorie.country", id="eu"
            )
            api.content.create(
                container=self.portal.client, type="euphorie.clientcountry", id="eu"
            )

        account1 = addAccount("foo@example.com", password="secret")
        account2 = addAccount("bar@example.com", password="secret")
        organisation2 = Organisation(
            owner_id=account2.id,
            title="Bar&co",
        )
        Session.add(organisation2)
        account3 = addAccount("baz@example.com", password="secret")
        with api.env.adopt_user(user=self.account):
            with self._get_view(
                "panel-add-user-to-organisation", self.portal.client.eu
            ) as view:
                # self.account creates a token
                view.publishTraverse(view.request, self.organisation.organisation_id)
                token = view.token

        with api.env.adopt_user(user=account2):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                # Calling without a token returns a not found
                with self.assertRaises(NotFound):
                    view()

                # Now we traverse to a bogus token
                view.publishTraverse(None, "bogus")()
                self.assertEqual(
                    view.request.response.headers["location"],
                    "http://nohost/plone/client/eu/@@organisation",
                )
                self.assertListEqual(
                    [_.message for _ in IStatusMessage(view.request).show()],
                    ["We could not find the invitation you are looking for."],
                )

        # Check that account1 will not consume its own token
        with api.env.adopt_user(user=self.account):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                view.publishTraverse(None, token)()
                self.assertEqual(
                    view.request.response.headers["location"],
                    "http://nohost/plone/client/eu/@@organisation#org-1",
                )
                self.assertListEqual(
                    [_.message for _ in IStatusMessage(view.request).show()],
                    ["You cannot add yourself to your organisation."],
                )

        # Check that account2 can consume a good token
        with api.env.adopt_user(user=account2):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                view.publishTraverse(None, token)()
                self.assertEqual(
                    view.request.response.headers["location"],
                    "http://nohost/plone/client/eu/@@organisation#org-1",
                )
                self.assertListEqual(
                    [_.message for _ in IStatusMessage(view.request).show()],
                    ["You have been added to the Acme organisation."],
                )
                # We need to flush the data to the database
                view.sqlsession.flush()

        # Account 1 can check that account2 is in the organisation
        with api.env.adopt_user(user=self.account):
            with self._get_view("organisation", self.portal.client.eu) as view:
                self.assertListEqual(
                    [x.Account for x in view.get_memberships(self.organisation)],
                    [account2],
                )

        # Check that account2 cannot consume a good token more than once
        with api.env.adopt_user(user=account2):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                view.publishTraverse(None, token)()
                self.assertEqual(
                    view.request.response.headers["location"],
                    "http://nohost/plone/client/eu/@@organisation#org-1",
                )
                self.assertListEqual(
                    [_.message for _ in IStatusMessage(view.request).show()],
                    ["You are already a member of the Acme organisation."],
                )
                view.sqlsession.flush()

        # The same token can be used from account 3
        with api.env.adopt_user(user=account3):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                view.publishTraverse(None, token)()
                # We need to flush the data to the database
                view.sqlsession.flush()

        # Account 1 can check that account3 is in the organisation
        with api.env.adopt_user(user=account1):
            with self._get_view("organisation", self.portal.client.eu) as view:
                self.assertListEqual(
                    [x.Account for x in view.get_memberships(self.organisation)],
                    [account2, account3],
                )

        # Let's also have account 2 invite people around
        with api.env.adopt_user(user=account2):
            with self._get_view(
                "panel-add-user-to-organisation", self.portal.client.eu
            ) as view:
                view.publishTraverse(view.request, organisation2.organisation_id)
                # account1 creates a token
                token = view.token

        # Account 1 can accept
        with api.env.adopt_user(user=account1):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                view.publishTraverse(None, token)()

        # Let's fake that the token is expired now:
        with api.env.adopt_user(user=account2):
            with self._get_view(
                "panel-add-user-to-organisation", self.portal.client.eu
            ) as view:
                view.storage[token]["expires"] = 0.0

        # Check that account3 cannot consume an expired token
        with api.env.adopt_user(user=account3):
            with self._get_view(
                "confirm-organisation-invite", self.portal.client.eu, post=True
            ) as view:
                view.publishTraverse(None, token)()
                self.assertEqual(
                    view.request.response.headers["location"],
                    "http://nohost/plone/client/eu/@@organisation",
                )
                self.assertListEqual(
                    [_.message for _ in IStatusMessage(view.request).show()],
                    [
                        "The invitation from the Bar&co "
                        "organisation is not valid anymore."
                    ],
                )

        # Account 2 can check that account1 is in the organisation
        with api.env.adopt_user(user=account2):
            with self._get_view("organisation", self.portal.client.eu) as view:
                self.assertListEqual(
                    [x.Account for x in view.get_memberships(organisation2)],
                    [account1],
                )
