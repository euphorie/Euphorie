# coding=utf-8
from zope.interface import implementer
from plone.transformchain.interfaces import ITransform
from plone.app.theming.transform import ThemeTransform
# from lxml import etree


@implementer(ITransform)
class EuphorieTransform(ThemeTransform):
    """ A transform that comes after plone.app.theming.transform and before
    plone.protect.auto
    Since theming is not used in Euphorie, the only purpose of this transform
    is to ensure that we wrap the result into an XMLSerializer, so that the
    plone.protext transform does not mangle it. See:
    https://community.plone.org/t/where-does-url-quoting-of-links-happen/6643
    """

    order = 8870

    def transformIterable(self, result, encoding):
        """ Just make sure to call parseTree in order to wrap the result
        """
        result = self.parseTree(result)
        if result is None:
            return None
        # This is the attempt to make it work in the client, because
        # there we only have doctype html (HTML5).
        # However, this causes all pages in the client to be blank,
        # even though in source view it looks fine.
        # More debugging needed.
        # Until then, force doctype XMHTL on the risk_actionplan template,
        # the only location where this problem affects us negatively.
        # if (
        #     result.tree.docinfo.doctype and (
        #         'XHTML' in result.tree.docinfo.doctype or
        #         'html' in result.tree.docinfo.doctype
        #     )
        # ):
        #     result.serializer = etree.tostring
        return result
