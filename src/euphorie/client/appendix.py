"""
Appendix
--------

The @@appendix and @@about views.
"""

import logging
from zope.interface import Interface
from five import grok
from euphorie.client.interfaces import IClientSkinLayer

log = logging.getLogger(__name__)

grok.templatedir("templates")


class About(grok.View):
    """View name: @@about
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("about")
    grok.template("about")
