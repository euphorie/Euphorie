from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.content.survey import ISurvey
from plone import api
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder


@implementer(IContextSourceBinder)
class RegistryValueVocabulary:
    def __init__(self, value_name):
        self.value_name = value_name

    def __len__(self):
        return len(self.values)

    @property
    def values(self):
        return tuple(
            filter(None, api.portal.get_registry_record(self.value_name, default=[]))
        )

    def __call__(self, context):
        return safe_simplevocabulary_from_values(self.values)


def ChoiceConditionsVocabulary(context=None):
    query = {
        "portal_type": ["euphorie.option"],
        "sort_on": "path",
    }
    if context is not None:
        for parent in aq_chain(aq_inner(context)):
            if ISurvey.providedBy(parent):
                query["path"] = "/".join(parent.getPhysicalPath())
    return StaticCatalogVocabulary(query)
