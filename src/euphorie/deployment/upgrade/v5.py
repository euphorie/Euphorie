import logging
import transaction
from Products.CMFCore.utils import getToolByName

log = logging.getLogger(__name__)

def reindex_solution_titles(context):
    # XXX: Make sure that all Dexterity types have UIDs before running this
    # step. There is an upgrade step for plone.app.dexterity that does this.
    catalog = getToolByName(context, 'portal_catalog')
    ps = catalog(title='Hello World', portal_type='euphorie.solution')
    for p in ps:
        obj = p.getObject()
        obj.reindexObject('Title')
        transaction.commit()
