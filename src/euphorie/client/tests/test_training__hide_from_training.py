from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from z3c.saconfig import Session
from zope.interface import alsoProvides


SURVEY_1 = """
<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
  <title>sector</title>
  <survey>
    <title>survey</title>
    <language>nl</language>
    <module>
      <title>module1</title>
      <risk>
        <title>risk11</title>
        <problem_description>problem-desc-11</problem_description>
        <description>desc-11</description>
      </risk>
    </module>
    <module>
      <title>module2</title>
      <risk>
        <title>risk21</title>
        <problem_description>problem-desc-21</problem_description>
        <description>desc-21</description>
      </risk>
    </module>
  </survey>
</sector>
"""

SURVEY_2 = """
<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
  <title>sector</title>
  <survey>
    <title>survey</title>
    <language>nl</language>
    <module hide_from_training="True">
      <title>module1</title>
      <risk>
        <title>risk11</title>
        <problem_description>problem-desc-11</problem_description>
        <description>desc-11</description>
      </risk>
    </module>
    <module>
      <title>module2</title>
      <risk>
        <title>risk21</title>
        <problem_description>problem-desc-21</problem_description>
        <description>desc-21</description>
      </risk>
    </module>
  </survey>
</sector>
"""


class TestTrainingHideFromTraining(EuphorieIntegrationTestCase):
    """Tests the IHideFromTraining behavior.

    Also tests importing an xml structure with the hide_from_training
    attribute set.
    """

    def setUp(self):
        super().setUp()
        api.portal.set_registry_record("euphorie.use_training_module", True)

        # Add the hide_from_training behavior to the module type
        types = api.portal.get_tool("portal_types")
        fti_module = types.get("euphorie.module")
        fti_module.behaviors = tuple(
            list(fti_module.behaviors) + ["euphorie.hide_from_training"]
        )
        from plone.dexterity.schema import SCHEMA_CACHE

        SCHEMA_CACHE.invalidate("euphorie.module")

    def create_content(self, survey_xml):
        session = Session()
        self.account = addAccount(password="secret")
        with api.env.adopt_user("admin"):
            addSurvey(self.portal, survey_xml)
        self.survey = self.portal.client.nl.sector.survey
        alsoProvides(self.survey.REQUEST, IClientSkinLayer)

        survey_session = model.SurveySession(
            title="Dummy session",
            zodb_path="nl/sector/survey",
            account=self.account,
        )
        session.add(survey_session)

        module1 = survey_session.addChild(
            model.Module(title="module1", module_id="module1", zodb_path="1"),
        )
        module1.addChild(
            model.Risk(title="risk11", risk_id="risk11", zodb_path="1/2"),
        )
        module2 = survey_session.addChild(
            model.Module(title="module2", module_id="module2", zodb_path="3"),
        )
        module2.addChild(
            model.Risk(title="risk21", risk_id="risk21", zodb_path="3/4"),
        )
        session.flush()

    def test_training_module_visible(self):
        """Test the standard case - all modules and ristsk are visible in the
        training.
        """
        self.create_content(SURVEY_1)

        traversed_session = self.survey.restrictedTraverse("++session++1")
        with api.env.adopt_user(user=self.account):
            with self._get_view(
                "training", traversed_session, self.request.clone()
            ) as view:
                self.survey.enable_web_training = True
                data = list(view.slide_data.values())

                self.assertEqual(len(data), 4)
                self.assertEqual(data[0]["item"].title, "module1")
                self.assertEqual(data[1]["item"].title, "risk11")
                self.assertEqual(data[2]["item"].title, "module2")
                self.assertEqual(data[3]["item"].title, "risk21")

    def test_training_module_hidden(self):
        """Test module1 hidden from training."""
        self.create_content(SURVEY_2)

        traversed_session = self.survey.restrictedTraverse("++session++1")
        with api.env.adopt_user(user=self.account):
            with self._get_view(
                "training", traversed_session, self.request.clone()
            ) as view:
                self.survey.enable_web_training = True
                data = list(view.slide_data.values())

                self.assertEqual(len(data), 2)
                self.assertEqual(data[0]["item"].title, "module2")
                self.assertEqual(data[1]["item"].title, "risk21")
