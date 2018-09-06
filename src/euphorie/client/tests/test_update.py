# coding=utf-8
from euphorie.client import model
from euphorie.client import update
from euphorie.testing import EuphorieFunctionalTestCase
from plone.dexterity.utils import createContentInContainer
from z3c.saconfig import Session


class TreeTests(EuphorieFunctionalTestCase):

    def createClientSurvey(self):
        self.loginAsPortalOwner()
        self.client = self.portal.client
        self.client.invokeFactory("euphorie.clientcountry", "nl")
        createContentInContainer(
            self.client.nl,
            "euphorie.sector",
            checkConstraints=False,
            title=u"dining"
        )
        self.sector = self.client.nl.dining
        createContentInContainer(
            self.sector,
            "euphorie.survey",
            checkConstraints=False,
            title=u"Survey"
        )
        self.survey = self.sector.survey
        return self.survey

    def createSurveySession(self):
        self.sqlsession = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        self.sqlsession.add(account)
        self.session = model.SurveySession(
            title=u"Session", zodb_path="nl/dining/survey", account=account
        )
        self.sqlsession.add(self.session)
        self.sqlsession.flush()
        return self.session


class GetSurveyTreeTests(TreeTests):

    def testEmpty(self):
        survey = self.createClientSurvey()
        self.assertEqual(update.getSurveyTree(survey), [])

    def testSingleModule(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        self.assertEqual(
            update.getSurveyTree(survey), [{
                'optional': False,
                'zodb_path': '1',
                'type': 'module',
                'has_description': False,
                'always_present': False
            }]
        )

    def testModuleAndRisk(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        survey["1"].invokeFactory("euphorie.risk", "2")
        self.assertEqual(
            update.getSurveyTree(survey), [{
                'optional': False,
                'zodb_path': "1",
                'type': "module",
                'has_description': False,
                'always_present': False
            },
                                           {
                                               'optional': False,
                                               'zodb_path': '1/2',
                                               'type': 'risk',
                                               'has_description': False,
                                               'always_present': False
                                           }]
        )


class GetSessionTreeTests(TreeTests):

    def testEmpty(self):
        session = self.createSurveySession()
        self.assertEqual(update.getSessionTree(session), [])

    def testSingleModule(self):
        session = self.createSurveySession()
        session.addChild(
            model.Module(title=u"Root", module_id="1", zodb_path="1")
        )
        tree = update.getSessionTree(session)
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0].zodb_path, "1")
        self.assertEqual(tree[0].type, "module")
        self.assertEqual(tree[0].path, "001")

    def testModuleAndRisk(self):
        session = self.createSurveySession()
        root = model.Module(title=u"Root", module_id="1", zodb_path="1")
        session.addChild(root)
        root.addChild(
            model.Risk(
                title=u"Risk 1",
                risk_id="1",
                zodb_path="1/1",
                type="risk",
                identification="no"
            )
        )
        tree = update.getSessionTree(session)
        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0].zodb_path, "1")
        self.assertEqual(tree[0].type, "module")
        self.assertEqual(tree[0].path, "001")
        self.assertEqual(tree[1].zodb_path, "1/1")
        self.assertEqual(tree[1].type, "risk")
        self.assertEqual(tree[1].path, "001001")


class TreeChangesTests(TreeTests):

    def test_nothing_changes(self):
        session = self.createSurveySession()
        session_module = model.Module(
            title=u'Root',
            module_id='1',
            zodb_path='1',
            skip_children=False,
            has_description=False
        )
        session.addChild(session_module)
        session_module.addChild(
            model.Risk(
                title=u'Risk 1',
                risk_id='2',
                zodb_path='1/2',
                type='risk',
                identification='no'
            )
        )
        survey = self.createClientSurvey()
        survey.invokeFactory('euphorie.module', '1')
        survey['1'].invokeFactory('euphorie.risk', '2')
        self.assertEqual(update.treeChanges(session, survey), set())

    def test_no_changes_with_repeated_profile(self):
        session = self.createSurveySession()
        for i in range(2):
            session_module = model.Module(
                title=u'Root',
                module_id='1',
                zodb_path='1',
                skip_children=False,
                profile_index=i
            )
            session.addChild(session_module)
            session_module.addChild(
                model.Risk(
                    title=u'Risk 1',
                    risk_id='2',
                    zodb_path='1/2',
                    type='risk',
                    identification='no'
                )
            )

        survey = self.createClientSurvey()
        survey.invokeFactory('euphorie.profilequestion', '1')
        survey['1'].invokeFactory('euphorie.risk', '2')
        self.assertEqual(update.treeChanges(session, survey), set())

    def testAddNewModule(self):
        session = self.createSurveySession()
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([("1", "module", "add")]))

    def test_add_new_risk(self):
        session = self.createSurveySession()
        session.addChild(
            model.Module(
                title=u"Root",
                module_id="1",
                zodb_path="1",
                has_description=False
            )
        )
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        survey["1"].invokeFactory("euphorie.risk", "2")
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([("1/2", "risk", "add")]))

    def testProfileActsAsModule(self):
        session = self.createSurveySession()
        session.addChild(
            model.Module(title=u"Root", module_id="1", zodb_path="1")
        )
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([]))

    def testRemoveModule(self):
        session = self.createSurveySession()
        session.addChild(
            model.Module(title=u"Root", module_id="1", zodb_path="1")
        )
        survey = self.createClientSurvey()
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([("1", "module", "remove")]))

    def test_remove_risk(self):
        session = self.createSurveySession()
        session.addChild(
            model.Module(
                title=u"Root",
                module_id="1",
                zodb_path="1",
                has_description=False
            )
        )
        session.addChild(
            model.Risk(
                title=u"Risk 1",
                risk_id="1",
                zodb_path="1/1",
                type="risk",
                identification="no"
            )
        )
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([("1/1", "risk", "remove")]))

    def test_module_lost_description(self):
        session = self.createSurveySession()
        session_module = model.Module(
            title=u"Root",
            module_id="1",
            zodb_path="1",
            skip_children=False,
            has_description=True
        )
        session.addChild(session_module)
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        module = survey['1']
        module.description = u'<p></p>'
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([('1', 'module', 'modified')]))

    def test_module_gained_description(self):
        session = self.createSurveySession()
        session_module = model.Module(
            title=u"Root",
            module_id="1",
            zodb_path="1",
            skip_children=False,
            has_description=False
        )
        session.addChild(session_module)
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        module = survey['1']
        module.description = u'<p>Hello</p>'
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([('1', 'module', 'modified')]))

    def testModuleMadeRequired(self):
        session = self.createSurveySession()
        session_module = model.Module(
            title=u"Root", module_id="1", zodb_path="1", skip_children=True
        )
        session.addChild(session_module)
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        module = survey['1']
        module.optional = False
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([('1', 'module', 'modified')]))

    def test_module_made_optional(self):
        """
        Note: an optional module is always considered to have a description, so
        that is never gets skipped.
        See https://github.com/euphorie/Euphorie/commit/c277d05
        """
        session = self.createSurveySession()
        session_module = model.Module(
            title=u"Root",
            module_id="1",
            zodb_path="1",
            has_description=True,
            skip_children=False
        )
        session.addChild(session_module)
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        module = survey['1']
        module.optional = True
        changes = update.treeChanges(session, survey)
        self.assertEqual(changes, set([]))
