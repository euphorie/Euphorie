# coding=utf-8
from euphorie.decorators import reify

import unittest


class TestReify(unittest.TestCase):
    def reify(self, wrapped):
        return reify(wrapped)

    def test___get__withinst(self):
        def wrapped(inst):
            return 'a'
        decorator = self.reify(wrapped)
        inst = Dummy()
        result = decorator.__get__(inst)
        self.assertEqual(result, 'a')
        self.assertEqual(inst.__dict__['wrapped'], 'a')

    def test___get__noinst(self):
        decorator = self.reify(None)
        result = decorator.__get__(None)
        self.assertEqual(result, decorator)

    def test___doc__copied(self):
        def wrapped(inst):
            """My doc"""
        decorator = self.reify(wrapped)
        self.assertEqual(decorator.__doc__, "My doc")


class Dummy(object):
    pass
