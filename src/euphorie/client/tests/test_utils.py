# coding=utf-8
from euphorie.client import utils
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.country import ClientCountry
from euphorie.client.sector import ClientSector
from euphorie.client.tests.utils import testRequest
from euphorie.client.utils import locals
from euphorie.content.survey import Survey
from euphorie.testing import EuphorieIntegrationTestCase
from OFS.SimpleItem import SimpleItem
from PIL.ImageColor import getrgb
from zope.annotation import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.component import getGlobalSiteManager

import colorsys
import mock
import unittest


class MockRequest(object):
    form = {}

    def __init__(self, agent=None):
        self.__headers = {}
        if agent is not None:
            self.__headers['User-Agent'] = agent

    def purge_memoize(self):
        ''' Clean up the memoize cache
        '''
        try:
            self.__annotations__.pop('plone.memoize', None)
        except AttributeError:
            pass

    def get_header(self, key, default):
        return self.__headers.get(key, default)


class MockSession(object):

    def __init__(self, account=None):
        self.account = account


class TestURLs(EuphorieIntegrationTestCase):

    def setUp(self):
        super(TestURLs, self).setUp()
        # Set locals
        request = testRequest()
        locals.request = request
        self.loginAsPortalOwner()
        self.client = self.portal.client
        # Add survey
        self.client._setOb('en', ClientCountry('en'))
        country = self.client['en']
        country._setOb("sector", ClientSector('sector'))
        country["sector"].title = u"Test sector"
        country["sector"].id = "sector"
        sector = country["sector"]
        survey = Survey('survey')
        survey.title = u'Test Survey'
        survey.introduction = u"This is a survey that is well suited for tests"
        survey.language = 'en'
        sector._setOb('survey', survey)

    def testBaseURL(self):
        country = self.client['en']
        survey = self.client['en']['sector']['survey']

        request = testRequest()
        request.client = self.client
        view = WebHelpers(self.client, request)
        self.assertTrue(
            view._base_url().startswith(self.client.absolute_url())
        )
        self.assertFalse(view._base_url().startswith(country.absolute_url()))

        view = WebHelpers(country, testRequest())
        self.assertTrue(view._base_url().startswith(country.absolute_url()))

        request = testRequest()
        view = WebHelpers(survey, testRequest())
        view._survey = survey
        self.assertTrue(view._base_url().startswith(survey.absolute_url()))

        view = WebHelpers(country, testRequest())
        self.assertFalse(view._base_url().startswith(survey.absolute_url()))
        self.assertTrue(view._base_url().startswith(country.absolute_url()))


class WebhelperUnitTests(unittest.TestCase):

    def patch_view(self, name, is_property=False):
        dotted = '.'.join((WebHelpers.__module__, WebHelpers.__name__, name))
        if is_property:
            new_callable = mock.PropertyMock
        else:
            new_callable = None
        return mock.patch(dotted, new_callable=new_callable)

    def test_is_owner(self):
        # If no session is set is_owner return False
        # Allow memoize
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(
            AttributeAnnotations, (MockRequest, ), IAnnotations
        )

        view = WebHelpers(None, MockRequest())
        self.assertEqual(view.session, None)
        self.assertFalse(view.is_owner())
        # Otherwise we will return True is the session account is equal
        # to the current account
        with self.patch_view('session', is_property=True) as mocked_session:
            session = MockSession('account_1')
            mocked_session.return_value = session
            view.get_current_account = lambda: 'account_2'
            self.assertFalse(view.is_owner())
            view.get_current_account = lambda: 'account_1'
            view.request.purge_memoize()
            self.assertTrue(view.is_owner())


class WebhelperTests(EuphorieIntegrationTestCase):

    def _createView(self, agent=None):
        return WebHelpers(self.portal.client, MockRequest(agent))

    def testIsIphone_NoUserAgent(self):
        self.assertEqual(self._createView().is_iphone, False)

    def testIsIphone_IE6(self):
        view = self._createView(
            agent='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; '
            'SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)'
        )
        self.assertEqual(view.is_iphone, False)

    def testIsIphone_iPhone30(self):
        view = self._createView(
            agent='Mozilla/5.0 (iPod; U; CPU iPhone OS 3_0 like Mac OS X; '
            'en-us) AppleWebKit/528.18 (KHTML, like Gecko) '
            'Version/4.0 Mobile/7A341 Safari/528.16'
        )
        self.assertEqual(view.is_iphone, True)


class HasTextTests(unittest.TestCase):

    def testNone(self):
        self.assertEqual(utils.HasText(None), False)

    def testEmpty(self):
        self.assertEqual(utils.HasText(u''), False)

    def testSimpleText(self):
        self.assertEqual(utils.HasText(u'Hello, World'), True)

    def testWhitespaceOnly(self):
        self.assertEqual(utils.HasText(u'   &nbsp;'), False)

    def testTagsOnly(self):
        self.assertEqual(utils.HasText(u'<strong></strong>'), False)

    def testWhitespaceInTag(self):
        self.assertEqual(utils.HasText(u'<strong>  </strong>'), False)

    def testTagsAndText(self):
        self.assertEqual(utils.HasText(u'<strong>STRONG</strong>'), True)


class RelativePathTests(unittest.TestCase):

    def _createObject(self, id):
        obj = SimpleItem()
        obj.id = id
        return obj

    def testSameItem(self):
        obj = self._createObject('dummy')
        self.assertEqual(utils.RelativePath(obj, obj), '')

    def testDirectChild(self):
        parent = self._createObject('parent')
        child = self._createObject('child').__of__(parent)
        self.assertEqual(utils.RelativePath(parent, child), 'child')

    def testDirectParent(self):
        parent = self._createObject('parent')
        child = self._createObject('child').__of__(parent)
        self.assertEqual(utils.RelativePath(parent, child), 'child')

    def testOtherTree(self):
        parent = self._createObject('root')
        child1 = self._createObject('child1').__of__(parent)
        grandchild = self._createObject('grandchild').__of__(child1)
        child2 = self._createObject('child2').__of__(parent)
        self.assertEqual(
            utils.RelativePath(child2, grandchild), '../child1/grandchild'
        )


class MatchColourTests(unittest.TestCase):

    def from_hls(self, h, l, s):
        (r, g, b) = colorsys.hls_to_rgb(h, l, s)
        return '#%02x%02x%02x' % (r * 255, g * 255, b * 255)

    def to_hls(self, colour):
        (r, g, b) = getrgb(colour)
        return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    def testLowLuminosity(self):
        self.assertAlmostEqual(
            self.to_hls(utils.MatchColour(self.from_hls(0, 0, 0)))[1], 0.65, 2
        )

    def testHighLuminosity(self):
        self.assertAlmostEqual(
            self.to_hls(utils.MatchColour(self.from_hls(0, 0.8, 0)))[1], 0.2, 2
        )

    def testYellowishColour(self):
        self.assertAlmostEqual(
            self.to_hls(utils.MatchColour(self.from_hls(0.20, 0, 0)))[1], 0.65,
            2
        )


class RandomStringTests(unittest.TestCase):

    def testOutputChanges(self):
        self.assertNotEquals(utils.randomString(), utils.randomString())

    def testLength(self):
        self.assertEquals(len(utils.randomString(5)), 5)
