from Testing.ZopeTestCase import installPackage
from Testing.ZopeTestCase import installProduct
from collective.testcaselayer import ptc
from Products.PloneTestCase import PloneTestCase

PloneTestCase.setupPloneSite()

# This should in theory work in the afterSetUp() method, but it does not work there
installProduct("membrane")

class EuphorieContentTestLayer(ptc.BasePTCLayer):
    def afterSetUp(self):
        from Products.Five import zcml
        from Products.Five import fiveconfigure
        import euphorie.content

        fiveconfigure.debug_mode = True
        zcml.load_config("configure.zcml", euphorie.content)
        zcml.load_config("overrides.zcml", euphorie.content)
        fiveconfigure.debug_mode = False

        installPackage("collective.indexing")
        installPackage("plone.app.dexterity")
        installPackage("plone.app.folder")
        installPackage("euphorie.content")

        self.addProduct("euphorie.content")

EuphorieContentLayer = EuphorieContentTestLayer([ptc.ptc_layer])


class EuphorieContentTestCase(PloneTestCase.PloneTestCase):
    layer = EuphorieContentLayer



class EuphorieContentFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    layer = EuphorieContentLayer



