# -*- coding: UTF-8 -*-
from plone import api


def setCountryLanguageFR(context):
    portal = api.portal.get()
    client = portal.client
    country = client.fr
    setattr(country, 'language', 'fr')
