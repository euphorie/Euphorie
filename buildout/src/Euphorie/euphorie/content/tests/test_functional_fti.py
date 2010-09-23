from zope.component import adapts
from zope.component import provideAdapter
from zope.interface import implements
from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.content.fti import ConditionalDexterityFTI
from euphorie.content.fti import IConstructionFilter
from euphorie.content.module import Module


class Veto(object):
    adapts(ConditionalDexterityFTI, Module)
    implements(IConstructionFilter)

    def __init__(self, fti, container):
        self.fti=fti
        self.container=container

    def allowed(self):
        return False


class ConditionalDexterityFTITests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createContent(self):
        self.setRoles(["Manager"])
        self.country=self.portal.sectors.nl
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "survey")

    def testConditionalFtiUsedByModule(self):
        fti=getattr(self.portal.portal_types, "euphorie.module")
        self.failUnless(isinstance(fti, ConditionalDexterityFTI))

    def testVeto(self):
        self.createContent()
        provideAdapter(Veto, name="euphorie.module")
        try:
            fti=getattr(self.portal.portal_types, "euphorie.module")
            self.assertEqual(fti.isConstructionAllowed(self.module), False)
        finally:
            from zope.component import getGlobalSiteManager
            getGlobalSiteManager().unregisterAdapter(Veto, name="euphorie.module")

    def testVetoRegisteredForOtherType(self):
        self.createContent()
        provideAdapter(factory=Veto, name="euphorie.solution")
        try:
            fti=getattr(self.portal.portal_types, "euphorie.module")
            self.assertEqual(fti.isConstructionAllowed(self.module), True)
        finally:
            from zope.component import getGlobalSiteManager
            getGlobalSiteManager().unregisterAdapter(Veto, name="euphorie.solution")

