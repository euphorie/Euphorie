import Acquisition
import OFS.Traversable


class PathGhost(OFS.Traversable.Traversable, Acquisition.Implicit):
    """Dummy object to fake a traversable element.

    This object is inserted into the acquisition chain by
    :py:class:`SurveyPublishTraverser` when it needs to add components
    to the acquisition chain when no corresponding object in the
    ZODB or SQL databsae exists.
    """

    def __init__(self, id, request=None):
        self.id = id
        self.request = request

    def getId(self):
        return self.id
