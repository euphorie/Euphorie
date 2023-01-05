"""
Country
-------

The main view after login, to list existing sessions, start new sessions,
delete & rename sessions

URL: https://client-oiranew.syslab.com/eu
"""

from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

import logging


log = logging.getLogger(__name__)


class IClientCountry(model.Schema, IBasic):
    """Country grouping in the online client."""


@implementer(IClientCountry)
class ClientCountry(Container):
    country_type = None

    # Many countries only have one language. Use it as the default
    language_mapping_by_country = {
        "bg": "bg",
        "cy": "el",
        "de": "de",
        "eu": "en",
        "fi": "fi",
        "fr": "fr",
        "gb": "en",
        "gr": "el",
        "hr": "hr",
        "hu": "hu",
        "is": "is",
        "it": "it",
        "lt": "lt",
        "lv": "lv",
        "mt": "en",
        "pt": "pt",
        "si": "sl",
        "sk": "sk",
        "cz": "cs",
    }

    @property
    def language(self):
        return self.language_mapping_by_country.get(self.id)
