# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from plone import api


@implementer(IContextSourceBinder)
class RegistryValueVocabulary(object):

    def __init__(self, value_name):
        self.value_name = value_name

    def __len__(self):
        return len(self.values)

    @property
    def values(self):
        return api.portal.get_registry_record(self.value_name, default=[])

    def __call__(self, context):
        return safe_simplevocabulary_from_values(self.values)
