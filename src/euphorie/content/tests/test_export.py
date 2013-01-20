# coding: utf-8
import unittest
from zope.component.testing import PlacelessSetup
from lxml import etree
from euphorie.content.export import ExportSurvey


class MockImage(object):
    def __init__(self, data, filename=None, contentType=None):
        self.data = data
        self.filename = filename
        self.contentType = contentType


class ExportSurveyTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        from zope.component import provideAdapter
        from zope.annotation.attribute import AttributeAnnotations
        from plone.folder.default import DefaultOrdering
        provideAdapter(AttributeAnnotations)
        provideAdapter(DefaultOrdering)

    def root(self):
        from euphorie.content.upload import NSMAP
        return etree.Element("root", nsmap=NSMAP)

    def testImage_Minimal(self):
        image = MockImage("hot stuff here")
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportImage(root, image)
        self.assertTrue(node in root)
        self.assertEqual(
                etree.tostring(node, pretty_print=True),
                '<image xmlns="http://xml.simplon.biz/euphorie/survey/1.0">'
                'aG90IHN0dWZmIGhlcmU=\n</image>\n')

    def testImage_Full(self):
        image = MockImage("hot stuff here", "test.gif", "image/gif")
        root = self.root()
        view = ExportSurvey(None, None)
        image = view.exportImage(root, image, u"Captiøn")
        self.assertEqual(etree.tostring(image, pretty_print=True),
                '<image xmlns="http://xml.simplon.biz/euphorie/survey/1.0" '
                'content-type="image/gif" filename="test.gif" '
                'caption="Capti&#xF8;n">aG90IHN0dWZmIGhlcmU=\n'
                '</image>\n')

    def testSolution_Minimal(self):
        from euphorie.content.solution import Solution
        solution = Solution()
        solution.description = u"<p>Test description</p>"
        solution.action_plan = u"Sample action plan"
        solution.prevention_plan = None
        solution.requirements = None
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportSolution(root, solution)
        self.assertTrue(node in root)
        self.assertEqual(etree.tostring(node, pretty_print=True),
                '<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <description>&lt;p&gt;Test description&lt;/p&gt;'
                '</description>\n'
                '  <action-plan>Sample action plan</action-plan>\n'
                '</solution>\n')

    def testSolution_Complete(self):
        from euphorie.content.solution import Solution
        solution = Solution()
        solution.description = u"<p>Tést description</p>"
        solution.action_plan = u"Sample actiøn plan"
        solution.prevention_plan = u"Sample prevention plån"
        solution.requirements = u"Requîrements"
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportSolution(root, solution)
        self.assertEqual(etree.tostring(node, pretty_print=True),
                '<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <description>&lt;p&gt;T&#233;st description&lt;/p&gt;'
                '</description>\n'
                '  <action-plan>Sample acti&#248;n plan</action-plan>\n'
                '  <prevention-plan>Sample prevention pl&#229;n'
                '</prevention-plan>\n'
                '  <requirements>Requ&#238;rements</requirements>\n'
                '</solution>\n')

    def testRisk_Minimal(self):
        from euphorie.content.risk import Risk
        risk = Risk()
        risk.type = "top5"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportRisk(root, risk)
        self.assertTrue(node in root)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <risk type="top5">\n'
                '    <title>Can your windows be locked?</title>\n'
                '    <problem-description>Not all your windows can be locked'
                '</problem-description>\n'
                '    <description>&lt;p&gt;Locking windows is '
                'critical.&lt;/p&gt;</description>\n'
                '    <show-not-applicable>false</show-not-applicable>\n'
                '  </risk>\n'
                '</root>\n')

    def testRisk_DirectEvaluation(self):
        from euphorie.content.risk import Risk
        risk = Risk()
        risk.type = "risk"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = True
        risk.evaluation_method = "direct"
        risk.default_priority = "low"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <risk type="risk">\n'
                '    <title>Can your windows be locked?</title>\n'
                '    <problem-description>Not all your windows can be '
                'locked</problem-description>\n'
                '    <description>&lt;p&gt;Locking windows is '
                'critical.&lt;/p&gt;</description>\n'
                '    <show-not-applicable>true</show-not-applicable>\n'
                '    <evaluation-method default-priority="low">direct'
                '</evaluation-method>\n'
                '  </risk>\n'
                '</root>\n')

    def testRisk_CalculatedEvaluation(self):
        from euphorie.content.risk import Risk
        risk = Risk()
        risk.type = "risk"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = True
        risk.evaluation_method = "calculated"
        risk.default_probability = 1
        risk.default_frequency = 4
        risk.default_effect = 0
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <risk type="risk">\n'
                '    <title>Can your windows be locked?</title>\n'
                '    <problem-description>Not all your windows can be '
                'locked</problem-description>\n'
                '    <description>&lt;p&gt;Locking windows is critical.'
                '&lt;/p&gt;</description>\n'
                '    <show-not-applicable>true</show-not-applicable>\n'
                '    <evaluation-method default-probability="small" '
                'default-frequency="regular">calculated</evaluation-method>\n'
                '  </risk>\n'
                '</root>\n')

    def testRisk_LegalReferenceNoText(self):
        from euphorie.content.risk import Risk
        risk = Risk()
        risk.type = "top5"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = u"<p><br/></p>"
        risk.show_notapplicable = False
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <risk type="top5">\n'
                '    <title>Can your windows be locked?</title>\n'
                '    <problem-description>Not all your windows can be locked'
                '</problem-description>\n'
                '    <description>&lt;p&gt;Locking windows is critical.'
                '&lt;/p&gt;</description>\n'
                '    <show-not-applicable>false</show-not-applicable>\n'
                '  </risk>\n'
                '</root>\n')

    def testRisk_TwoImages(self):
        from euphorie.content.risk import Risk
        risk = Risk()
        risk.type = "top5"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        risk.image = MockImage("hot stuff here")
        risk.caption = u"Image caption 1"
        risk.image2 = MockImage("hot stuff here")
        risk.caption2 = u"Image caption 2"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <risk type="top5">\n'
                '    <title>Can your windows be locked?</title>\n'
                '    <problem-description>Not all your windows can be locked'
                '</problem-description>\n'
                '    <description>&lt;p&gt;Locking windows is critical.'
                '&lt;/p&gt;</description>\n'
                '    <show-not-applicable>false</show-not-applicable>\n'
                '    <image caption="Image caption 1">aG90IHN0dWZmIGhlcmU=\n'
                '</image>\n'
                '    <image caption="Image caption 2">aG90IHN0dWZmIGhlcmU=\n'
                '</image>\n'
                '  </risk>\n'
                '</root>\n')

    def testRisk_WithSolution(self):
        from euphorie.content.solution import Solution
        from euphorie.content.risk import Risk
        risk = Risk()
        risk.type = "top5"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        solution = Solution()
        solution.description = u"<p>Test description</p>"
        solution.action_plan = u"Sample action plan"
        solution.prevention_plan = None
        solution.requirements = None
        risk["1"] = solution
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportRisk(root, risk)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <risk type="top5">\n'
                '    <title>Can your windows be locked?</title>\n'
                '    <problem-description>Not all your windows can be locked'
                '</problem-description>\n'
                '    <description>&lt;p&gt;Locking windows is critical.'
                '&lt;/p&gt;</description>\n'
                '    <show-not-applicable>false</show-not-applicable>\n'
                '    <solutions>\n'
                '      <solution>\n'
                '        <description>&lt;p&gt;Test description&lt;/p&gt;'
                '</description>\n'
                '        <action-plan>Sample action plan</action-plan>\n'
                '      </solution>\n'
                '    </solutions>\n'
                '  </risk>\n'
                '</root>\n')

    def testModule_Minimal(self):
        from euphorie.content.module import Module
        module = Module()
        module.title = u"Office buildings"
        module.optional = False
        module.solution_direction = None
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportModule(root, module)
        self.assertTrue(node in root)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <module optional="false">\n'
                '    <title>Office buildings</title>\n'
                '  </module>\n'
                '</root>\n')

    def testModule_with_description(self):
        from euphorie.content.module import Module
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.solution_direction = None
        module.optional = False
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        xml = etree.tostring(root, pretty_print=True)
        self.assertTrue(
                '<description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n' in xml)

    def testModule_Optional(self):
        from euphorie.content.module import Module
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = True
        module.question = u"Do you have an office building?"
        module.solution_direction = None
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <module optional="true">\n'
                '    <title>Office buildings</title>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '    <question>Do you have an office building?</question>\n'
                '  </module>\n'
                '</root>\n')

    def testModule_SolutionDirectionNoText(self):
        from euphorie.content.module import Module
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = u"<p><br/></p>"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <module optional="false">\n'
                '    <title>Office buildings</title>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '  </module>\n'
                '</root>\n')

    def testModule_Image(self):
        from euphorie.content.module import Module
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        module.image = MockImage("hot stuff here")
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <module optional="false">\n'
                '    <title>Office buildings</title>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '    <image>aG90IHN0dWZmIGhlcmU=\n'
                '</image>\n'
                '  </module>\n'
                '</root>\n')

    def testModule_WithRisk(self):
        from euphorie.content.module import Module
        from euphorie.content.risk import Risk
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        risk = Risk()
        risk.type = "top5"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        module["1"] = risk
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <module optional="false">\n'
                '    <title>Office buildings</title>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '    <risk type="top5">\n'
                '      <title>Can your windows be locked?</title>\n'
                '      <problem-description>Not all your windows can be '
                'locked</problem-description>\n'
                '      <description>&lt;p&gt;Locking windows is critical.'
                '&lt;/p&gt;</description>\n'
                '      <show-not-applicable>false</show-not-applicable>\n'
                '    </risk>\n'
                '  </module>\n'
                '</root>\n')

    def testModule_WithSubModule(self):
        from euphorie.content.module import Module
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        submodule = Module()
        submodule.title = u"Parking"
        submodule.description = u"<p>All about parking garages.</p>"
        submodule.optional = False
        submodule.solution_direction = None
        module["1"] = submodule
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportModule(root, module)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <module optional="false">\n'
                '    <title>Office buildings</title>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '    <module optional="false">\n'
                '      <title>Parking</title>\n'
                '      <description>&lt;p&gt;All about parking garages.'
                '&lt;/p&gt;</description>\n'
                '    </module>\n'
                '  </module>\n'
                '</root>\n')

    def testProfileQuestion_Minimal(self):
        from euphorie.content.profilequestion import ProfileQuestion
        profile = ProfileQuestion()
        profile.title = u"Office buildings"
        profile.question = u"Do you have an office building?"
        profile.type = "optional"
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportProfileQuestion(root, profile)
        self.assertTrue(node in root)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <profile-question>\n'
                '    <title>Office buildings</title>\n'
                '    <question>Do you have an office building?</question>\n'
                '  </profile-question>\n'
                '</root>\n')

    def testProfileQuestion_with_description(self):
        from euphorie.content.profilequestion import ProfileQuestion
        profile = ProfileQuestion()
        profile.title = u"Office buildings"
        profile.description = u"<p>Owning property brings risks.</p>"
        profile.type = 'optional'
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        xml = etree.tostring(root, pretty_print=True)
        self.assertTrue(
                '<description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>' in xml)

    def testProfileQuestion_WithoutQuestion(self):
        from euphorie.content.profilequestion import ProfileQuestion
        profile = ProfileQuestion()
        profile.title = u"Office buildings"
        profile.description = u"<p>Owning property brings risks.</p>"
        profile.type = "optional"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <profile-question>\n'
                '    <title>Office buildings</title>\n'
                '    <question>Office buildings</question>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '  </profile-question>\n'
                '</root>\n')

    def testProfileQuestion_WithRisk(self):
        from euphorie.content.profilequestion import ProfileQuestion
        from euphorie.content.risk import Risk
        profile = ProfileQuestion()
        profile.title = u"Office buildings"
        profile.question = u"Do you have an office buildings?"
        profile.description = u"<p>Owning property brings risks.</p>"
        profile.type = "optional"
        risk = Risk()
        risk.type = "top5"
        risk.title = u"Can your windows be locked?"
        risk.problem_description = u"Not all your windows can be locked"
        risk.description = u"<p>Locking windows is critical.</p>"
        risk.legal_reference = None
        risk.show_notapplicable = False
        profile["1"] = risk
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <profile-question>\n'
                '    <title>Office buildings</title>\n'
                '    <question>Do you have an office buildings?</question>\n'
                '    <description>&lt;p&gt;Owning property brings risks.'
                '&lt;/p&gt;</description>\n'
                '    <risk type="top5">\n'
                '      <title>Can your windows be locked?</title>\n'
                '      <problem-description>Not all your windows can be '
                'locked</problem-description>\n'
                '      <description>&lt;p&gt;Locking windows is critical.'
                '&lt;/p&gt;</description>\n'
                '      <show-not-applicable>false</show-not-applicable>\n'
                '    </risk>\n'
                '  </profile-question>\n'
                '</root>\n')

    def testProfileQuestion_WithModule(self):
        from euphorie.content.profilequestion import ProfileQuestion
        from euphorie.content.module import Module
        profile = ProfileQuestion()
        profile.title = u"Office buildings"
        profile.question = u"Do you have an office buildings?"
        profile.description = u"<p>Owning property brings risks.</p>"
        profile.type = "optional"
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        profile["1"] = module
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportProfileQuestion(root, profile)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <profile-question>\n'
                '    <title>Office buildings</title>\n'
                '    <question>Do you have an office buildings?</question>\n'
                '    <description>&lt;p&gt;Owning property brings '
                'risks.&lt;/p&gt;</description>\n'
                '    <module optional="false">\n'
                '      <title>Office buildings</title>\n'
                '      <description>&lt;p&gt;Owning property brings '
                'risks.&lt;/p&gt;</description>\n'
                '    </module>\n'
                '  </profile-question>\n'
                '</root>\n')

    def testSurvey_Minimal(self):
        from euphorie.content.surveygroup import SurveyGroup
        from euphorie.content.survey import Survey
        surveygroup = SurveyGroup()
        surveygroup.title = u"Generic sector"
        surveygroup.evaluation_algorithm = u"french"
        surveygroup["standard"] = Survey()
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = u"Standard"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        root = self.root()
        view = ExportSurvey(None, None)
        node = view.exportSurvey(root, survey)
        self.assertTrue(node in root)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <survey>\n'
                '    <title>Generic sector</title>\n'
                '    <language>en-GB</language>\n'
                '    <evaluation-algorithm>french</evaluation-algorithm>\n'
                '    <evaluation-optional>false</evaluation-optional>\n'
                '  </survey>\n'
                '</root>\n')

    def testSurvey_IntroductionNoText(self):
        from euphorie.content.surveygroup import SurveyGroup
        from euphorie.content.survey import Survey
        surveygroup = SurveyGroup()
        surveygroup.title = u"Generic sector"
        surveygroup["standard"] = Survey()
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = u"Standard"
        survey.introduction = u"<p><br/></p>"
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportSurvey(root, survey)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <survey>\n'
                '    <title>Generic sector</title>\n'
                '    <language>en-GB</language>\n'
                '    <evaluation-algorithm>kinney</evaluation-algorithm>\n'
                '    <evaluation-optional>false</evaluation-optional>\n'
                '  </survey>\n'
                '</root>\n')

    def testSurvey_WithProfileQuestion(self):
        from euphorie.content.surveygroup import SurveyGroup
        from euphorie.content.survey import Survey
        from euphorie.content.profilequestion import ProfileQuestion
        surveygroup = SurveyGroup()
        surveygroup.title = u"Generic sector"
        surveygroup["standard"] = Survey()
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = u"Generic sector"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        profile = ProfileQuestion()
        profile.title = u"Office buildings"
        profile.question = u"Do you have an office buildings?"
        profile.description = u"<p>Owning property brings risks.</p>"
        profile.type = "optional"
        survey["1"] = profile
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportSurvey(root, survey)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <survey>\n'
                '    <title>Generic sector</title>\n'
                '    <language>en-GB</language>\n'
                '    <evaluation-algorithm>kinney</evaluation-algorithm>\n'
                '    <evaluation-optional>false</evaluation-optional>\n'
                '    <profile-question>\n'
                '      <title>Office buildings</title>\n'
                '      <question>Do you have an office buildings?</question>\n'
                '      <description>&lt;p&gt;Owning property brings '
                'risks.&lt;/p&gt;</description>\n'
                '    </profile-question>\n'
                '  </survey>\n'
                '</root>\n')

    def testSurvey_WithModule(self):
        from euphorie.content.surveygroup import SurveyGroup
        from euphorie.content.survey import Survey
        from euphorie.content.module import Module
        surveygroup = SurveyGroup()
        surveygroup.title = u"Generic sector"
        surveygroup["standard"] = Survey()
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.title = u"Generic sector"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        module = Module()
        module.title = u"Office buildings"
        module.description = u"<p>Owning property brings risks.</p>"
        module.optional = False
        module.solution_direction = None
        survey["1"] = module
        root = self.root()
        view = ExportSurvey(None, None)
        view.exportSurvey(root, survey)
        self.assertEqual(etree.tostring(root, pretty_print=True),
                '<root xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <survey>\n'
                '    <title>Generic sector</title>\n'
                '    <language>en-GB</language>\n'
                '    <evaluation-algorithm>kinney</evaluation-algorithm>\n'
                '    <evaluation-optional>false</evaluation-optional>\n'
                '    <module optional="false">\n'
                '      <title>Office buildings</title>\n'
                '      <description>&lt;p&gt;Owning property brings '
                'risks.&lt;/p&gt;</description>\n'
                '    </module>\n'
                '  </survey>\n'
                '</root>\n')

    def testRender(self):
        from euphorie.content.surveygroup import SurveyGroup
        from euphorie.content.survey import Survey
        from zope.publisher.browser import TestRequest
        surveygroup = SurveyGroup()
        surveygroup.id = "mysector"
        surveygroup.title = u"Generic sector"
        surveygroup["standard"] = Survey()
        survey = surveygroup["standard"]  # Acquisition wrap
        survey.id = "dummy"
        survey.title = u"Standard"
        survey.introduction = None
        survey.classification_code = None
        survey.evaluation_optional = False
        survey.language = "en-GB"
        view = ExportSurvey(survey, TestRequest())
        output = view()
        response = view.request.response
        self.assertEqual(response.getHeader("Content-Type"), "text/xml")
        self.assertEqual(
                response.getHeader("Content-Disposition"),
                'attachment; filename="mysector.xml"')
        self.assertEqual(output,
                '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n'
                '<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">\n'
                '  <survey>\n'
                '    <title>Generic sector</title>\n'
                '    <language>en-GB</language>\n'
                '    <evaluation-algorithm>kinney</evaluation-algorithm>\n'
                '    <evaluation-optional>false</evaluation-optional>\n'
                '  </survey>\n'
                '</sector>\n')
