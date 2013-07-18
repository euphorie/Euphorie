import unittest
from euphorie.client.country import ClientCountry


class ViewTests(unittest.TestCase):
    def setUp(self):
        from plone.folder.tests.layer import PloneFolderLayer
        PloneFolderLayer.setUp()

    def tearDown(Self):
        from zope.testing.cleanup import cleanUp
        cleanUp()

    def addSurvey(self, country, language, title):
        from euphorie.content.survey import Survey
        from euphorie.client.sector import ClientSector
        if "sector" not in country:
            country["sector"] = ClientSector()
            country["sector"].title = u"Test sector"
            country["sector"].id = "sector"
        sector = country["sector"]
        survey = Survey()
        survey.title = title
        survey.id = language
        survey.language = language
        sector[language] = survey
        return survey

    def surveys(self, country, language):
        from euphorie.client.country import View

        class Request:
            environ = {'REQUEST_METHOD': 'GET'}
            form = {}

            def __init__(self, language):
                self.language = language

            def __getattr__(self, key):
                if key in ["request", "locale", "id"]:
                    return self
                raise AttributeError(key)

        view = View(country, Request(language))
        view.update()
        return view.surveys

    def test_surveys_NoSurveys(self):
        country = ClientCountry()
        self.assertEqual(self.surveys(country, "en"), [])

    def test_surveys_WrongLanguage(self):
        country = ClientCountry()
        self.addSurvey(country, "en", u"Test survey")
        self.assertEqual(self.surveys(country, "nl"), [])

    def test_surveys_SameLanguage(self):
        country = ClientCountry()
        self.addSurvey(country, "en", u"Test survey")
        self.assertEqual(self.surveys(country, "en"),
                [{"id": "sector/en", "title": u"Test survey"}])

    def test_surveys_SurveyHasDialect(self):
        country = ClientCountry()
        self.addSurvey(country, "en-GB", u"Test survey")
        self.assertEqual(self.surveys(country, "en"),
                [{"id": "sector/en-GB", "title": u"Test survey"}])

    def test_surveys_SkipPreview(self):
        country = ClientCountry()
        survey = self.addSurvey(country, "en", u"Test survey")
        survey.preview = True
        self.assertEqual(self.surveys(country, "en"), [])
