from lxml import objectify
from plone.dexterity.utils import createContentInContainer
from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.content import upload


class SurveyImporterTests(EuphorieTestCase):
    def createSurveyGroup(self):
        country = self.portal.sectors.nl
        sector = createContentInContainer(country,
                "euphorie.sector", title="sector")
        return createContentInContainer(sector,
                "euphorie.surveygroup", title="group")

    def createSurvey(self):
        surveygroup = self.createSurveyGroup()
        return createContentInContainer(surveygroup,
                "euphorie.survey", title="survey")

    def createModule(self):
        survey = self.createSurvey()
        return createContentInContainer(survey,
                "euphorie.module", title="module")

    def createRisk(self):
        module = self.createModule()
        return createContentInContainer(module,
                "euphorie.risk", title="risk")

    def testImportImage(self):
        from plone.namedfile.file import NamedBlobImage
        snippet = objectify.fromstring(
                '<image caption="Key image" filename="myfile.gif" '
                'content-type="image/gif">R0lGODlhAQABAIAAAAAAAP//'
                '/yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>')
        importer = upload.SurveyImporter(None)
        (image, caption) = importer.ImportImage(snippet)
        self.assertEqual(caption, u"Key image")
        self.assertTrue(isinstance(caption, unicode))
        self.assertEqual(image.contentType, "image/gif")
        self.assertEqual(image.filename, 'myfile.gif')
        self.assertTrue(isinstance(image, NamedBlobImage))

    def testImportImage_filename_from_mimetype(self):
        snippet = objectify.fromstring(
                '<image caption="Key image" content-type="image/bmp">'
                'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIB'
                'TAA7</image>')
        importer = upload.SurveyImporter(None)
        (image, caption) = importer.ImportImage(snippet)
        self.assertTrue(image.filename.endswith('.bmp'))

    def testImportImage_MimeFromFilename(self):
        snippet = objectify.fromstring(
                '<image filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAA'
                'EALAAAAAABAAEAAAIBTAA7</image>')
        importer = upload.SurveyImporter(None)
        (image, caption) = importer.ImportImage(snippet)
        self.assertEqual(caption, None)
        self.assertEqual(image.filename, u"tiny.gif")
        # Required by the interface :(
        self.assertTrue(isinstance(image.filename, unicode))
        self.assertEqual(image.contentType, "image/gif")

    def testImportSolution(self):
        snippet = objectify.fromstring(
        """<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <description>Add more abstraction layers</description>
             <action-plan>Add another level</action-plan>
             <prevention-plan>Ask a code reviewer to verify the design</prevention-plan>
             <requirements>A good understanding of architecture</requirements>
           </solution>""")
        self.loginAsPortalOwner()
        risk = self.createRisk()
        importer = upload.SurveyImporter(None)
        solution = importer.ImportSolution(snippet, risk)
        self.assertEqual(risk.keys(), ["3"])
        self.assertEqual(solution.description, u"Add more abstraction layers")
        self.failUnless(isinstance(solution.description, unicode))
        self.assertEqual(solution.action_plan, u"Add another level")
        self.failUnless(isinstance(solution.action_plan, unicode))
        self.assertEqual(
                solution.prevention_plan,
                u"Ask a code reviewer to verify the design")
        self.failUnless(isinstance(solution.prevention_plan, unicode))
        self.assertEqual(
                solution.requirements,
                u"A good understanding of architecture")
        self.failUnless(isinstance(solution.requirements, unicode))

    def testImportSolution_MissingFields(self):
        snippet = objectify.fromstring(
        """<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <description>Add more abstraction layers</description>
             <action-plan>Add another level</action-plan>
           </solution>""")
        self.loginAsPortalOwner()
        risk = self.createRisk()
        importer = upload.SurveyImporter(None)
        solution = importer.ImportSolution(snippet, risk)
        self.assertEqual(solution.description, u"Add more abstraction layers")
        self.assertEqual(solution.action_plan, u"Add another level")
        self.assertEqual(solution.prevention_plan, None)
        self.assertEqual(solution.requirements, None)

    def testImportRisk(self):
        snippet = objectify.fromstring(
        """<risk type="policy" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <problem-description>Not all desks are set to the right height.</problem-description>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <legal-reference>&lt;p&gt;See ARBO policies.&lt;/p&gt;</legal-reference>
             <show-not-applicable>true</show-not-applicable>
             <evaluation-method>direct</evaluation-method>
           </risk>""")
        self.loginAsPortalOwner()
        module = self.createModule()
        importer = upload.SurveyImporter(None)
        risk = importer.ImportRisk(snippet, module)
        self.assertEqual(risk.title, u"Are your desks at the right height?")
        self.failUnless(isinstance(risk.title, unicode))
        self.assertEqual(
                risk.problem_description,
                u"Not all desks are set to the right height.")
        self.failUnless(isinstance(risk.problem_description, unicode))
        self.assertEqual(
                risk.description,
                u"<p>The right height is important to prevent back problems.</p>")
        self.failUnless(isinstance(risk.description, unicode))
        self.assertEqual(risk.legal_reference, u"<p>See ARBO policies.</p>")
        self.failUnless(isinstance(risk.legal_reference, unicode))
        self.assertEqual(risk.show_notapplicable, True)
        self.assertEqual(risk.keys(), [])
        self.assertEqual(risk.caption, None)
        self.assertEqual(risk.image, None)

    def testImportRisk_Images(self):
        snippet = objectify.fromstring(
        """<risk type="policy" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <problem-description>Not all desks are set to the right height.</problem-description>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <legal-reference>&lt;p&gt;See ARBO policies.&lt;/p&gt;</legal-reference>
             <show-not-applicable>true</show-not-applicable>
             <evaluation-method>direct</evaluation-method>
             <image caption="Key image" filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
             <image caption="Image 2" filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
             <image caption="Image 3" filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
             <image caption="Image 4" filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
             <image caption="Image 5" filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
           </risk>""")
        self.loginAsPortalOwner()
        module = self.createModule()
        importer = upload.SurveyImporter(None)
        risk = importer.ImportRisk(snippet, module)
        self.assertEqual(risk.image.filename, "tiny.gif")
        self.assertEqual(risk.caption, u"Key image")
        self.assertEqual(risk.image2.filename, "tiny.gif")
        self.assertEqual(risk.caption2, u"Image 2")
        self.assertEqual(risk.image3.filename, "tiny.gif")
        self.assertEqual(risk.caption3, u"Image 3")
        self.assertEqual(risk.image4.filename, "tiny.gif")
        self.assertEqual(risk.caption4, u"Image 4")

    def testImportRisk_DirectEvaluation(self):
        snippet = objectify.fromstring(
        """<risk type="risk" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <evaluation-method default-priority="high">direct</evaluation-method>
           </risk>""")
        self.loginAsPortalOwner()
        module = self.createModule()
        importer = upload.SurveyImporter(None)
        risk = importer.ImportRisk(snippet, module)
        self.assertEqual(risk.show_notapplicable, False)
        self.assertEqual(risk.evaluation_method, "direct")
        self.assertEqual(risk.default_priority, "high")

    def testImportRisk_CalculatedEvaluation_Kinney(self):
        from euphorie.content.risk import IKinneyEvaluation
        snippet = objectify.fromstring(
        """<risk type="risk" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <evaluation-method default-probability="small" default-frequency="regular" default-effect="high">calculated</evaluation-method>
           </risk>""")
        self.loginAsPortalOwner()
        module = self.createModule()
        importer = upload.SurveyImporter(None)
        importer.ImportRisk(snippet, module)
        risk = module["2"]
        self.assertTrue(IKinneyEvaluation.providedBy(risk))
        self.assertEqual(risk.show_notapplicable, False)
        self.assertEqual(risk.evaluation_method, "calculated")
        self.assertEqual(risk.default_probability, 1)
        self.assertEqual(risk.default_frequency, 4)
        self.assertEqual(risk.default_effect, 10)

    def testImportRisk_CalculatedEvaluation_French(self):
        from Acquisition import aq_parent
        from euphorie.content.risk import IFrenchEvaluation
        snippet = objectify.fromstring(
        """<risk type="risk" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <evaluation-method default-severity="very-severe" default-frequency="often">calculated</evaluation-method>
           </risk>""")
        self.loginAsPortalOwner()
        module = self.createModule()
        group = aq_parent(aq_parent(module))
        group.evaluation_algorithm = u"french"
        importer = upload.SurveyImporter(None)
        risk = importer.ImportRisk(snippet, module)
        self.assertTrue(IFrenchEvaluation.providedBy(risk))
        self.assertEqual(risk.show_notapplicable, False)
        self.assertEqual(risk.evaluation_method, "calculated")
        self.assertEqual(risk.default_severity, 10)
        self.assertEqual(risk.default_frequency, 7)

    def testImportRisk_WithSolution(self):
        snippet = objectify.fromstring(
        """<risk type="policy" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <evaluation-method>direct</evaluation-method>
             <solutions>
               <solution>
                 <description>Use height-adjustable desks</description>
                 <action-plan>Order height-adjustable desks for desk workers.</action-plan>
               </solution>
             </solutions>
           </risk>""")
        self.loginAsPortalOwner()
        module = self.createModule()
        importer = upload.SurveyImporter(None)
        risk = importer.ImportRisk(snippet, module)
        self.assertEqual(risk.keys(), ["3"])
        solution = risk["3"]
        from euphorie.content.solution import Solution
        self.failUnless(isinstance(solution, Solution))
        self.assertEqual(solution.description, u"Use height-adjustable desks")

    def testImportModule(self):
        snippet = objectify.fromstring(
        """<module optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <solution-direction>&lt;p&gt;Buy the book from the gang of four.&lt;/p&gt;</solution-direction>
           </module>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        module = importer.ImportModule(snippet, survey)
        self.assertEqual(module.title, u"Design patterns")
        self.failUnless(isinstance(module.title, unicode))
        self.assertEqual(module.optional, False)
        self.assertEqual(module.question, None)
        self.assertEqual(
                module.description,
                u"<p>Software design patterns are critical.</p>")
        self.failUnless(isinstance(module.description, unicode))
        self.assertEqual(
                module.solution_direction,
                u"<p>Buy the book from the gang of four.</p>")
        self.failUnless(isinstance(module.solution_direction, unicode))
        self.assertEqual(module.keys(), [])
        self.assertEqual(module.image, None)

    def testImportModule_Image(self):
        snippet = objectify.fromstring(
        """<module optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <solution-direction>&lt;p&gt;Buy the book from the gang of four.&lt;/p&gt;</solution-direction>
             <image caption="My caption" content-type="image/gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
           </module>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        module = importer.ImportModule(snippet, survey)
        self.assertNotEqual(module.image, None)
        self.assertEqual(module.image.contentType, "image/gif")
        self.assertEqual(module.caption, u'My caption')

    def testImportModule_Optional(self):
        snippet = objectify.fromstring(
        """<module optional="true" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <question>Have you used design patterns?</question>
           </module>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        module = importer.ImportModule(snippet, survey)
        self.assertEqual(module.optional, True)
        self.assertEqual(module.question, u"Have you used design patterns?")

    def testImportModule_WithSubModule(self):
        snippet = objectify.fromstring(
        """<module optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <module optional="no">
               <title>Iterators</title>
               <description>&lt;p&gt;Iterators help optimise list handling.&lt;/p&gt;</description>
             </module>
           </module>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        module = importer.ImportModule(snippet, survey)
        self.assertEqual(module.keys(), ["2"])
        module = module["2"]
        from euphorie.content.module import Module
        self.failUnless(isinstance(module, Module))
        self.assertEqual(module.title, u"Iterators")

    def testImportModule_WithRisk(self):
        snippet = objectify.fromstring(
        """<module optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <risk type="policy">
               <title>New hires are not aware of design patterns.</title>
               <description>&lt;p&gt;Every developer should know about them..&lt;/p&gt;</description>
               <evaluation-method>direct</evaluation-method>
             </risk>
           </module>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        module = importer.ImportModule(snippet, survey)
        self.assertEqual(module.keys(), ["2"])
        risk = module["2"]
        from euphorie.content.risk import Risk
        self.failUnless(isinstance(risk, Risk))
        self.assertEqual(
                risk.title,
                u"New hires are not aware of design patterns.")

    def testImportProfileQuestion(self):
        snippet = objectify.fromstring(
        """<profile-question xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Laptop usage</title>
             <question>Do your employees use laptops?</question>
             <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
           </profile-question>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        profile = importer.ImportProfileQuestion(snippet, survey)
        self.assertEqual(profile.title, u"Laptop usage")
        self.failUnless(isinstance(profile.title, unicode))
        self.assertEqual(profile.question, u"Do your employees use laptops?")
        self.failUnless(isinstance(profile.question, unicode))
        self.assertEqual(profile.description, u"<p>Laptops are very common in the modern workplace.</p>")
        self.failUnless(isinstance(profile.description, unicode))
        self.assertEqual(profile.keys(), [])

    def testImportProfileQuestion_optional_type(self):
        from euphorie.content.module import Module
        snippet = objectify.fromstring(
        """<profile-question type="optional"
                xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Laptop usage</title>
             <question>Do your employees use laptops?</question>
           </profile-question>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        profile = importer.ImportProfileQuestion(snippet, survey)
        self.assertTrue(isinstance(profile, Module))
        self.assertEqual(profile.optional, True)

    def testImportProfileQuestion_WithModule(self):
        snippet = objectify.fromstring(
        """<profile-question xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Laptop usage</title>
             <question>Do your employees use laptops?</question>
             <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
             <module optional="no">
               <title>Design patterns</title>
               <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             </module>
           </profile-question>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        profile = importer.ImportProfileQuestion(snippet, survey)
        self.assertEqual(profile.keys(), ["2"])
        module = profile["2"]
        from euphorie.content.module import Module
        self.failUnless(isinstance(module, Module))
        self.assertEqual(module.title, u"Design patterns")

    def testImportProfileQuestion_WithRisk(self):
        snippet = objectify.fromstring(
        """<profile-question xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Laptop usage</title>
             <question>Do your employees use laptops?</question>
             <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
             <risk type="policy">
               <title>New hires are not aware of design patterns.</title>
               <description>&lt;p&gt;Every developer should know about them..&lt;/p&gt;</description>
               <evaluation-method>direct</evaluation-method>
             </risk>
           </profile-question>""")
        self.loginAsPortalOwner()
        survey = self.createSurvey()
        importer = upload.SurveyImporter(None)
        profile = importer.ImportProfileQuestion(snippet, survey)
        self.assertEqual(profile.keys(), ["2"])
        risk = profile["2"]
        from euphorie.content.risk import Risk
        self.failUnless(isinstance(risk, Risk))
        self.assertEqual(
                risk.title,
                u"New hires are not aware of design patterns.")

    def testImportSurvey(self):
        snippet = objectify.fromstring(
        """<survey xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <classification-code>A.1.2.3</classification-code>
             <language>nl</language>
             <evaluation-optional>true</evaluation-optional>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup = self.createSurveyGroup()
        importer = upload.SurveyImporter(None)
        survey = importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        self.assertEqual(survey.keys(), [])
        self.assertEqual(survey.title, u"Fresh import")
        self.failUnless(isinstance(survey.title, unicode))
        self.assertEqual(survey.classification_code, u"A.1.2.3")
        self.failUnless(isinstance(survey.language, str))
        self.assertEqual(survey.language, "nl")
        self.failUnless(isinstance(survey.classification_code, str))
        self.assertEqual(survey.evaluation_optional, True)

    def testImportSurvey_WithModule(self):
        snippet = objectify.fromstring(
        """<survey optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <module optional="no">
               <title>Design patterns</title>
               <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             </module>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup = self.createSurveyGroup()
        importer = upload.SurveyImporter(None)
        survey = importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        self.assertEqual(survey.keys(), ["1"])
        module = survey["1"]
        from euphorie.content.module import Module
        self.failUnless(isinstance(module, Module))
        self.assertEqual(module.title, u"Design patterns")

    def testImportSurvey_WithProfileQuestion(self):
        snippet = objectify.fromstring(
        """<survey optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <profile-question>
               <title>Laptop usage</title>
               <question>Do your employees use laptops?</question>
               <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
             </profile-question>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup = self.createSurveyGroup()
        importer = upload.SurveyImporter(None)
        survey = importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        self.assertEqual(survey.keys(), ["1"])
        profile = survey["1"]
        from euphorie.content.profilequestion import ProfileQuestion
        self.failUnless(isinstance(profile, ProfileQuestion))
        self.assertEqual(profile.title, u"Laptop usage")

    def testImportSurvey_ChildOrdering(self):
        snippet = objectify.fromstring(
        """<survey optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <module optional="no">
               <title>Module one</title>
               <description/>
             </module>
             <profile-question>
               <title>Profile one</title>
               <question/>
               <description/>
             </profile-question>
             <module optional="no">
               <title>Module two</title>
               <description/>
             </module>
             <profile-question>
               <title>Profile two</title>
               <question/>
               <description/>
             </profile-question>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup = self.createSurveyGroup()
        importer = upload.SurveyImporter(None)
        survey = importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        self.assertEqual(survey.keys(), ["1", "2", "3", "4"])
        children = survey.values()
        self.assertEquals(children[0].title, u"Module one")
        self.assertEquals(children[1].title, u"Profile one")
        self.assertEquals(children[2].title, u"Module two")
        self.assertEquals(children[3].title, u"Profile two")


class SectorImporterTests(EuphorieTestCase):
    def testImportSurvey(self):
        from plone.uuid.interfaces import IUUID
        snippet = objectify.fromstring(
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development sector</title>
             <survey>
               <title>Software development</title>
             </survey>
           </sector>""")
        self.loginAsPortalOwner()
        country = self.portal.sectors.nl
        importer = upload.SectorImporter(country)
        importer(snippet, None, "login", None, u"Import")
        self.assertEqual(
                country.keys(),
                ["help", "software-development-sector"])
        sector = country["software-development-sector"]
        self.assertEqual(sector.title, "Software development sector")
        self.assertEqual(sector.login, "login")
        self.failUnless(isinstance(sector.title, unicode))
        self.assertEqual(sector.keys(), ["software-development"])
        self.assertEqual(sector.contact_email, None)
        self.assertEqual(sector.password, None)
        group = sector["software-development"]
        self.assertEqual(group.title, "Software development")
        self.failUnless(isinstance(group.title, unicode))
        self.assertEqual(group.keys(), ["import"])
        self.assertTrue(isinstance(IUUID(sector), str))

    def testImportSurvey_WithAccount(self):
        snippet = objectify.fromstring(
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development sector</title>
             <account login="coders" password="s3cr3t" />
             <contact>
               <name>Team lead</name>
               <email>discard@simplon.biz</email>
             </contact>
           </sector>""")
        self.loginAsPortalOwner()
        country = self.portal.sectors.nl
        importer = upload.SectorImporter(country)
        importer(snippet, None, None, None, u"Import")
        sector = country["software-development-sector"]
        self.assertEqual(sector.login, u"coders")
        self.assertEqual(sector.contact_name, u"Team lead")
        self.assertEqual(sector.contact_email, u"discard@simplon.biz")
        self.assertEqual(sector.password, "s3cr3t")

    def testImportSurvey_WithLogo(self):
        snippet = objectify.fromstring(
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development sector</title>
             <logo filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</logo>
           </sector>""")
        self.loginAsPortalOwner()
        country = self.portal.sectors.nl
        importer = upload.SectorImporter(country)
        importer(snippet, None, "login", None, u"Import")
        sector = country["software-development-sector"]
        self.assertNotEqual(sector.logo, None)
        self.assertEqual(sector.logo.filename, "tiny.gif")
        self.assertEqual(sector.logo.contentType, "image/gif")
        self.assertEqual(sector.logo.data, "GIF89a\x01\x00\x01\x00\x80\x00\x00"
                                           "\x00\x00\x00\xff\xff\xff!\xf9\x04"
                                           "\x01\x00\x00\x01\x00,\x00\x00\x00"
                                           "\x00\x01\x00\x01\x00\x00\x02\x01L"
                                           "\x00;")
