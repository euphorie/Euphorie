from lxml import objectify
from plone.dexterity.utils import createContentInContainer
from euphorie.content.tests.functional import EuphorieContentTestCase
from euphorie.content import upload

class SurveyImporterTests(EuphorieContentTestCase):
    def createSurveyGroup(self):
        self.portal.invokeFactory("euphorie.sectorcontainer", "sectors")
        container=self.portal.sectors
        country=createContentInContainer(container, "euphorie.country", "nl")
        sector=createContentInContainer(country, "euphorie.sector", "sector")
        return createContentInContainer(sector, "euphorie.surveygroup", "group")

    def createSurvey(self):
        surveygroup=self.createSurveyGroup()
        return createContentInContainer(surveygroup, "euphorie.survey", "survey")

    def createModule(self):
        survey=self.createSurvey()
        return createContentInContainer(survey, "euphorie.module", "module")

    def createRisk(self):
        module=self.createModule()
        return createContentInContainer(module, "euphorie.risk", "risk")

    def testImportSolution(self):
        snippet=objectify.fromstring(
        """<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <description>Add more abstraction layers</description>
             <action-plan>Add another level</action-plan>
             <prevention-plan>Ask a code reviewer to verify the design</prevention-plan>
             <requirements>A good understanding of architecture</requirements>
           </solution>""")
        self.loginAsPortalOwner()
        risk=self.createRisk()
        importer=upload.SurveyImporter(None)
        importer.ImportSolution(snippet, risk)
        self.assertEqual(risk.keys(), ["3"])
        solution=risk["3"]
        self.assertEqual(solution.description, u"Add more abstraction layers")
        self.assertEqual(solution.action_plan, u"Add another level")
        self.assertEqual(solution.prevention_plan, u"Ask a code reviewer to verify the design")
        self.assertEqual(solution.requirements, u"A good understanding of architecture")

    def testImportSolution_MissingFields(self):
        snippet=objectify.fromstring(
        """<solution xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <description>Add more abstraction layers</description>
             <action-plan>Add another level</action-plan>
           </solution>""")
        self.loginAsPortalOwner()
        risk=self.createRisk()
        importer=upload.SurveyImporter(None)
        importer.ImportSolution(snippet, risk)
        solution=risk["3"]
        self.assertEqual(solution.description, u"Add more abstraction layers")
        self.assertEqual(solution.action_plan, u"Add another level")
        self.assertEqual(solution.prevention_plan, None)
        self.assertEqual(solution.requirements, None)

    def testImportRisk(self):
        snippet=objectify.fromstring(
        """<risk type="policy" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <problem-description>Not all desks are set to the right height.</problem-description>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <legal-reference>&lt;p&gt;See ARBO policies.&lt;/p&gt;</legal-reference>
             <show-not-applicable>yes</show-not-applicable>
             <evaluation-method>direct</evaluation-method>
           </risk>""")
        self.loginAsPortalOwner()
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportRisk(snippet, module)
        risk=module["2"]
        self.assertEqual(risk.title, u"Are your desks at the right height?")
        self.assertEqual(risk.problem_description, u"Not all desks are set to the right height.")
        self.assertEqual(risk.description, u"<p>The right height is important to prevent back problems.</p>")
        self.assertEqual(risk.legal_reference, u"<p>See ARBO policies.</p>")
        self.assertEqual(risk.show_notapplicable, True)
        self.assertEqual(risk.evaluation_method, "direct")
        self.assertEqual(risk.keys(), [])

    def testImportRisk_CalculatedEvaluation(self):
        snippet=objectify.fromstring(
        """<risk type="policy" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <evaluation-method default-probability="1" default-frequency="2" default-effect="3">calculated</evaluation-method>
           </risk>""")
        self.loginAsPortalOwner()
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportRisk(snippet, module)
        risk=module["2"]
        self.assertEqual(risk.show_notapplicable, False)
        self.assertEqual(risk.evaluation_method, "calculated")
        self.assertEqual(risk.default_probability, 1)
        self.assertEqual(risk.default_frequency, 2)
        self.assertEqual(risk.default_effect, 3)

    def testImportRisk_WithLinks(self):
        snippet=objectify.fromstring(
        """<risk type="policy" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Are your desks at the right height?</title>
             <description>&lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;</description>
             <evaluation-method>direct</evaluation-method>
             <links>
               <link>
                 <url>http://en.wikipedia.org/wiki/Computer_desk</url>
                 <title>Computer desks</title>
               </link>
               <link>
                 <url>http://en.wikipedia.org/wiki/Repetitive_strain_injury</url>
                 <title>Repetetive strain injury</title>
               </link>
             </links>
           </risk>""")
        self.loginAsPortalOwner()
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportRisk(snippet, module)
        risk=module["2"]
        self.assertEqual(risk.keys(), [])
        self.assertEqual(len(risk.links), 2)
        self.assertEqual(risk.links[0].url, u"http://en.wikipedia.org/wiki/Computer_desk")
        self.assertEqual(risk.links[0].title, u"Computer desks")
        self.assertEqual(risk.links[1].url, u"http://en.wikipedia.org/wiki/Repetitive_strain_injury")
        self.assertEqual(risk.links[1].title, u"Repetetive strain injury")

    def testImportRisk_WithSolution(self):
        snippet=objectify.fromstring(
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
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportRisk(snippet, module)
        risk=module["2"]
        self.assertEqual(risk.keys(), ["3"])
        solution=risk["3"]
        from euphorie.content.solution import Solution
        self.failUnless(isinstance(solution, Solution))
        self.assertEqual(solution.description, u"Use height-adjustable desks")

    def testImportModule(self):
        snippet=objectify.fromstring(
        """<module optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <solution-direction>&lt;p&gt;Buy the book from the gang of four.&lt;/p&gt;</solution-direction>
           </module>""")
        self.loginAsPortalOwner()
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportModule(snippet, module)
        module=module["2"]
        self.assertEqual(module.title, u"Design patterns")
        self.assertEqual(module.optional, False)
        self.assertEqual(module.question, None)
        self.assertEqual(module.description, u"<p>Software design patterns are critical.</p>")
        self.assertEqual(module.solution_direction, u"<p>Buy the book from the gang of four.</p>")
        self.assertEqual(module.keys(), [])

    def testImportModule_Optional(self):
        snippet=objectify.fromstring(
        """<module optional="yes" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <question>Have you used design patterns?</question>
           </module>""")
        self.loginAsPortalOwner()
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportModule(snippet, module)
        module=module["2"]
        self.assertEqual(module.optional, True)
        self.assertEqual(module.question, u"Have you used design patterns?")

    def testImportModule_WithSubModule(self):
        snippet=objectify.fromstring(
        """<module optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Design patterns</title>
             <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             <module optional="no">
               <title>Iterators</title>
               <description>&lt;p&gt;Iterators help optimise list handling.&lt;/p&gt;</description>
             </module>
           </module>""")
        self.loginAsPortalOwner()
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportModule(snippet, module)
        module=module["2"]
        self.assertEqual(module.keys(), ["3"])
        module=module["3"]
        from euphorie.content.module import Module
        self.failUnless(isinstance(module, Module))
        self.assertEqual(module.title, u"Iterators")

    def testImportModule_WithRisk(self):
        snippet=objectify.fromstring(
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
        module=self.createModule()
        importer=upload.SurveyImporter(None)
        importer.ImportModule(snippet, module)
        module=module["2"]
        self.assertEqual(module.keys(), ["3"])
        risk=module["3"]
        from euphorie.content.risk import Risk
        self.failUnless(isinstance(risk, Risk))
        self.assertEqual(risk.title, u"New hires are not aware of design patterns.")

    def testImportProfileQuestion(self):
        snippet=objectify.fromstring(
        """<profile-question type="optional" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Laptop usage</title>
             <question>Do your employees use laptops?</question>
             <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
           </profile-question>""")
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        importer=upload.SurveyImporter(None)
        importer.ImportProfileQuestion(snippet, survey)
        profile=survey["1"]
        self.assertEqual(profile.title, u"Laptop usage")
        self.assertEqual(profile.type, "optional")
        self.assertEqual(profile.question, u"Do your employees use laptops?")
        self.assertEqual(profile.description, u"<p>Laptops are very common in the modern workplace.</p>")
        self.assertEqual(profile.keys(), [])

    def testImportProfileQuestion_WithModule(self):
        snippet=objectify.fromstring(
        """<profile-question type="optional" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Laptop usage</title>
             <question>Do your employees use laptops?</question>
             <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
             <module optional="no">
               <title>Design patterns</title>
               <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             </module>
           </profile-question>""")
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        importer=upload.SurveyImporter(None)
        importer.ImportProfileQuestion(snippet, survey)
        profile=survey["1"]
        self.assertEqual(profile.keys(), ["2"])
        module=profile["2"]
        from euphorie.content.module import Module
        self.failUnless(isinstance(module, Module))
        self.assertEqual(module.title, u"Design patterns")

    def testImportProfileQuestion_WithRisk(self):
        snippet=objectify.fromstring(
        """<profile-question type="optional" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
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
        survey=self.createSurvey()
        importer=upload.SurveyImporter(None)
        importer.ImportProfileQuestion(snippet, survey)
        profile=survey["1"]
        self.assertEqual(profile.keys(), ["2"])
        risk=profile["2"]
        from euphorie.content.risk import Risk
        self.failUnless(isinstance(risk, Risk))
        self.assertEqual(risk.title, u"New hires are not aware of design patterns.")

    def testImportSurvey(self):
        snippet=objectify.fromstring(
        """<survey xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <classification-code>A.1.2.3</classification-code>
             <evaluation-optional>yes</evaluation-optional>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup=self.createSurveyGroup()
        importer=upload.SurveyImporter(None)
        importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        survey=surveygroup["fresh-import"]
        self.assertEqual(survey.keys(), [])
        self.assertEqual(survey.title, u"Fresh import")
        self.assertEqual(survey.classification_code, u"A.1.2.3")
        self.assertEqual(survey.evaluation_optional, True)

    def testImportSurvey_WithModule(self):
        snippet=objectify.fromstring(
        """<survey optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <module optional="no">
               <title>Design patterns</title>
               <description>&lt;p&gt;Software design patterns are critical.&lt;/p&gt;</description>
             </module>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup=self.createSurveyGroup()
        importer=upload.SurveyImporter(None)
        importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        survey=surveygroup["fresh-import"]
        self.assertEqual(survey.keys(), ["1"])
        module=survey["1"]
        from euphorie.content.module import Module
        self.failUnless(isinstance(module, Module))
        self.assertEqual(module.title, u"Design patterns")

    def testImportSurvey_WithProfileQuestion(self):
        snippet=objectify.fromstring(
        """<survey optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <profile-question type="optional">
               <title>Laptop usage</title>
               <question>Do your employees use laptops?</question>
               <description>&lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;</description>
             </profile-question>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup=self.createSurveyGroup()
        importer=upload.SurveyImporter(None)
        importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        survey=surveygroup["fresh-import"]
        self.assertEqual(survey.keys(), ["1"])
        profile=survey["1"]
        from euphorie.content.profilequestion import ProfileQuestion
        self.failUnless(isinstance(profile, ProfileQuestion))
        self.assertEqual(profile.title, u"Laptop usage")

    def testImportSurvey_ChildOrdering(self):
        snippet=objectify.fromstring(
        """<survey optional="no" xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development</title>
             <module optional="no">
               <title>Module one</title>
               <description/>
             </module>
             <profile-question type="optional">
               <title>Profile one</title>
               <question/>
               <description/>
             </profile-question>
             <module optional="no">
               <title>Module two</title>
               <description/>
             </module>
             <profile-question type="optional">
               <title>Profile two</title>
               <question/>
               <description/>
             </profile-question>
           </survey>""")
        self.loginAsPortalOwner()
        surveygroup=self.createSurveyGroup()
        importer=upload.SurveyImporter(None)
        importer.ImportSurvey(snippet, surveygroup, u"Fresh import")
        self.assertEqual(surveygroup.keys(), ["fresh-import"])
        survey=surveygroup["fresh-import"]
        self.assertEqual(survey.keys(), ["1", "2", "3", "4"])
        children=survey.values()
        self.assertEquals(children[0].title, u"Module one")
        self.assertEquals(children[1].title, u"Profile one")
        self.assertEquals(children[2].title, u"Module two")
        self.assertEquals(children[3].title, u"Profile two")


class SectorImporterTests(EuphorieContentTestCase):
    def createCountry(self):
        self.portal.invokeFactory("euphorie.sectorcontainer", "sectors")
        container=self.portal.sectors
        return createContentInContainer(container, "euphorie.country", "nl")

    def testImportSurvey(self):
        snippet=objectify.fromstring(
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development sector</title>
             <survey>
               <title>Software development</title>
             </survey>
           </sector>""")
        self.loginAsPortalOwner()
        country=self.createCountry()
        importer=upload.SectorImporter(country)
        importer(snippet, None, None, u"Import")
        self.assertEqual(country.keys(), ["software-development-sector"])
        sector=country["software-development-sector"]
        self.assertEqual(sector.title, "Software development sector")
        self.assertEqual(sector.keys(), ["software-development"])
        self.assertEqual(sector.contact_email, None)
        self.assertEqual(sector.password, None)
        group=sector["software-development"]
        self.assertEqual(group.title, "Software development")
        self.assertEqual(group.keys(), ["import"])

    def testImportSurvey_WithAccount(self):
        snippet=objectify.fromstring(
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development sector</title>
             <account login="coders" password="s3cr3t" />
             <contact>
               <name>Team lead</name>
               <email>discard@simplon.biz</email>
             </contact>
           </sector>""")
        self.loginAsPortalOwner()
        country=self.createCountry()
        importer=upload.SectorImporter(country)
        importer(snippet, None, None, u"Import")
        sector=country["software-development-sector"]
        self.assertEqual(sector.login, u"coders")
        self.assertEqual(sector.contact_name, u"Team lead")
        self.assertEqual(sector.contact_email, u"discard@simplon.biz")
        self.assertEqual(sector.password, "s3cr3t")

    def testImportSurvey_WithLogo(self):
        snippet=objectify.fromstring(
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>Software development sector</title>
             <logo filename="tiny.gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</logo>
           </sector>""")
        self.loginAsPortalOwner()
        country=self.createCountry()
        importer=upload.SectorImporter(country)
        importer(snippet, None, None, u"Import")
        sector=country["software-development-sector"]
        self.assertNotEqual(sector.logo, None)
        self.assertEqual(sector.logo.filename, "tiny.gif")
        self.assertEqual(sector.logo.contentType, "image/gif")
        self.assertEqual(sector.logo.data, "GIF89a\x01\x00\x01\x00\x80\x00\x00"
                                           "\x00\x00\x00\xff\xff\xff!\xf9\x04"
                                           "\x01\x00\x00\x01\x00,\x00\x00\x00"
                                           "\x00\x01\x00\x01\x00\x00\x02\x01L"
                                           "\x00;")


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
