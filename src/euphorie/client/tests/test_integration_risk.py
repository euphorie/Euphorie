from euphorie.client import model
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from z3c.saconfig import Session


class RiskIntegrationTests(EuphorieIntegrationTestCase):
    def create_session_risk(self):
        with api.env.adopt_user(SITE_OWNER_NAME):
            api.content.create(
                container=self.portal.sectors, type="euphorie.country", id="eu"
            )
            client_country = api.content.create(
                container=self.portal.client, type="euphorie.clientcountry", id="eu"
            )
            client_sector = api.content.create(
                container=client_country, type="euphorie.clientsector", id="sector"
            )
            client_survey = api.content.create(
                container=client_sector, type="euphorie.survey", id="survey"
            )

        sqlsession = Session()
        account = model.Account(loginname="jane", password="secret")
        sqlsession.add(account)
        session = model.SurveySession(
            title="Session", zodb_path="eu/sector/survey", account=account
        )
        sqlsession.add(session)
        sqlsession.flush()

        module = session.addChild(
            model.Module(
                title="Root", module_id="1", zodb_path="1", has_description=False
            )
        )
        module = module.__of__(client_survey)
        risk = session.addChild(
            model.Risk(
                title="Risk 1",
                risk_id="1",
                zodb_path="1/1",
                type="risk",
                identification="no",
            )
        )
        risk = risk.__of__(module)

        return risk

    def test_default_collapsible_sections(self):
        risk = self.create_session_risk()

        with self._get_view("identification", risk) as view:
            # default default sections
            self.assertEqual(
                view.default_collapsible_sections, ["collapsible_section_information"]
            )

        # customized default sections
        view.webhelpers.content_country_obj.risk_default_collapsible_sections = [
            "collapsible_section_resources",
            "collapsible_section_comments",
        ]
        with self._get_view("identification", risk) as view:
            self.assertEqual(
                view.default_collapsible_sections,
                ["collapsible_section_resources", "collapsible_section_comments"],
            )

    def test_get_collapsible_section_state(self):
        risk = self.create_session_risk()

        with self._get_view("identification", risk) as view:
            # default default sections
            self.assertEqual(view.get_collapsible_section_state("information"), "")
            self.assertEqual(view.get_collapsible_section_state("resources"), "closed")
            self.assertEqual(view.get_collapsible_section_state("comments"), "closed")

        # customized default sections
        view.webhelpers.content_country_obj.risk_default_collapsible_sections = [
            "collapsible_section_resources",
            "collapsible_section_comments",
        ]
        with self._get_view("identification", risk) as view:
            self.assertEqual(
                view.get_collapsible_section_state("information"), "closed"
            )
            self.assertEqual(view.get_collapsible_section_state("resources"), "")
            self.assertEqual(view.get_collapsible_section_state("comments"), "")
