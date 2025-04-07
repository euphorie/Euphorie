from euphorie.content.browser.export import ExportSurvey
from euphorie.content.browser.upload import NSMAP
from euphorie.content.module import Module
from euphorie.content.profilequestion import ProfileQuestion
from euphorie.content.risk import Risk
from euphorie.content.solution import Solution
from euphorie.content.survey import Survey
from euphorie.content.surveygroup import SurveyGroup
from euphorie.content.training_question import TrainingQuestion
from euphorie.testing import EuphorieIntegrationTestCase
from io import BytesIO
from lxml import etree
from plone.base.utils import safe_text
from zipfile import ZipFile
from zope.publisher.browser import TestRequest


class MockImage:
    def __init__(self, data, filename=None, contentType=None):
        self.data = data
        self.filename = filename
        self.contentType = contentType


class ExportSurveyTests(EuphorieIntegrationTestCase):
    def root(self):
        return etree.Element("root", nsmap=NSMAP)

    def testImage_Minimal(self):
        image = MockImage("hot stuff here")
        root = self.root()
        view = ExportSurvey(None, None)
        view.include_images = True
        node = view.exportImage(root, image)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(node, pretty_print=True)),
            '<image xmlns="http://xml.simplon.biz/euphorie/survey/1.0">'
            "aG90IHN0dWZmIGhlcmU=\n</image>\n",
        )

    def testImage_Full(self):
        image = MockImage("hot stuff here", "test.gif", "image/gif")
        root = self.root()
        view = ExportSurvey(None, None)
        view.include_images = True
        image = view.exportImage(root, image, "Captiøn")
        self.assertEqual(
            safe_text(etree.tostring(image, pretty_print=True)),
            '<image xmlns="http://xml.simplon.biz/euphorie/survey/1.0" '
            'content-type="image/gif" filename="test.gif" '
            'caption="Capti&#xF8;n">aG90IHN0dWZmIGhlcmU=\n'
            "</image>\n",
        )

    def testSolution_Minimal(self):
        solution = Solution()
        solution.description = "<p>Test description</p>"
        solution.action = "Sample action plan"
        solution.requirements = None
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportSolution(root, solution)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(node, pretty_print=True)),
            '<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <description>&lt;p&gt;Test description&lt;/p&gt;"
            "</description>\n"
            "  <action>Sample action plan</action>\n"
            "</solution>\n",
        )

    def testSolution_Complete(self):
        solution = Solution()
        solution.description = "<p>Tést description</p>"
        solution.action = "Sample actiøn plan"
        solution.requirements = "Requîrements"
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportSolution(root, solution)
        self.assertEqual(
            safe_text(etree.tostring(node, pretty_print=True)),
            '<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <description>&lt;p&gt;T&#233;st description&lt;/p&gt;"
            "</description>\n"
            "  <action>Sample acti&#248;n plan</action>\n"
            "  <requirements>Requ&#238;rements</requirements>\n"
            "</solution>\n",
        )

    def testRisk_Minimal(self):
        risk = Risk()
        risk.type = "top5"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportRisk(root, risk)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <risk type="top5">\n'
            "    <title>Can your windows be locked?</title>\n"
            "    <problem-description>Not all your windows can be locked"
            "</problem-description>\n"
            "    <description>&lt;p&gt;Locking windows is "
            "critical.&lt;/p&gt;</description>\n"
            "    <show-not-applicable>false</show-not-applicable>\n"
            "  </risk>\n"
            "</root>\n",
        )

    def testRisk_DirectEvaluation(self):
        risk = Risk()
        risk.type = "risk"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = True
        risk.evaluation_method = "direct"
        risk.default_priority = "low"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <risk type="risk">\n'
            "    <title>Can your windows be locked?</title>\n"
            "    <problem-description>Not all your windows can be "
            "locked</problem-description>\n"
            "    <description>&lt;p&gt;Locking windows is "
            "critical.&lt;/p&gt;</description>\n"
            "    <show-not-applicable>true</show-not-applicable>\n"
            '    <evaluation-method default-priority="low">direct'
            "</evaluation-method>\n"
            "  </risk>\n"
            "</root>\n",
        )

    def testRisk_CalculatedEvaluation(self):
        risk = Risk()
        risk.type = "risk"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = True
        risk.evaluation_method = "calculated"
        risk.default_probability = 1
        risk.default_frequency = 4
        risk.default_effect = 0
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <risk type="risk">\n'
            "    <title>Can your windows be locked?</title>\n"
            "    <problem-description>Not all your windows can be "
            "locked</problem-description>\n"
            "    <description>&lt;p&gt;Locking windows is critical."
            "&lt;/p&gt;</description>\n"
            "    <show-not-applicable>true</show-not-applicable>\n"
            '    <evaluation-method default-probability="small" '
            'default-frequency="regular">calculated</evaluation-method>\n'
            "  </risk>\n"
            "</root>\n",
        )

    def testRisk_LegalReferenceNoText(self):
        risk = Risk()
        risk.type = "top5"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = "<p><br/></p>"
        risk.show_notapplicable = False
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <risk type="top5">\n'
            "    <title>Can your windows be locked?</title>\n"
            "    <problem-description>Not all your windows can be locked"
            "</problem-description>\n"
            "    <description>&lt;p&gt;Locking windows is critical."
            "&lt;/p&gt;</description>\n"
            "    <show-not-applicable>false</show-not-applicable>\n"
            "  </risk>\n"
            "</root>\n",
        )

    def testRisk_TwoImages(self):
        risk = Risk()
        risk.type = "top5"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        risk.image = MockImage("hot stuff here")
        risk.caption = "Image caption 1"
        risk.image2 = MockImage("hot stuff here")
        risk.caption2 = "Image caption 2"
        root = self.root()
        view = ExportSurvey(None, None)
        view.include_images = True
        view.exportRisk(root, risk)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <risk type="top5">\n'
            "    <title>Can your windows be locked?</title>\n"
            "    <problem-description>Not all your windows can be locked"
            "</problem-description>\n"
            "    <description>&lt;p&gt;Locking windows is critical."
            "&lt;/p&gt;</description>\n"
            "    <show-not-applicable>false</show-not-applicable>\n"
            '    <image caption="Image caption 1">aG90IHN0dWZmIGhlcmU=\n'
            "</image>\n"
            '    <image caption="Image caption 2">aG90IHN0dWZmIGhlcmU=\n'
            "</image>\n"
            "  </risk>\n"
            "</root>\n",
        )

    def testRisk_WithSolution(self):
        risk = Risk()
        risk.type = "top5"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        solution = Solution()
        solution.description = "<p>Test description</p>"
        solution.action = "Sample action plan"
        solution.requirements = None
        risk._setOb("1", solution)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <risk type="top5">\n'
            "    <title>Can your windows be locked?</title>\n"
            "    <problem-description>Not all your windows can be locked"
            "</problem-description>\n"
            "    <description>&lt;p&gt;Locking windows is critical."
            "&lt;/p&gt;</description>\n"
            "    <show-not-applicable>false</show-not-applicable>\n"
            "    <solutions>\n"
            "      <solution>\n"
            "        <description>&lt;p&gt;Test description&lt;/p&gt;"
            "</description>\n"
            "        <action>Sample action plan</action>\n"
            "      </solution>\n"
            "    </solutions>\n"
            "  </risk>\n"
            "</root>\n",
        )

    def testModule_Minimal(self):
        module = Module()
        module.title = "Office buildings"
        module.optional = False
        module.solution_direction = None
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportModule(root, module)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <module optional="false">\n'
            "    <title>Office buildings</title>\n"
            "  </module>\n"
            "</root>\n",
        )

    def testModule_with_description(self):
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.solution_direction = None
        module.optional = False
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        xml = safe_text(etree.tostring(root, pretty_print=True))
        self.assertTrue(
            "<description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n" in xml
        )

    def testModule_Optional(self):
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = True
        module.question = "Do you have an office building?"
        module.solution_direction = None
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <module optional="true">\n'
            "    <title>Office buildings</title>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            "    <question>Do you have an office building?</question>\n"
            "  </module>\n"
            "</root>\n",
        )

    def testModule_SolutionDirectionNoText(self):
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = "<p><br/></p>"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <module optional="false">\n'
            "    <title>Office buildings</title>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            "  </module>\n"
            "</root>\n",
        )

    def testModule_Image(self):
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        module.image = MockImage("hot stuff here")
        root = self.root()
        view = ExportSurvey(None, None)
        view.include_images = True
        view.exportModule(root, module)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <module optional="false">\n'
            "    <title>Office buildings</title>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            "    <image>aG90IHN0dWZmIGhlcmU=\n"
            "</image>\n"
            "  </module>\n"
            "</root>\n",
        )

    def testModule_WithRisk(self):
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        risk = Risk()
        risk.type = "top5"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        module._setOb("1", risk)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <module optional="false">\n'
            "    <title>Office buildings</title>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            '    <risk type="top5">\n'
            "      <title>Can your windows be locked?</title>\n"
            "      <problem-description>Not all your windows can be "
            "locked</problem-description>\n"
            "      <description>&lt;p&gt;Locking windows is critical."
            "&lt;/p&gt;</description>\n"
            "      <show-not-applicable>false</show-not-applicable>\n"
            "    </risk>\n"
            "  </module>\n"
            "</root>\n",
        )

    def testModule_WithSubModule(self):
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        submodule = Module()
        submodule.title = "Parking"
        submodule.description = "<p>All about parking garages.</p>"
        submodule.optional = False
        submodule.solution_direction = None
        module._setOb("1", submodule)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            '  <module optional="false">\n'
            "    <title>Office buildings</title>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            '    <module optional="false">\n'
            "      <title>Parking</title>\n"
            "      <description>&lt;p&gt;All about parking garages."
            "&lt;/p&gt;</description>\n"
            "    </module>\n"
            "  </module>\n"
            "</root>\n",
        )

    def testProfileQuestion_Minimal(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office building?"
        profile.use_location_question = False
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportProfileQuestion(root, profile)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Do you have an office building?</question>\n"
            "    <use-location-question>false</use-location-question>\n"
            "  </profile-question>\n"
            "</root>\n",
        )

    def testProfileQuestion_LocationQuestions(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office building?"
        profile.label_multiple_present = "Do you have more than one building?"
        profile.label_single_occurance = "Enter the name of your building."
        profile.label_multiple_occurances = (
            "Enter the names of each of your buildings."  # noqa
        )
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportProfileQuestion(root, profile)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Do you have an office building?</question>\n"
            "    <label-multiple-present>Do you have more than one building"
            "?</label-multiple-present>\n"
            "    <label-single-occurance>Enter the name of your building."
            "</label-single-occurance>\n"
            "    <label-multiple-occurances>Enter the names of each of your"
            " buildings.</label-multiple-occurances>\n"
            "    <use-location-question>true</use-location-question>\n"
            "  </profile-question>\n"
            "</root>\n",
        )

    def testProfileQuestion_with_description(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.description = "<p>Owning property brings risks.</p>"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        xml = safe_text(etree.tostring(root, pretty_print=True))
        self.assertTrue(
            "<description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>" in xml
        )

    def testProfileQuestion_WithoutQuestion(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.description = "<p>Owning property brings risks.</p>"
        profile.use_location_question = False
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Office buildings</question>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            "    <use-location-question>false</use-location-question>\n"
            "  </profile-question>\n"
            "</root>\n",
        )

    def testProfileQuestion_WithRisk(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office buildings?"
        profile.description = "<p>Owning property brings risks.</p>"
        risk = Risk()
        risk.type = "top5"
        risk.title = "Can your windows be locked?"
        risk.problem_description = "Not all your windows can be locked"
        risk.description = "<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        profile._setOb("1", risk)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Do you have an office buildings?</question>\n"
            "    <description>&lt;p&gt;Owning property brings risks."
            "&lt;/p&gt;</description>\n"
            "    <use-location-question>true</use-location-question>\n"
            '    <risk type="top5">\n'
            "      <title>Can your windows be locked?</title>\n"
            "      <problem-description>Not all your windows can be "
            "locked</problem-description>\n"
            "      <description>&lt;p&gt;Locking windows is critical."
            "&lt;/p&gt;</description>\n"
            "      <show-not-applicable>false</show-not-applicable>\n"
            "    </risk>\n"
            "  </profile-question>\n"
            "</root>\n",
        )

    def testProfileQuestion_WithModule(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office buildings?"
        profile.description = "<p>Owning property brings risks.</p>"
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        profile._setOb("1", module)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Do you have an office buildings?</question>\n"
            "    <description>&lt;p&gt;Owning property brings "
            "risks.&lt;/p&gt;</description>\n"
            "    <use-location-question>true</use-location-question>\n"
            '    <module optional="false">\n'
            "      <title>Office buildings</title>\n"
            "      <description>&lt;p&gt;Owning property brings "
            "risks.&lt;/p&gt;</description>\n"
            "    </module>\n"
            "  </profile-question>\n"
            "</root>\n",
        )

    def testTrainingQuestion(self):
        training_question = TrainingQuestion()
        training_question.title = "What is the answer?"
        training_question.right_answer = "Yes"
        training_question.wrong_answer_1 = "No"
        training_question.wrong_answer_2 = "Maybe"
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportTrainingQuestion(root, training_question)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <training_question>\n"
            "    <title>What is the answer?</title>\n"
            "    <right_answer>Yes</right_answer>\n"
            "    <wrong_answer_1>No</wrong_answer_1>\n"
            "    <wrong_answer_2>Maybe</wrong_answer_2>\n"
            "  </training_question>\n"
            "</root>\n",
        )

    def testSurvey_Minimal(self):
        surveygroup = SurveyGroup()
        surveygroup.title = "Generic sector"
        surveygroup.evaluation_algorithm = "french"
        surveygroup._setOb("standard", Survey())
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = "Standard"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportSurvey(root, survey)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <survey>\n"
            "    <title>Generic sector</title>\n"
            "    <language>en-GB</language>\n"
            "    <tool_type>classic</tool_type>\n"
            "    <measures_text_handling>full</measures_text_handling>\n"
            "    <integrated_action_plan>false</integrated_action_plan>\n"
            "    <evaluation-algorithm>french</evaluation-algorithm>\n"
            "    <evaluation-optional>false</evaluation-optional>\n"
            "  </survey>\n"
            "</root>\n",
        )

    def testSurvey_IntroductionNoText(self):
        surveygroup = SurveyGroup()
        surveygroup.title = "Generic sector"
        surveygroup._setOb("standard", Survey())
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = "Standard"
        survey.introduction = "<p><br/></p>"
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportSurvey(root, survey)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <survey>\n"
            "    <title>Generic sector</title>\n"
            "    <language>en-GB</language>\n"
            "    <tool_type>classic</tool_type>\n"
            "    <measures_text_handling>full</measures_text_handling>\n"
            "    <integrated_action_plan>false</integrated_action_plan>\n"
            "    <evaluation-algorithm>kinney</evaluation-algorithm>\n"
            "    <evaluation-optional>false</evaluation-optional>\n"
            "  </survey>\n"
            "</root>\n",
        )

    def testSurvey_WithProfileQuestion(self):
        surveygroup = SurveyGroup()
        surveygroup.title = "Generic sector"
        surveygroup._setOb("standard", Survey())
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = "Generic sector"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office buildings?"
        profile.description = "<p>Owning property brings risks.</p>"
        profile.type = "optional"
        survey._setOb("1", profile)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportSurvey(root, survey)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <survey>\n"
            "    <title>Generic sector</title>\n"
            "    <language>en-GB</language>\n"
            "    <tool_type>classic</tool_type>\n"
            "    <measures_text_handling>full</measures_text_handling>\n"
            "    <integrated_action_plan>false</integrated_action_plan>\n"
            "    <evaluation-algorithm>kinney</evaluation-algorithm>\n"
            "    <evaluation-optional>false</evaluation-optional>\n"
            "    <profile-question>\n"
            "      <title>Office buildings</title>\n"
            "      <question>Do you have an office buildings?</question>\n"
            "      <description>&lt;p&gt;Owning property brings "
            "risks.&lt;/p&gt;</description>\n"
            "      <use-location-question>true</use-location-question>\n"
            "    </profile-question>\n"
            "  </survey>\n"
            "</root>\n",
        )

    def testSurvey_WithModule(self):
        surveygroup = SurveyGroup()
        surveygroup.title = "Generic sector"
        surveygroup._setOb("standard", Survey())
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = "Generic sector"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        module = Module()
        module.title = "Office buildings"
        module.description = "<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        survey._setOb("1", module)
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportSurvey(root, survey)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <survey>\n"
            "    <title>Generic sector</title>\n"
            "    <language>en-GB</language>\n"
            "    <tool_type>classic</tool_type>\n"
            "    <measures_text_handling>full</measures_text_handling>\n"
            "    <integrated_action_plan>false</integrated_action_plan>\n"
            "    <evaluation-algorithm>kinney</evaluation-algorithm>\n"
            "    <evaluation-optional>false</evaluation-optional>\n"
            '    <module optional="false">\n'
            "      <title>Office buildings</title>\n"
            "      <description>&lt;p&gt;Owning property brings "
            "risks.&lt;/p&gt;</description>\n"
            "    </module>\n"
            "  </survey>\n"
            "</root>\n",
        )

    def testRender(self):
        surveygroup = SurveyGroup()
        surveygroup.id = "mysector"
        surveygroup.title = "Generic sector"
        surveygroup._setOb("standard", Survey())
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.id = "dummy"
        survey.title = "Standard"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.integrated_action_plan = True
        survey.language = "en-GB"
        survey.tool_type = "existing_measures"
        view = ExportSurvey(survey, TestRequest())
        output = view.render_output().decode("utf-8")
        response = view.request.response
        self.assertEqual(response.getHeader("Content-Type"), "text/xml")
        self.assertEqual(
            response.getHeader("Content-Disposition"),
            'attachment; filename="mysector.xml"',
        )
        self.assertEqual(
            output,
            "<?xml version='1.0' encoding='utf-8'?>\n"
            '<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <survey>\n"
            "    <title>Generic sector</title>\n"
            "    <language>en-GB</language>\n"
            "    <tool_type>existing_measures</tool_type>\n"
            "    <measures_text_handling>full</measures_text_handling>\n"
            "    <integrated_action_plan>true</integrated_action_plan>\n"
            "    <evaluation-algorithm>kinney</evaluation-algorithm>\n"
            "    <evaluation-optional>false</evaluation-optional>\n"
            "  </survey>\n"
            "</sector>\n",
        )

    def testRenderZip(self):
        surveygroup = SurveyGroup()
        surveygroup.id = "mysector"
        surveygroup.title = "Generic sector"
        surveygroup._setOb("standard", Survey())
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.id = "dummy"
        survey.title = "Standard"
        survey.introduction = "Wie grün sind deine Blätter?"
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.integrated_action_plan = True
        survey.language = "en-GB"
        survey.tool_type = "existing_measures"
        view = ExportSurvey(survey, TestRequest())
        view.export_as_plain_text = True
        output = view.render_output()
        zip_file = ZipFile(BytesIO(output), mode="r")
        response = view.request.response
        self.assertEqual(response.getHeader("Content-Type"), "application/zip")
        self.assertEqual(
            response.getHeader("Content-Disposition"),
            'attachment; filename="mysector.zip"',
        )
        self.assertEqual(
            zip_file.namelist(), ["mysector_word_count.txt", "mysector.xml"]
        )
        with zip_file.open("mysector_word_count.txt") as txt_file:
            txt = txt_file.read().decode("utf-8").strip()
            self.assertEqual(txt, "Generic sector Wie grün sind deine Blätter?")
        with zip_file.open("mysector.xml") as xml_file:
            xml = xml_file.read().decode("utf-8")
            self.assertEqual(
                xml,
                "<?xml version='1.0' encoding='utf-8'?>\n"
                '<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                "  <survey>\n"
                "    <title>Generic sector</title>\n"
                "    <introduction>Wie grün sind deine Blätter?</introduction>\n"
                "    <language>en-GB</language>\n"
                "    <tool_type>existing_measures</tool_type>\n"
                "    <measures_text_handling>full</measures_text_handling>\n"
                "    <integrated_action_plan>true</integrated_action_plan>\n"
                "    <evaluation-algorithm>kinney</evaluation-algorithm>\n"
                "    <evaluation-optional>false</evaluation-optional>\n"
                "  </survey>\n"
                "</sector>\n",
            )

    def testEtranslateRenderWithHTML(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office building?"
        profile.description = "<p>No</p><p>container</p>"
        root = self.root()
        view = ExportSurvey(None, None)
        view.is_etranslate_compatible = True
        node = view.exportProfileQuestion(root, profile)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Do you have an office building?</question>\n"
            "    <description>\n"
            "      <p>No</p>\n"
            "      <p>container</p>\n"
            "    </description>\n"
            "    <use-location-question>true</use-location-question>\n"
            "  </profile-question>\n"
            "</root>\n",
        )

    def testEtranslateRenderWithoutHTML(self):
        profile = ProfileQuestion()
        profile.title = "Office buildings"
        profile.question = "Do you have an office building?"
        profile.description = "Plain text"
        root = self.root()
        view = ExportSurvey(None, None)
        view.is_etranslate_compatible = True
        node = view.exportProfileQuestion(root, profile)
        self.assertTrue(node in root)
        self.assertEqual(
            safe_text(etree.tostring(root, pretty_print=True)),
            '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
            "  <profile-question>\n"
            "    <title>Office buildings</title>\n"
            "    <question>Do you have an office building?</question>\n"
            "    <description>Plain text</description>\n"
            "    <use-location-question>true</use-location-question>\n"
            "  </profile-question>\n"
            "</root>\n",
        )
