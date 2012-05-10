import unittest
from zope.interface import Interface
from zope.schema import Choice
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm


class DummySchema(Interface):
    field = Choice(vocabulary=SimpleVocabulary([
        SimpleTerm(u'foo', title=u'Bar')]))


class get_json_token_tests(unittest.TestCase):
    def get_json_token(self, *a, **kw):
        from euphorie.client.api import get_json_token
        return get_json_token(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_token, {}, 'field', None, required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_token({}, 'field', None, required=False,
                    default='default'),
                'default')

    def test_bad_value(self):
        self.assertRaises(ValueError,
                self.get_json_token, {'field': 'oops'}, 'field',
                DummySchema['field'])

    def test_correct_value(self):
        self.assertEqual(
                self.get_json_token({'field': u'foo'}, 'field',
                    DummySchema['field']),
                u'foo')


class get_json_string_tests(unittest.TestCase):
    def get_json_string(self, *a, **kw):
        from euphorie.client.api import get_json_string
        return get_json_string(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_string, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_string({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_string, {'field': False}, 'field',
                DummySchema['field'])

    def test_proper_value(self):
        self.assertEqual(
                self.get_json_string({'field': 'value'}, 'field'),
                'value')

    def test_trim_length(self):
        self.assertEqual(
                self.get_json_string({'field': 'value'}, 'field', length=2),
                'va')


class get_json_bool_tests(unittest.TestCase):
    def get_json_bool(self, *a, **kw):
        from euphorie.client.api import get_json_bool
        return get_json_bool(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_bool, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_bool({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_bool, {'field': 'dummy'}, 'field',
                DummySchema['field'])

    def test_proper_value(self):
        self.assertEqual(self.get_json_bool({'field': True}, 'field'), True)
