from euphorie import patches  # noqa: F401
from euphorie.patches.resource_directory import patch_resource_directory
from zope.i18nmessageid import MessageFactory as mf

patch_resource_directory()

MessageFactory = mf("euphorie")

__all__ = ["MessageFactory"]
