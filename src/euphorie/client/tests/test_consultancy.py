from AccessControl import Unauthorized
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import Consultancy
from euphorie.client.model import Organisation
from euphorie.client.model import OrganisationMembership
from euphorie.client.model import SessionEvent
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import MockMailFixture
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from time import sleep
from z3c.saconfig import Session
from zope.interface import alsoProvides

import json


class TestSessionValidation(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)

        self.session = Session()

        self.owner = model.Account(
            loginname="valerie@labyrinth.social", password="secret"
        )
        self.session.add(self.owner)
        self.session.flush()
        self.session.add(
            Organisation(
                owner_id=self.owner.id,
            )
        )

        survey_session = model.SurveySession(
            id=1,
            title="Euphorie",
            zodb_path="nl/ict/software-development",
            account=self.owner,
        )
        self.session.add(survey_session)
        survey = self.portal.client.nl.ict["software-development"]
        session_id = "++session++%d" % survey_session.id
        self.traversed_session = survey.restrictedTraverse(session_id)

        self.consultant = model.Account(
            loginname="michel.moulin@example-consultancy.com",
            password="secret",
        )
        self.session.add(self.consultant)
        self.session.flush()

        self.session.add(
            OrganisationMembership(
                owner_id=self.owner.id,
                member_id=self.consultant.id,
                member_role="consultant",
            )
        )

        self.session.flush()
        alsoProvides(self.request, IClientSkinLayer)

    def test_available_consultants(self):
        with api.env.adopt_user(user=self.owner):
            with self._get_view(
                "panel-request-validation",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                self.assertIn(self.consultant, view.consultants)

    def test_request_validation_permission_denied(self):
        other_member = model.Account(
            loginname="siobhan@labyrinth.social",
            password="secret",
        )
        self.session.add(other_member)
        self.session.flush()

        self.session.add(
            OrganisationMembership(
                owner_id=self.owner.id,
                member_id=other_member.id,
                member_role="member",
            )
        )
        self.session.flush()

        with api.env.adopt_user(user=other_member):
            with self._get_view(
                "panel-request-validation",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                self.assertRaises(Unauthorized, view)

    def test_request_validation(self):
        mail_fixture = MockMailFixture()
        with api.env.adopt_user(user=self.owner):
            with self._get_view(
                "panel-request-validation",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                view.request.method = "POST"
                view.request.form = {"consultant": self.consultant.id}
                view()
                self.assertEqual(
                    self.traversed_session.session.consultancy.account,
                    self.consultant,
                )
                events = (
                    self.session.query(SessionEvent)
                    .filter(
                        SessionEvent.session_id == self.traversed_session.session.id
                    )
                    .order_by(SessionEvent.time.desc())
                    .all()
                )
                self.assertEqual(len(events), 1)
                self.assertEqual(events[0].action, "validation_requested")
                self.assertEqual(events[0].account_id, self.owner.id)
                self.assertLessEqual(
                    abs(events[0].time - datetime.utcnow()),
                    timedelta(seconds=5),
                )
                self.assertEqual(len(mail_fixture.storage), 1)
                self.assertEqual(
                    mail_fixture.storage[0][0][1],
                    "michel.moulin@example-consultancy.com",
                )

    def test_validate_permission_denied_to_other_member(self):
        other_member = model.Account(
            loginname="siobhan@labyrinth.social",
            password="secret",
        )
        self.session.add(other_member)
        self.session.flush()

        self.session.add(
            OrganisationMembership(
                owner_id=self.owner.id,
                member_id=other_member.id,
                member_role="member",
            )
        )
        self.session.flush()

        self.traversed_session.session.consultancy = Consultancy(
            account=self.consultant,
            session=self.traversed_session.session,
        )
        event = SessionEvent(
            account_id=self.consultant.id,
            session_id=self.traversed_session.session.id,
            action="validation_requested",
        )
        self.session.add(event)
        with api.env.adopt_user(user=other_member):
            with self._get_view(
                "panel-validate-risk-assessment",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                self.assertRaises(Unauthorized, view)

    def test_validate_permission_denied_to_other_consultant(self):
        other_consultant = model.Account(
            loginname="nancy.ann.ciancy@example-consultancy.com",
            password="secret",
        )
        self.session.add(other_consultant)
        self.session.flush()

        self.session.add(
            OrganisationMembership(
                owner_id=self.owner.id,
                member_id=other_consultant.id,
                member_role="consultant",
            )
        )

        self.session.flush()

        self.traversed_session.session.consultant = self.consultant
        with api.env.adopt_user(user=other_consultant):
            with self._get_view(
                "panel-validate-risk-assessment",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                self.assertRaises(Unauthorized, view)

    def test_validate_risk_assessment(self):
        second_admin = model.Account(
            loginname="jessica@labyrinth.social", password="secret"
        )
        self.session.add(second_admin)
        self.session.flush()

        self.session.add(
            OrganisationMembership(
                owner_id=self.owner.id,
                member_id=second_admin.id,
                member_role="admin",
            )
        )
        self.consultant.first_name = "Michel"
        self.consultant.last_name = "Moulin"

        mail_fixture = MockMailFixture()
        self.traversed_session.session.consultancy = Consultancy(
            account=self.consultant,
            session=self.traversed_session.session,
        )
        event = SessionEvent(
            account_id=self.consultant.id,
            session_id=self.traversed_session.session.id,
            action="validation_requested",
        )
        self.session.add(event)
        self.session.flush()
        with api.env.adopt_user(user=self.consultant):
            with self._get_view(
                "panel-validate-risk-assessment",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                view.request.method = "POST"
                view.request.form = {"approved": "1"}
                view()

        # consultant stays set
        self.assertEqual(
            self.traversed_session.session.consultancy.account,
            self.consultant,
        )
        self.assertTrue(self.traversed_session.session.is_validated)
        with api.env.adopt_user(user=self.owner):
            with self._get_view(
                "consultancy",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                self.assertEqual(
                    view.validated_info.consultant_email,
                    "michel.moulin@example-consultancy.com",
                )
                self.assertEqual(view.validated_info.consultant_name, "Michel Moulin")
            self.assertLessEqual(
                abs(
                    view.validated_info.raw_time
                    - datetime.utcnow().replace(tzinfo=timezone.utc)
                ),
                timedelta(seconds=5),
            )

        self.assertTrue(self.traversed_session.session.is_locked)

        self.assertEqual(len(mail_fixture.storage), 2)
        recipients = {
            mail_fixture.storage[0][0][1],
            mail_fixture.storage[1][0][1],
        }
        self.assertSetEqual(
            recipients,
            {"valerie@labyrinth.social", "jessica@labyrinth.social"},
        )

        # We need to wait at least one second because the datetime
        # is stored with that accuracy
        sleep(1)

        # if locking is enabled...
        api.portal.set_registry_record("euphorie.use_locking_feature", True)
        # ... then admin/owner can unlock
        with api.env.adopt_user(user=self.owner):
            with self._get_view(
                "locking_view",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                view.unset_lock()

        self.session.flush()
        self.assertTrue(self.traversed_session.session.is_validated)
        self.assertFalse(self.traversed_session.session.is_locked)

    def test_validate_locked_risk_assessment(self):
        self.traversed_session.session.consultancy = Consultancy(
            account=self.consultant,
            session=self.traversed_session.session,
        )
        event = SessionEvent(
            account_id=self.consultant.id,
            session_id=self.traversed_session.session.id,
            action="validation_requested",
        )
        self.session.add(event)

        api.portal.set_registry_record("euphorie.use_locking_feature", True)
        with api.env.adopt_user(user=self.owner):
            with self._get_view(
                "locking_view",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                view.set_lock()
                original_lock_event = view.last_locking_event

        # Some time passes before the consultant validates the assessment
        sleep(3)

        with api.env.adopt_user(user=self.consultant):
            with self._get_view(
                "panel-validate-risk-assessment",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                view.request.method = "POST"
                view.request.form = {"approved": "1"}
                view()

        # consultant stays set
        self.assertEqual(
            self.traversed_session.session.consultancy.account,
            self.consultant,
        )
        self.assertTrue(self.traversed_session.session.is_validated)
        self.assertTrue(self.traversed_session.session.is_locked)
        with self._get_view(
            "locking_view",
            self.traversed_session,
            self.traversed_session.session,
        ) as view:
            lock_event = view.last_locking_event
        self.assertEqual(lock_event.account, self.owner)
        self.assertEqual(lock_event.time, original_lock_event.time)

    def test_delete_consultant(self):
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.traversed_session.session.consultancy = Consultancy(
            account=self.consultant,
            session=self.traversed_session.session,
        )
        event = SessionEvent(
            account_id=self.consultant.id,
            session_id=self.traversed_session.session.id,
            action="validated",
            time=now,
            note=json.dumps(
                {
                    "consultant_id": self.consultant.id,
                    "consultant_email": self.consultant.email,
                    "consultant_name": "Michel Moulin",
                }
            ),
        )
        self.session.add(event)

        self.session.delete(self.consultant)
        self.session.flush()

        self.assertTrue(self.traversed_session.session.is_validated)
        with api.env.adopt_user(user=self.owner):
            with self._get_view(
                "consultancy",
                self.traversed_session,
                self.traversed_session.session,
            ) as view:
                self.assertEqual(
                    view.validated_info.consultant_email,
                    "michel.moulin@example-consultancy.com",
                )
                self.assertEqual(view.validated_info.consultant_name, "Michel Moulin")
            self.assertLessEqual(
                abs(view.validated_info.raw_time - now),
                timedelta(seconds=5),
            )
