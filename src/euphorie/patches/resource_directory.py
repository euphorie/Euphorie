from logging import getLogger
from Products.Five.browser.resource import DirectoryResource

logger = getLogger(__name__)


def patch_resource_directory():
    """Patch the DirectoryResource to not interpret .html files as page templates.

    The DirectoryResource object returned by the ++resource++ namespace traversal
    has a resource_factories dict that maps
    which file extensions should be interpreted as page templates.
    Help pages coming from proto are not page templates,
    but contain code snippet that might break chameleon, so we clear that dict.
    """
    logger.info("PATCH:Patching DirectoryResource for html files")
    DirectoryResource.resource_factories.pop("html", None)
