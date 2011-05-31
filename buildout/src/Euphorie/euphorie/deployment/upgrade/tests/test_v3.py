from euphorie.deployment.tests.functional import EuphorieTestCase


class set_evaluation_method_interfaces_tests(EuphorieTestCase):
    def set_evaluation_method_interfaces(self, *a, **kw):
        from euphorie.deployment.upgrade.v3 import set_evaluation_method_interfaces
        return set_evaluation_method_interfaces(*a, **kw)

    def test_empty_site(self):
        self.set_evaluation_method_interfaces(self.portal)

    def test_risk_with_interfaces_already_set(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.risk import IKinneyEvaluation
        from euphorie.content.risk import IFrenchEvaluation
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        risk = survey["1"]["2"]
        self.assertTrue(IKinneyEvaluation.providedBy(risk))
        self.assertTrue(not IFrenchEvaluation.providedBy(risk))
        self.set_evaluation_method_interfaces(self.portal)
        self.assertTrue(IKinneyEvaluation.providedBy(risk))
        self.assertTrue(not IFrenchEvaluation.providedBy(risk))

    def test_set_kinney_interface(self):
        from zope.interface import noLongerProvides
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.risk import IKinneyEvaluation
        from euphorie.content.risk import IFrenchEvaluation
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        risk = survey["1"]["2"]
        noLongerProvides(risk, IKinneyEvaluation)
        self.assertTrue(not IKinneyEvaluation.providedBy(risk))
        self.set_evaluation_method_interfaces(self.portal)
        self.assertTrue(IKinneyEvaluation.providedBy(risk))
        self.assertTrue(not IFrenchEvaluation.providedBy(risk))

    def test_set_french_interface(self):
        from Acquisition import aq_parent
        from zope.interface import noLongerProvides
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.risk import IKinneyEvaluation
        from euphorie.content.risk import IFrenchEvaluation
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        aq_parent(survey).evaluation_algorithm = u"french"
        risk = survey["1"]["2"]
        noLongerProvides(risk, IKinneyEvaluation)
        self.set_evaluation_method_interfaces(self.portal)
        self.assertTrue(not IKinneyEvaluation.providedBy(risk))
        self.assertTrue(IFrenchEvaluation.providedBy(risk))

