from euphorie.client import utils
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.country import ClientCountry
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.sector import ClientSector
from euphorie.client.tests.utils import testRequest
from euphorie.client.utils import locals
from euphorie.content.survey import Survey
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zope.interface import alsoProvides

import unittest


class MockRequest:
    form = {}

    def __init__(self, agent=None):
        self.__headers = {}
        if agent is not None:
            self.__headers["User-Agent"] = agent

    def purge_memoize(self):
        """Clean up the memoize cache."""
        try:
            self.__annotations__.pop("plone.memoize", None)
        except AttributeError:
            pass

    def get_header(self, key, default):
        return self.__headers.get(key, default)


class MockSession:
    def __init__(self, account=None):
        self.account = account


class TestURLs(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        # Set locals
        request = testRequest()
        locals.request = request
        self.loginAsPortalOwner()
        self.client = self.portal.client
        # Add survey
        self.client._setOb("en", ClientCountry("en"))
        country = self.client["en"]
        country._setOb("sector", ClientSector("sector"))
        country["sector"].title = "Test sector"
        country["sector"].id = "sector"
        sector = country["sector"]
        survey = Survey("survey")
        survey.title = "Test Survey"
        survey.introduction = "This is a survey that is well suited for tests"
        survey.language = "en"
        sector._setOb("survey", survey)

    def _get_view(self, context):
        request = self.request.clone()
        alsoProvides(request, IClientSkinLayer)
        return api.content.get_view("webhelpers", context, request)

    def testBaseURL(self):
        country = self.client["en"]
        survey = self.client["en"]["sector"]["survey"]

        view = self._get_view(self.client)
        self.assertEqual(view._base_url(), self.client.absolute_url())
        view = self._get_view(country)
        self.assertEqual(view._base_url(), country.absolute_url())

        view = self._get_view(survey)
        self.assertEqual(view._base_url(), survey.absolute_url())


class WebhelperTests(EuphorieIntegrationTestCase):
    def _createView(self, agent=None):
        return WebHelpers(self.portal.client, MockRequest(agent))

    def testIsIphone_NoUserAgent(self):
        self.assertEqual(self._createView().is_iphone, False)

    def testIsIphone_IE6(self):
        view = self._createView(
            agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; "
            "SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)"
        )
        self.assertEqual(view.is_iphone, False)

    def testIsIphone_iPhone30(self):
        view = self._createView(
            agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 3_0 like Mac OS X; "
            "en-us) AppleWebKit/528.18 (KHTML, like Gecko) "
            "Version/4.0 Mobile/7A341 Safari/528.16"
        )
        self.assertEqual(view.is_iphone, True)


class HasTextTests(unittest.TestCase):
    def testNone(self):
        self.assertEqual(utils.HasText(None), False)

    def testEmpty(self):
        self.assertEqual(utils.HasText(""), False)

    def testSimpleText(self):
        self.assertEqual(utils.HasText("Hello, World"), True)

    def testWhitespaceOnly(self):
        self.assertEqual(utils.HasText("   &nbsp;"), False)

    def testTagsOnly(self):
        self.assertEqual(utils.HasText("<strong></strong>"), False)

    def testWhitespaceInTag(self):
        self.assertEqual(utils.HasText("<strong>  </strong>"), False)

    def testTagsAndText(self):
        self.assertEqual(utils.HasText("<strong>STRONG</strong>"), True)


class RandomStringTests(unittest.TestCase):
    def testOutputChanges(self):
        self.assertNotEqual(utils.randomString(), utils.randomString())

    def testLength(self):
        self.assertEqual(len(utils.randomString(5)), 5)
