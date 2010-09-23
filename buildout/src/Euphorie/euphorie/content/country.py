from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic


class ICountry(form.Schema, IBasic):
    """Country grouping in the online client.
    """

