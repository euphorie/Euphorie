"""
Appendix
--------

The @@appendix and @@about views.
"""

from euphorie.client.interfaces import IClientSkinLayer
from five import grok
from zope.interface import Interface

import logging


log = logging.getLogger(__name__)

grok.templatedir("templates")


class About(grok.View):
    """View name: @@about"""

    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("about")
    grok.template("about")
