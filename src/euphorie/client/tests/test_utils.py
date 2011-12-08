import unittest
from euphorie.client import utils


class MockRequest:
    def __init__(self, agent=None):
        self.__headers = {}
        if agent is not None:
            self.__headers['User-Agent'] = agent

    def get_header(self, key, default):
        return self.__headers.get(key, default)


class WebhelperTests(unittest.TestCase):
    def _createView(self, agent=None):
        from euphorie.client.utils import WebHelpers
        return WebHelpers(None, MockRequest(agent))

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
                      'Version/4.0 Mobile/7A341 Safari/528.16')
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
        from OFS.SimpleItem import SimpleItem
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
                utils.RelativePath(child2, grandchild),
                '../child1/grandchild')


class MatchColourTests(unittest.TestCase):
    def from_hls(self, h, l, s):
        import colorsys
        (r, g, b) = colorsys.hls_to_rgb(h, l, s)
        return '#%02x%02x%02x' % (r * 255, g * 255, b * 255)

    def to_hls(self, colour):
        import colorsys
        from PIL.ImageColor import getrgb
        (r, g, b) = getrgb(colour)
        return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    def testLowLuminosity(self):
        self.assertAlmostEqual(
                self.to_hls(utils.MatchColour(self.from_hls(0, 0, 0)))[1],
                0.65, 2)

    def testHighLuminosity(self):
        self.assertAlmostEqual(
                self.to_hls(utils.MatchColour(self.from_hls(0, 0.8, 0)))[1],
                0.2, 2)

    def testYellowishColour(self):
        self.assertAlmostEqual(
                self.to_hls(utils.MatchColour(self.from_hls(0.20, 0, 0)))[1],
                0.65, 2)


class RandomStringTests(unittest.TestCase):
    def testOutputChanges(self):
        self.assertNotEquals(utils.randomString(), utils.randomString())

    def testLength(self):
        self.assertEquals(len(utils.randomString(5)), 5)
