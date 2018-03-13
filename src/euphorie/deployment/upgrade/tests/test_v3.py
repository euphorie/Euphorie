from euphorie.testing import EuphorieFunctionalTestCase


class set_evaluation_method_interfaces_tests(EuphorieFunctionalTestCase):
    def set_evaluation_method_interfaces(self, *a, **kw):
        from euphorie.deployment.upgrade.v3 \
                import set_evaluation_method_interfaces
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


class convert_solution_description_to_text_tests(EuphorieFunctionalTestCase):
    def convert_solution_description_to_text(self, *a, **kw):
        from euphorie.deployment.upgrade.v3 \
                import convert_solution_description_to_text
        return convert_solution_description_to_text(*a, **kw)

    def test_empty_site(self):
        self.convert_solution_description_to_text(self.portal)

    def test_rich_description(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        risk = survey['1']['2']
        risk.invokeFactory('euphorie.solution', '3')
        solution = risk['3']
        solution.description = u'<p>This is my description.</p>'
        self.convert_solution_description_to_text(self.portal)
        self.assertEqual(solution.description,
                u'This is my description.')

    def test_text_description(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        risk = survey['1']['2']
        risk.invokeFactory('euphorie.solution', '3')
        solution = risk['3']
        solution.description = u'This is my description.'
        self.convert_solution_description_to_text(self.portal)
        self.assertEqual(solution.description,
                u'This is my description.')


class lowercase_login_tests(EuphorieFunctionalTestCase):
    def lowercase_login(self, *a, **kw):
        from euphorie.deployment.upgrade.v3 import lowercase_login
        return lowercase_login(*a, **kw)

    def test_already_lowercase(self):
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        session = Session()
        account = Account(loginname='jane@example.com', password=u'john')
        session.add(account)
        self.lowercase_login(None)
        session.expire(account)
        self.assertEqual(account.loginname, 'jane@example.com')

    def test_uppercase_login(self):
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        session = Session()
        account = Account(loginname='JaNe@ExAmPlE.CoM', password=u'john')
        session.add(account)
        self.lowercase_login(None)
        session.expire(account)
        self.assertEqual(account.loginname, 'jane@example.com')
