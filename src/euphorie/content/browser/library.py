from Acquisition import aq_base
from Acquisition import aq_inner
from euphorie.content import MessageFactory as _
from euphorie.content.behaviour.uniqueid import get_next_id
from euphorie.content.behaviour.uniqueid import INameFromUniqueId
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.module import item_depth
from euphorie.content.risk import IRisk
from euphorie.content.sector import ISector
from euphorie.content.survey import ISurvey
from euphorie.content.surveygroup import ISurveyGroup
from OFS.CopySupport import CopyError
from OFS.event import ObjectClonedEvent
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plonetheme.nuplone.utils import getPortal
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zExceptions import NotFound
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectCopiedEvent

import collections
import logging


log = logging.getLogger(__name__)


def is_allowed(context, item):
    """:returns: True if the item can be pasted into the context
    :rtype: bool
    """
    try:
        context._verifyObjectPaste(item)
    except ValueError:
        return False
    except CopyError:
        return False
    return True


def get_library(context):
    """Get a list of sectors, based on the the euphorie.library registry
    record.

    :returns: A list of dicts with details for sectors
    :rtype: list
    """
    record = api.portal.get_registry_record("euphorie.library", default="")
    if not record:
        return []
    paths = [path.lstrip("/") for path in record.split()]
    if not paths:
        return []
    site = getPortal(context)
    library = []
    for path in paths:
        try:
            sector = site.restrictedTraverse(path)
        except (AttributeError, KeyError):
            log.warning("Invalid library path (not found): %s" % path)
            continue
        if not ISector.providedBy(sector):
            log.warning("Invalid library path (not a sector): %s", path)
            continue
        sector_library = []
        survey_groups = [
            sg
            for sg in sector.values()
            if ISurveyGroup.providedBy(sg) and not sg.obsolete
        ]
        for sg in survey_groups:
            surveys = [s for s in sg.values() if ISurvey.providedBy(s)]
            if len(surveys) != 1:
                log.warning(
                    "Ignoring surveygroup due to multiple versions: %s",
                    "/".join(sg.getPhysicalPath()),
                )
                continue
            tree = build_survey_tree(aq_inner(context), surveys[0])
            tree["title"] = sg.title
            sector_library.append(tree)
        if sector_library:
            sector_library.sort(key=lambda s: s["title"])
            library.append(
                {
                    "title": sector.title,
                    "url": sector.absolute_url(),
                    "path": "/".join(sector.getPhysicalPath()),
                    "surveys": sector_library,
                }
            )
    library.sort(key=lambda s: s["title"])
    return library


def build_survey_tree(context, root):
    """Build a simple datastructure describing (part of) a survey.

    This implementation does a walk over the content itself. It is possible
    to also do this based on a catalog query, but since we use light-weight
    content items this should be simpler and removes the need to turn a
    catalog result back into a tree.

    :rtype: dict
    """
    normalize = getUtility(IIDNormalizer).normalize
    tree = {
        "title": root.title,
        "path": "/".join(root.getPhysicalPath()),
        "portal_type": normalize(root.portal_type),
        "children": [],
        "url": root.absolute_url(),
    }
    todo = collections.deque([(root, [], tree["children"])])
    while todo:
        (node, index, child_list) = todo.popleft()
        for ix, child in enumerate(node.values(), 1):
            if not (IQuestionContainer.providedBy(child) or IRisk.providedBy(child)):
                continue
            child_index = index + [str(ix)]
            info = {
                "title": child.title,
                "children": [],
                "number": ".".join(child_index),
                "path": "/".join(child.getPhysicalPath()),
                "url": child.absolute_url(),
                "disabled": not is_allowed(context, child),
                "portal_type": normalize(child.portal_type),
            }
            child_list.append(info)
            todo.append((child, child_index, info["children"]))
    return tree


def assign_ids(context, tree):
    uid_handler = getToolByName(context, "portal_uidhandler")
    todo = collections.deque([(None, tree)])
    while todo:
        (parent, item) = todo.popleft()
        uid_handler.register(item)
        if INameFromUniqueId.providedBy(item):
            if parent is not None:
                contents = parent.ZopeFind(parent, search_sub=1)
                ids = [int(child[1].id) for child in contents]
            else:
                ids = None
            old_id = item.id
            new_id = get_next_id(context, ids)
            item._setId(new_id)
            if parent is not None:
                # We need to reset the child in its folder to make sure
                # the folder knows of the new id.
                position = parent.getObjectPosition(old_id)
                del parent[old_id]
                parent._setObject(new_id, item, suppress_events=True)
                parent.moveObjectToPosition(new_id, position, True)
        if IDexterityContainer.providedBy(item):
            for gc in item.values():
                todo.append((item, aq_base(gc)))


class Library(BrowserView):
    def __call__(self):
        """Set view attributes to define the current library, depth and
        at_root, which is True when the context is the root of the library."""
        self.library = get_library(self.context)
        if not self.library:
            raise NotFound(self, "library", self.request)
        self.depth = item_depth(aq_inner(self.context))
        self.at_root = not self.depth
        return super().__call__()


class LibraryInsert(BrowserView):
    """Copy an item from the Library to the current context.

    View name: @@library-insert
    """

    def __call__(self):
        if self.request.method != "POST":
            raise NotFound(self, "library-insert", self.request)
        path = self.request.form.get("path")
        if not path:
            raise NotFound(
                self, "library-insert", self.request
            )  # XXX Wrong exception type
        target = aq_inner(self.context)
        app = target.getPhysicalRoot()
        source = app.restrictedTraverse(path)
        if not is_allowed(target, source):
            raise NotFound(
                self, "library-insert", self.request
            )  # XXX Wrong exception type
        copy = source._getCopy(target)
        assign_ids(target, copy)
        notify(ObjectCopiedEvent(copy, source))
        target._setObject(copy.id, copy)
        copy = target[copy.id]
        copy._postCopy(target, op=0)
        notify(ObjectClonedEvent(copy))

        api.portal.show_message(
            _(
                'Added a copy of "${title}" to your OiRA tool.',
                mapping={"title": copy.title},
            ),
            request=self.request,
            type="success",
        )
        self.request.RESPONSE.redirect(copy.absolute_url())
