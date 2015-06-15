from euphorie.client.tests.database import DatabaseTests
from euphorie.client import model
from euphorie.client import config
from z3c.saconfig import Session


def createSurvey():
    session = Session()
    account = model.Account(loginname=u"jane", password=u"secret")
    session.add(account)
    survey = model.SurveySession(title=u"Session", zodb_path="survey",
            account=account)
    session.add(survey)
    session.flush()
    return (session, survey)


class SurveySessionTests(DatabaseTests):
    def testNoChildren(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title=u"Root", module_id="1",
            zodb_path="1"))
        ses.add(root)
        ses.flush()
        self.assertEqual(root.children().count(), 0)

    def testAddChild(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title=u"Root", module_id="1",
            zodb_path="1"))
        ses.add(root)
        root.addChild(model.Module(title=u"Module", module_id="1",
            zodb_path="1/1"))
        ses.flush()
        self.assertEqual(root.children().count(), 1)

    def testChildOrder(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title=u"Root", module_id="1",
            zodb_path="1"))
        ses.add(root)
        ses.flush()
        root.addChild(
            model.Module(title=u"Profile 5", module_id="5", zodb_path="1/5"))
        root.addChild(
            model.Module(title=u"Profile 1", module_id="1", zodb_path="1/1"))
        root.addChild(
            model.Module(title=u"Profile 3", module_id="3", zodb_path="1/3"))
        ses.flush()
        self.assertEqual(
                [c.module_id for c in list(root.children())],
                [u"5", "1", "3"])

    def testReset_NoChildren(self):
        (ses, survey) = createSurvey()
        survey.reset()
        children = ses.query(model.SurveyTreeItem.id)\
                .filter(model.SurveyTreeItem.session == survey)
        self.assertEqual(children.count(), 0)

    def testReset_SingleChild(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(
            title=u"Root", module_id="1", zodb_path="1"))
        ses.add(root)
        children = ses.query(model.SurveyTreeItem.id)\
                .filter(model.SurveyTreeItem.session == survey)
        self.assertEqual(children.count(), 1)
        survey.reset()
        self.assertEqual(children.count(), 0)

    def testHasTree_NoChildren(self):
        (ses, survey) = createSurvey()
        self.assertEqual(survey.hasTree(), False)

    def testHasTree_SingleChild(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(
                model.Module(title=u"Root", module_id="1", zodb_path="1"))
        ses.add(root)
        self.assertEqual(survey.hasTree(), True)


class RiskPresentFilterTests(DatabaseTests):
    def createData(self):
        (self.session, self.survey) = createSurvey()
        self.mod1 = model.Module(title=u"Module 1", module_id="1",
                zodb_path="1", skip_children=False)
        self.survey.addChild(self.mod1)
        self.q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1",
                type="risk", identification="no")
        self.mod1.addChild(self.q1)

    def query(self):
        return self.session.query(model.SurveyTreeItem)\
                .filter(model.RISK_PRESENT_FILTER)

    def testValidRisk(self):
        self.createData()
        self.assertEqual(self.query().count(), 1)

    def testIncludeTop5(self):
        self.createData()
        self.q1.risk_type = "top5"
        self.assertEqual(self.query().count(), 1)

    def testNoPresentRisk(self):
        self.createData()
        self.q1.identification = "n/a"
        self.assertEqual(self.query().count(), 0)


class RiskPresentNoTop5FilterTests(DatabaseTests):
    def createData(self):
        (self.session, self.survey) = createSurvey()
        self.mod1 = model.Module(title=u"Module 1", module_id="1",
                zodb_path="1", skip_children=False)
        self.survey.addChild(self.mod1)
        self.q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1",
                type="risk", identification="no")
        self.mod1.addChild(self.q1)

    def query(self):
        return self.session.query(model.SurveyTreeItem)\
                .filter(model.RISK_PRESENT_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER)

    def testValidRisk(self):
        self.createData()
        self.assertEqual(self.query().count(), 1)

    def testSkipTop5(self):
        self.createData()
        self.q1.risk_type = "top5"
        self.assertEqual(self.query().count(), 0)

    def testSkipPolicy(self):
        self.createData()
        self.q1.risk_type = "policy"
        self.assertEqual(self.query().count(), 0)

    def testNoPresentRisk(self):
        self.createData()
        self.q1.identification = "n/a"
        self.assertEqual(self.query().count(), 0)


class ModuleWithRiskFilterTests(DatabaseTests):
    def createData(self):
        (self.session, self.survey) = createSurvey()
        self.mod1 = model.Module(title=u"Module 1", module_id="1",
                zodb_path="1", skip_children=False)
        self.survey.addChild(self.mod1)
        self.q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1",
                type="risk", identification="no")
        self.mod1.addChild(self.q1)

    def query(self):
        return self.session.query(model.SurveyTreeItem)\
                .filter(model.MODULE_WITH_RISK_FILTER)

    def testValidModule(self):
        self.createData()
        self.assertEqual(self.query().count(), 1)

    def testSkipChildren(self):
        self.createData()
        self.mod1.skip_children = True
        self.assertEqual(self.query().count(), 0)

    def testNoPresentRisk(self):
        self.createData()
        self.q1.identification = "n/a"
        self.assertEqual(self.query().count(), 0)

    def testNoChildren(self):
        (self.session, self.survey) = createSurvey()
        self.session.add(self.survey)
        self.mod1 = model.Module(title=u"Module 1", module_id="1",
                zodb_path="1", skip_children=False)
        self.survey.addChild(self.mod1)
        self.assertEqual(self.query().count(), 0)


class AccountTests(DatabaseTests):

    def testGlobalRoles(self):
        user = model.Account()
        self.assertEqual(user.getRoles(), ("EuphorieUser",))

    def testRolesInContext(self):
        user = model.Account()
        self.assertEqual(user.getRolesInContext(None), ("EuphorieUser",))

    def testNoViewPermission(self):
        user = model.Account()
        self.assertEqual(user.has_permission("View", None), False)

    def testHasSurveyViewPermission(self):
        user = model.Account()
        self.assertEqual(
                user.has_permission("Euphorie: View a Survey", None), True)

    def testNonLicetLoviNonLicetBovi(self):
        from AccessControl.PermissionRole import _what_not_even_god_should_do
        user = model.Account()
        self.assertEqual(
                user.allowed(None, _what_not_even_god_should_do), False)

    def testHasAnonymousRole(self):
        user = model.Account()
        self.assertEqual(user.allowed(None, "Anonymous"), True)

    def testHasAuthenticatedRole(self):
        user = model.Account()
        self.assertEqual(user.allowed(None, "Authenticated"), True)

    def testHasEuphorieUserRole(self):
        user = model.Account()
        self.assertEqual(user.allowed(None, "EuphorieUser"), True)

    def testNoOtherRole(self):
        user = model.Account()
        self.assertEqual(user.allowed(None, "Manager"), False)

    def testAccountType(self):
        from sqlalchemy.exc import StatementError
        (self.session, self.survey) = createSurvey()
        account = self.survey.account
        self.assertEqual(account.account_type, None)
        account.account_type = config.GUEST_ACCOUNT
        self.assertEqual(account.account_type, config.GUEST_ACCOUNT)
        self.session.flush() # check that exception is not raised
        account.account_type = config.CONVERTED_ACCOUNT
        self.session.flush() # check that exception is not raised
        self.assertEqual(account.account_type, config.CONVERTED_ACCOUNT)
        account.account_type = 'invalid'
        self.assertRaises(StatementError, self.session.flush)
