from Testing.ZopeTestCase import installPackage
from Testing.ZopeTestCase import installProduct
from collective.testcaselayer import ptc
from Products.PloneTestCase import PloneTestCase

PloneTestCase.setupPloneSite()

# This should in theory work in the afterSetUp() method, but it does not work there
installProduct("membrane")

class EuphorieClientTestLayer(ptc.BasePTCLayer):
    def afterSetUp(self):
        from Products.Five import zcml
        from Products.Five import fiveconfigure
        import euphorie.client
        import euphorie.client.tests

        fiveconfigure.debug_mode = True
        zcml.load_config("configure.zcml", euphorie.client)
        zcml.load_config("overrides.zcml", euphorie.client)
        zcml.load_config("configure.zcml", euphorie.client.tests)
        fiveconfigure.debug_mode = False

        installPackage("collective.indexing")
        installPackage("plone.app.dexterity")
        installPackage("plone.app.folder")
        installPackage("euphorie.content")
        installPackage("euphorie.client")

        self.addProduct("euphorie.client")

        from euphorie.client import model
        from z3c.saconfig import Session
        model.metadata.create_all(Session.bind, checkfirst=True)

    def beforeTearDown(self):
        from euphorie.client import model
        from z3c.saconfig import Session
        Session.remove()
        model.metadata.drop_all(Session.bind)


EuphorieClientLayer = EuphorieClientTestLayer([ptc.ptc_layer])


class EuphorieClientTestCase(PloneTestCase.PloneTestCase):
    layer = EuphorieClientLayer



class EuphorieClientFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    layer = EuphorieClientLayer

