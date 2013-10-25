import os.path
from Testing.ZopeTestCase import installProduct
from collective.testcaselayer import ptc
from Products.PloneTestCase import PloneTestCase

PloneTestCase.setupPloneSite()

# This should in theory work in the afterSetUp() method, but it does not work
# there.
installProduct("membrane")

TEST_INI = os.path.join(os.path.dirname(__file__), "test.ini")


class EuphorieTestLayer(ptc.BasePTCLayer):
    def afterSetUp(self):
        from Testing.ZopeTestCase import installPackage
        import euphorie.deployment
        import euphorie.client.tests

        self.loadZCML("configure.zcml", package=euphorie.deployment)
        self.loadZCML("overrides.zcml", package=euphorie.deployment)
        self.loadZCML("configure.zcml", package=euphorie.client.tests)

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

        appconfig = getUtility(IAppConfig)
        appconfig.loadConfig(TEST_INI, clear=True)

    def beforeTearDown(self):
        from euphorie.client import model
        from euphorie.client import utils
        from z3c.saconfig import Session
        Session.remove()
        model.metadata.drop_all(Session.bind)
        utils.setRequest(None)

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

    def runTest(self):
        pass

    def adminBrowser(self):
        """Return a browser logged in as the site owner."""
        from Products.PloneTestCase.setup import portal_owner
        from Products.PloneTestCase.setup import default_password
        from Products.Five.testbrowser import Browser
        browser = Browser()
        browser.open("%s/@@login" % self.portal.absolute_url())
        browser.getControl(name="__ac_name").value = portal_owner
        browser.getControl(name="__ac_password").value = default_password
        browser.getForm(id="loginForm").submit()
        return browser
