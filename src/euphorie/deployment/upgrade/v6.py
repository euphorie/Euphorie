import collections
import logging
import transaction
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from euphorie.content.profilequestion import ProfileQuestion

log = logging.getLogger(__name__)


def _convert_to_module(catalog, question):
    pass


def _convert_optional_profiles(root, update_catalog):
    catalog = getToolByName(root, 'portal_catalog')
    todo = collections.deque([root])
    transaction_size = 0
    while todo:
        entry = todo.popleft()
        if isinstance(entry, ProfileQuestion):
            type = getattr(entry, 'type', None)
            if type is not None:
                del entry.type
            if type == 'optional' and _convert_to_module(catalog, entry):
                transaction_size += 1
                if transaction_size == 500:
                    transaction.get().commit()
        todo.extend(entry.values())


def convert_optional_profiles(context):
    site = aq_parent(aq_inner(context))
    _convert_optional_profiles(site['sectors'], True)
    _convert_optional_profiles(site['client'], False)
