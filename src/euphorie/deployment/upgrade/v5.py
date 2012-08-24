import logging
import transaction
from Products.CMFCore.utils import getToolByName

log = logging.getLogger(__name__)

def reindex_solution_titles(context):
    catalog = getToolByName(context, 'portal_catalog')
    ps = catalog(title='Hello World', portal_type='euphorie.solution')
    for p in ps:
        obj = p.getObject()
        obj.reindexObject('Title')
        transaction.commit()
