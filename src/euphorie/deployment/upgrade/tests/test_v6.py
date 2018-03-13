from euphorie.client.tests.database import DatabaseTests
from euphorie.testing import EuphorieFunctionalTestCase


class convert_to_module_tests(EuphorieFunctionalTestCase):
    def _convert_to_module(self, *a, **kw):
        from ..v6 import _convert_to_module
        return _convert_to_module(*a, **kw)

    def create_survey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        sector = createSector(self.portal)
        return addSurvey(sector, EMPTY_SURVEY)

    def test_basic(self):
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        question = createContentInContainer(survey, 'euphorie.profilequestion')
        question.title = u'Profile title'
        question.question = u'The question'
        question.description = u'<p>My description.</p>'
        module = self._convert_to_module(question)
        self.assertEqual(question.getPhysicalPath(), module.getPhysicalPath())
        self.assertEqual(module.title, u'Profile title')
        self.assertEqual(module.question, u'The question')
        self.assertEqual(module.description, u'<p>My description.</p>')
        self.assertEqual(module.optional, True)

    def test_keep_module_at_same_place_in_survey(self):
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        createContentInContainer(survey, 'euphorie.profilequestion')
        question = createContentInContainer(survey, 'euphorie.profilequestion')
        createContentInContainer(survey, 'euphorie.profilequestion')
        question.title = u'Profile title'
        question.question = u'The question'
        question.description = u'<p>My description.</p>'
        self._convert_to_module(question)
        self.assertEqual(survey.keys(), ['1', '2', '3'])

    def test_move_children(self):
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        question = createContentInContainer(survey, 'euphorie.profilequestion')
        question.invokeFactory('euphorie.risk', '3')
        question.invokeFactory('euphorie.risk', '2')
        question.invokeFactory('euphorie.risk', '4')
        module = self._convert_to_module(question)
        self.assertEqual(module.keys(), ['3', '2', '4'])


class convert_optional_profiles_tests(EuphorieFunctionalTestCase):
    def _convert_optional_profiles(self, *a, **kw):
        from ..v6 import _convert_optional_profiles
        return _convert_optional_profiles(*a, **kw)

    def create_survey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        sector = createSector(self.portal)
        return addSurvey(sector, EMPTY_SURVEY)

    def test_empty_survey(self):
        import mock
        self.loginAsPortalOwner()
        survey = self.create_survey()
        with mock.patch('euphorie.deployment.upgrade.v6._convert_to_module') \
                as mock_convert:
            self._convert_optional_profiles(survey, False)
            self.assertTrue(not mock_convert.called)

    def test_keep_new_profile_question(self):
        import mock
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        createContentInContainer(survey, 'euphorie.profilequestion')
        with mock.patch('euphorie.deployment.upgrade.v6._convert_to_module') \
                as mock_convert:
            self._convert_optional_profiles(survey, False)
            self.assertTrue(not mock_convert.called)

    def test_keep_repetable_but_remove_type_flag(self):
        import mock
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        question = createContentInContainer(survey, 'euphorie.profilequestion')
        question.type = 'repetable'
        with mock.patch('euphorie.deployment.upgrade.v6._convert_to_module') \
                as mock_convert:
            self._convert_optional_profiles(survey, False)
            self.assertTrue(not mock_convert.called)
            self.assertTrue(not hasattr(question, 'type'))

    def test_convert_optional_question(self):
        import mock
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        question = createContentInContainer(survey, 'euphorie.profilequestion')
        question.type = 'optional'
        with mock.patch('euphorie.deployment.upgrade.v6._convert_to_module') \
                as mock_convert:
            self._convert_optional_profiles(survey, False)
            mock_convert.assert_called_once_with(question)

    def test_update_client_publication_date(self):
        import datetime
        from plone.dexterity.utils import createContentInContainer
        self.loginAsPortalOwner()
        survey = self.create_survey()
        survey.published = ('version-id', u'Version title', 'old date')
        question = createContentInContainer(survey, 'euphorie.profilequestion')
        question.type = 'optional'
        self._convert_optional_profiles(survey, True)
        self.assertEqual(survey.published[0], 'version-id')
        self.assertEqual(survey.published[1], u'Version title')
        self.assertTrue(isinstance(survey.published[2], datetime.datetime))


class add_skip_evaluation_to_model_tests(DatabaseTests):
    create_tables = False

    def add_skip_evaluation_to_model(self):
        from euphorie.deployment.upgrade.v6 import add_skip_evaluation_to_model
        add_skip_evaluation_to_model(None)

    def test_column_present(self):
        import mock
        from z3c.saconfig import Session
        session = Session()
        session.execute('CREATE TABLE risk (skip_evaluation TEXT)')
        session.execute = mock.Mock()
        self.add_skip_evaluation_to_model()
        self.assertTrue(not session.execute.called)

    def test_column_not_present(self):
        import mock
        from z3c.saconfig import Session
        session = Session()
        session.execute('CREATE TABLE risk (foo INT)')
        session.execute = mock.Mock()
        self.add_skip_evaluation_to_model()
        self.assertTrue(session.execute.called)
