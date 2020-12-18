# coding=utf-8
"""
Country
-------

The main view after login, to list existing sessions, start new sessions,
delete & rename sessions

URL: https://client-oiranew.syslab.com/eu
"""

from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from zope.interface import implementer

import logging

log = logging.getLogger(__name__)


class IClientCountry(form.Schema, IBasic):
    """Country grouping in the online client.
    """


@implementer(IClientCountry)
class ClientCountry(dexterity.Container):

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
        "pt": "pt",
        "si": "sl",
    }

    @property
    def language(self):
        return self.language_mapping_by_country.get(self.id)
