import collections
import datetime
import logging
from sqlalchemy.engine.reflection import Inspector
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContent
from euphorie.content.profilequestion import ProfileQuestion
from euphorie.client import model

log = logging.getLogger(__name__)


def _convert_to_module(question):
    log.info('Converting %s to module', '/'.join(question.getPhysicalPath()))
    parent = aq_parent(question)
    question = aq_base(question)
    module = createContent('euphorie.module')
    module.id = question.id
    module.creation_date = question.creation_date
    module.modification_date = question.modification_date
    module.creators = question.creators
    if getattr(question, 'external_id', None):
        module.external_id = question.external_id
    module.title = question.title
    module.question = question.question
    module.description = question.description
    module.optional = True
    children = question.getOrdering().idsInOrder()
    for key in children:
        module._setObject(key, question[key], suppress_events=True)
    ordering = parent.getOrdering()
    position = ordering.getObjectPosition(question.id)
    parent._delOb(question.id)
    parent._setObject(question.id, module, suppress_events=True)
    ordering.moveObjectToPosition(module.id, position, suppress_events=True)
    return parent[question.id]


def _convert_optional_profiles(root, in_client):
    catalog = getToolByName(root, 'portal_catalog')
    todo = collections.deque([root])
    while todo:
        entry = todo.popleft()
        if isinstance(entry, ProfileQuestion):
            type = getattr(entry, 'type', None)
            if type is not None:
                del entry.type
            if type == 'optional':
                module = _convert_to_module(entry)
                if in_client:
                    survey = aq_parent(module)
                    published = survey.published
                    survey.published = (published[0], published[1],
                            datetime.datetime.now())
                else:
                    catalog.indexObject(module,
                            ['portal_type', 'meta_type', 'object_provides'])
            continue
        if entry.portal_type not in ['euphorie.page', 'euphorie.module',
                                     'euphorie.risk']:
            todo.extend(entry.objectValues())


def convert_optional_profiles(context):
    site = aq_parent(aq_inner(context))
    _convert_optional_profiles(site['sectors'], False)
    _convert_optional_profiles(site['client'], True)


def add_skip_evaluation_to_model(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c['name']
               for c in inspector.get_columns(model.Risk.__table__.name)]
    if 'skip_evaluation' not in columns:
        log.info('Adding skip_evaluation column for risks')
        session.execute(
            "ALTER TABLE %s ADD skip_evaluation BOOL DEFAULT 'f' NOT NULL" %
            model.Risk.__table__.name)
        datamanager.mark_changed(session)

