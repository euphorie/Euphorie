import logging
import transaction
from Products.CMFCore.utils import getToolByName
from euphorie.content.behaviour.richdescription import IRichDescription

log = logging.getLogger(__name__)


def reindex_solution_titles(context):
    catalog = getToolByName(context, 'portal_catalog')
    ps = catalog(title='title_common_solution',
            portal_type='euphorie.solution')
    i = 0
    for p in ps:
        try:
            obj = p.getObject()
        except:
            continue
        obj.reindexObject('Title')
        i += 1
        if i == 100:
            transaction.commit()


def reindex_richtext_descriptions(context):
    catalog = getToolByName(context, 'portal_catalog')
    ps = catalog(object_provides=IRichDescription.__identifier__)
    i = 0
    for p in ps:
        try:
            obj = p.getObject()
        except:
            continue
        obj.reindexObject('Description')
        i += 1
        if i == 100:
            transaction.commit()
