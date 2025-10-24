from Acquisition import aq_parent
from ftw.upgrade import UpgradeStep
from plone import api
from plone.uuid.handlers import addAttributeUUID
from plone.uuid.interfaces import ATTRIBUTE_NAME
from plone.uuid.interfaces import IUUID
from Products.CMFCore.indexing import processQueue
from Products.ZCatalog.ProgressHandler import ZLogHandler
from zope.globalrequest import getRequest

import logging


logger = logging.getLogger(__name__)


class FixUidIndex(UpgradeStep):
    """Fix UID index inconsistencies.

    The 20251006201600_ensure_uid upgrade step ensured that all content
    has a UID assigned to it.  But that was not enough to fix all problems.
    So we need to take over some more code from this script:
    https://github.com/zestsoftware/plonescripts/blob/master/fix_uid_index.py

    That script first checks paths in actual_catalog.uids.keys(), but that did
    not surface any problems in our case, so we skip that part here.

    Then it really checks the UID index.  This has two internal BTrees
    that can get out of sync:

        1) _index: UID -> doc id
        2) _unindex: doc id -> UID

    And indeed we see problems there in a test site:

        Number of _index uid keys:      198801, unique: 198801
        Number of _index doc id values: 198801, unique: 198801
        Number of _unindex doc id keys: 419339, unique: 419339
        Number of _unindex uid values:  419339, unique: 245707

    Normally, all these numbers should all be the same.
    This is not the case for us.

    The script tries to register intids for all objects that are missing them,
    but we don't have that problem.  So we skip that part.
    """

    def is_uid_index_consistent(self):
        """Check if the UID index is consistent.

        Returns True if consistent, False if not.
        """
        catalog = api.portal.get_tool("portal_catalog")
        index = catalog.Indexes["UID"]
        _index_keys = index._index.keys()
        _index_values = index._index.values()
        _unindex_keys = index._unindex.keys()
        _unindex_values = index._unindex.values()
        logger.info(
            "Number of _index uid keys:      %d, unique: %d",
            len(_index_keys),
            len(set(_index_keys)),
        )
        logger.info(
            "Number of _index doc id values: %d, unique: %d",
            len(_index_values),
            len(set(_index_values)),
        )
        logger.info(
            "Number of _unindex doc id keys: %d, unique: %d",
            len(_unindex_keys),
            len(set(_unindex_keys)),
        )
        logger.info(
            "Number of _unindex uid values:  %d, unique: %d",
            len(_unindex_values),
            len(set(_unindex_values)),
        )

        # Both index and unindex should have the same number of entries.
        # And keys and values should be unique.
        if not (
            len(_index_keys)
            == len(set(_index_keys))
            == len(_index_values)
            == len(set(_index_values))
            == len(_unindex_keys)
            == len(set(_unindex_keys))
            == len(_unindex_values)
            == len(set(_unindex_values))
        ):
            logger.error(
                "The numbers of keys and values in the UID index are NOT consistent."
            )
            return False

        logger.info("The numbers of keys and values in the UID index are consistent.")
        # Are the matching sets the same?
        if set(_index_keys) != set(_unindex_values) or set(_index_values) != set(
            _unindex_keys
        ):
            logger.error(
                "The sets are NOT the same. Inconsistencies found in UID index."
            )
            return False
        logger.info("No inconsistencies found in UID index.")
        return True

    def __call__(self):
        """Upgrade step to fix inconsistencies in the UID index.

        I will add some inline comments about how long this took on a test
        site with about 420k items and a messed up UID index.
        """
        logger.info("Checking inconsistencies in UID index.")
        if self.is_uid_index_consistent():
            logger.info("The UID index is consistent. Nothing to do.")
            return

        # Gather paths for which we will create a new uuid.
        recreate = set()
        catalog = api.portal.get_tool("portal_catalog")
        index = catalog.Indexes["UID"]
        logger.info("Checking _unindex items.")
        # Get the values once to speed up the loop below.  Without this, the
        # first full run took over an hour, gathering 220k paths to recreate.
        index_index_values = index._index.values()
        for docid, uid in index._unindex.items():
            if docid not in index_index_values:
                path = catalog.getpath(docid)
                logger.debug(
                    "Doc id %s is missing from _index values. UID %s, path %s",
                    docid,
                    uid,
                    path,
                )
                recreate.add(path)
                if len(recreate) % 1000 == 0:
                    logger.info("Found %d paths to recreate so far.", len(recreate))

        logger.info("Done checking _unindex items.")
        if not recreate:
            logger.info("No paths need to have their UID recreated.")
            return
        if recreate:
            logger.info(
                "We will recreate %d UIDs/UUIDs that are currently duplicate.",
                len(recreate),
            )
            logger.info(
                "You might need to manually fix some links.\n"
                "We have no way of knowing if a link should use "
                "resolveuid/old_uid or resolveuid/new_uid.\n"
                "Perhaps we could query the relation catalog to see "
                "which relations an item has."
            )

        # Now recreate UIDs for the gathered paths.
        # This took about 6 minutes on the test site.
        app = aq_parent(api.portal.get())
        for num, path in enumerate(recreate, 1):
            try:
                obj = app.unrestrictedTraverse(path)
            except KeyError:
                logger.info("Ignoring unreachable path to recreate UID: %s", path)
                continue
            # obj.UID() would return the UID of the parent in case
            # obj is a Discussion Item.
            old_uuid = IUUID(obj)
            # This might find an item by acquisition.
            # migration-law/migration-law/migration-law/research.htm
            # may actually be migration-law/research.htm
            actual_path = "/".join(obj.getPhysicalPath())
            if actual_path != path:
                logger.warning(
                    "Wanted to recreate UID for path %s, but this leads to "
                    "other path %s. Ignoring.",
                    path,
                    actual_path,
                )
                continue
            delattr(obj, ATTRIBUTE_NAME)
            # Call the event handler that adds a UUID:
            addAttributeUUID(obj, None)
            # Reindex the UID index for this object and update its metadata in
            # the catalog.
            obj.reindexObject(idxs=["UID"])
            new_uuid = IUUID(obj)
            logger.debug("Changed UID from %s to %s for %s", old_uuid, new_uuid, path)
            if num % 10000 == 0:
                logger.info(
                    "Created fresh UID for %d/%d paths so far.", num, len(recreate)
                )

        logger.info("Created fresh UID for all %d paths.", len(recreate))

        # Even after the above fix, the clear and reindex is still needed.
        logger.info("Clearing UID index...")
        index.clear()
        # Reindexing took about 10 minutes on the test site.
        # So let's add a progress logger.
        logger.info("Reindexing UID index...")
        catalog._catalog.reindexIndex(
            "UID",
            getRequest(),
            pghandler=ZLogHandler(10000),
        )
        logger.info("Done reindexing UID index.")
        logger.info("Processing catalog queue. This can take a long time...")
        # This took about 22 minutes on the test site.
        processQueue()
        logger.info("Done processing catalog queue.")
        logger.info("The UID index should be fine again. Checking...")
        if not self.is_uid_index_consistent():
            raise ValueError(
                "After all fixes and reindexing, the UID index is still inconsistent."
            )
        logger.info("Yes, the UID index is consistent. All done.")
