# coding=utf-8
from euphorie.client.country import ClientCountry
from euphorie.testing import EuphorieIntegrationTestCase
from zope.annotation import IAttributeAnnotatable
from zope.interface import implementer


class ViewTests(EuphorieIntegrationTestCase):

    def addSurvey(self, country, language, title):
        from euphorie.content.survey import Survey
        from euphorie.client.sector import ClientSector
        if "sector" not in country:
            sector = ClientSector(id='sector', title=u"Test sector")
            country._setOb("sector", sector)
        else:
            sector = country["sector"]
        survey = Survey()
        survey.title = title
        survey.id = language
        survey.language = language
        sector._setOb('language', survey)
        return survey

    def surveys(self, country, language):

        @implementer(IAttributeAnnotatable)
        class Request(object):
            environ = {'REQUEST_METHOD': 'GET'}
            form = {}

            def __init__(self, language):
                self.language = language

            def __getattr__(self, key):
                if key in ["request", "locale", "id"]:
                    return self
                raise AttributeError(key)

        with self._get_view('view', country) as view:
            view.request = Request(language)
            view._updateSurveys()
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
        self.assertEqual(
            self.surveys(country, "en"), [{
                "id": "sector/en",
                "title": u"Test survey"
            }]
        )

    def test_surveys_SurveyHasDialect(self):
        country = ClientCountry()
        self.addSurvey(country, "en-GB", u"Test survey")
        self.assertEqual(
            self.surveys(country, "en"), [{
                "id": "sector/en-GB",
                "title": u"Test survey"
            }]
        )

    def test_surveys_SkipPreview(self):
        country = ClientCountry()
        survey = self.addSurvey(country, "en", u"Test survey")
        survey.preview = True
        self.assertEqual(self.surveys(country, "en"), [])
