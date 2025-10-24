from ftw.upgrade import UpgradeStep
from plone import api
from plone.app.upgrade.utils import update_catalog_metadata
from plone.uuid.handlers import addAttributeUUID
from plone.uuid.interfaces import ATTRIBUTE_NAME
from plone.uuid.interfaces import IUUID
from Products.ZCatalog.ProgressHandler import ZLogHandler
from zope.globalrequest import getRequest

import logging
import os
import transaction


logger = logging.getLogger(__name__)
# By default we do intermediate commits, to have less chance of ConflictErrors.
# Set the environment variable EUPHORIE_DISABLE_INTERMEDIATE_COMMITS=1
# to disable intermediate commits.
EUPHORIE_DISABLE_INTERMEDIATE_COMMITS = bool(
    int(os.environ.get("EUPHORIE_DISABLE_INTERMEDIATE_COMMITS", 0))
)


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

    def _commit(self, note=""):
        """Commit the current transaction with an optional note."""
        if EUPHORIE_DISABLE_INTERMEDIATE_COMMITS:
            return
        tx = transaction.get()
        if note:
            tx.note(note)
        tx.commit()
        logger.info("Committed transaction: %s", note)

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
        # Get the values once to speed up the loop below.  Without this, the
        # first full run took over an hour, gathering 220k paths to recreate.
        # Make it a set for faster 'in' checks.  This reduces the time insanely.
        index_index_values = set(index._index.values())
        logger.info("Checking _unindex items.")
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
                if len(recreate) % 10000 == 0:
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
        app = self.portal.getPhysicalRoot()
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
            new_uuid = IUUID(obj)
            logger.debug("Changed UID from %s to %s for %s", old_uuid, new_uuid, path)
            if num % 10000 == 0:
                note = f"Created fresh UID for {num}/{len(recreate)} paths so far."
                logger.info(note)
                if num % 50000 == 0:
                    self._commit(note=note)

        note = f"Created fresh UID for all {len(recreate)} paths."
        logger.info(note)
        self._commit(note=note)

        # Update catalog metadata to reflect new UIDs.
        # On the test site this took about 13 minutes.
        note = "Updating catalog metadata for UIDs."
        logger.info(note)
        logger.info("This can take a long time...")
        update_catalog_metadata(self.portal, "UID")
        self._commit(note=note)

        # Now we need to clear and reindex the UID index.
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
        note = "Reindexed UID index."
        logger.info(note)
        self._commit(note=note)

        logger.info("The UID index should be fine again. Checking...")
        if not self.is_uid_index_consistent():
            raise ValueError(
                "After all fixes and reindexing, the UID index is still inconsistent."
            )
        logger.info("Yes, the UID index is consistent. All done.")
