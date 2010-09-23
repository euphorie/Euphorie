import os.path
from Testing.ZopeTestCase import installPackage
from Testing.ZopeTestCase import installProduct
from collective.testcaselayer import ptc
from Products.PloneTestCase import PloneTestCase

PloneTestCase.setupPloneSite()

# This should in theory work in the afterSetUp() method, but it does not work there
installProduct("membrane")

TEST_INI = os.path.join(os.path.dirname(__file__), "test.ini")

class EuphorieTestLayer(ptc.BasePTCLayer):
    def afterSetUp(self):
        from Products.Five import zcml
        from Products.Five import fiveconfigure
        import euphorie.deployment
        import euphorie.client.tests

        fiveconfigure.debug_mode = True
        zcml.load_config("configure.zcml", euphorie.deployment)
        zcml.load_config("overrides.zcml", euphorie.deployment)
        zcml.load_config("configure.zcml", euphorie.client.tests)
        fiveconfigure.debug_mode = False

        installPackage("plone.uuid")
        installPackage("collective.indexing")
        installPackage("plone.app.dexterity")
        installPackage("plone.app.folder")
        installPackage("euphorie.content")
        installPackage("euphorie.client")
        installPackage("euphorie.deployment")
        installPackage("plonetheme.nuplone")

        self.addProduct("euphorie.deployment")

        from euphorie.client import model
        from z3c.saconfig import Session
        model.metadata.create_all(Session.bind, checkfirst=True)

        from zope.component import getUtility
        from z3c.appconfig.interfaces import IAppConfig

        appconfig=getUtility(IAppConfig)
        appconfig.loadConfig(TEST_INI, clear=True)

    def beforeTearDown(self):
        from euphorie.client import model
        from z3c.saconfig import Session
        Session.remove()
        model.metadata.drop_all(Session.bind)


    # XXX testSetUp and testTearDown should not be neceesary, but it seems
    # SQL data is not correctly cleared at the end of a test method run,
    # even if testTearDown does an explicit transaction.abort()
    def testSetUp(self):
        from euphorie.client import model
        from z3c.saconfig import Session
        model.metadata.create_all(Session.bind, checkfirst=True)

    def testTearDown(self):
        from euphorie.client import model
        from z3c.saconfig import Session
        Session.remove()
        model.metadata.drop_all(Session.bind)


EuphorieLayer = EuphorieTestLayer([ptc.ptc_layer])


class EuphorieTestCase(PloneTestCase.PloneTestCase):
    layer = EuphorieLayer



class EuphorieFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    layer = EuphorieLayer


