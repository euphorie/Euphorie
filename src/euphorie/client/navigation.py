"""
Navigation
----------

Assemble data for a navigation tree.
"""

from Acquisition import aq_parent
from sqlalchemy import sql
from z3c.saconfig import Session
from euphorie.client.session import SessionManager
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.model import SurveySession
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.interfaces import ICustomRisksModule


def QuestionURL(survey, question, phase):
    return "%s/%s/%s" % (survey.absolute_url(), phase,
                         "/".join(question.short_path))


def FindFirstQuestion(dbsession=None, filter=None):
    if dbsession is None:
        dbsession = SessionManager.session
    query = Session.query(model.SurveyTreeItem)\
            .filter(model.SurveyTreeItem.session == dbsession)\
            .filter(sql.not_(model.SKIPPED_PARENTS))
    if filter is not None:
        query = query.filter(filter)
    return query.order_by(model.SurveyTreeItem.path).first()


def FindNextQuestion(after, dbsession=None, filter=None):
    if dbsession is None:
        dbsession = SessionManager.session

    query = Session.query(model.SurveyTreeItem)\
            .filter(model.SurveyTreeItem.session == dbsession)\
            .filter(model.SurveyTreeItem.path > after.path)\
            .filter(sql.not_(model.SKIPPED_PARENTS))
    # Skip modules without a description.
    if filter is None:
        filter = model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER
    else:
        filter = sql.and_(model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER, filter)
    query = query.filter(filter)
    return query.order_by(model.SurveyTreeItem.path).first()


def FindPreviousQuestion(after, dbsession=None, filter=None):
    if dbsession is None:
        dbsession = SessionManager.session

    query = Session.query(model.SurveyTreeItem)\
            .filter(model.SurveyTreeItem.session == dbsession)\
            .filter(model.SurveyTreeItem.path < after.path)\
            .filter(sql.not_(model.SKIPPED_PARENTS))
    # Skip modules without a description.
    if filter is None:
        filter = model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER
    else:
        filter = sql.and_(model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER, filter)
    query = query.filter(filter)
    return query.order_by(model.SurveyTreeItem.path.desc()).first()


def first(func, iter):
    """Find the first item in an iterable for which func(item) is True.
    If not item is find None is returned."""

    for i in iter:
        if func(i):
            return i
    else:
        return None


def getTreeData(request, context, phase="identification", filter=None):
    """Assemble data for a navigation tree

    This function returns a nested dictionary structure reflecting the
    elements for a navigation tree. The tree will all sibling questions of
    the current context, the current module and all its module siblings, its
    parents up to the root module, and all modules at the root level.

    Optionally a SQLAlchemy clause can be provided, which will be used to
    filter items shown in the tree. The current item and its parents will
    always be shown.

    Each element is reflect as a dictionary item with the following keys:

    - id: the SQL object id
    - type: the SQL object type
    - number: a human presentable numbering of the item
    - title: the object title
    - current: boolean indicating if this is the current context or its
      direct parent module
    - active: boolean indicating if this is a parent node of the current
      context
    - class: CSS classes to use for this node
    - children: a list of child nodes (in the right order)
    - url: URL for this item
    """
    query = Session.query(model.SurveyTreeItem)
    title_custom_risks = utils.get_translated_custom_risks_title(request)
    root = context
    parents = []
    while root.parent_id is not None:
        parent = query.get(root.parent_id)
        parents.append(parent)
        root = parent
    parents.reverse()

    base_url = "%s/%s/" % (request.survey.absolute_url(), phase)

    def morph(obj):
        info = {'id': obj.id,
                'number': obj.number,
                'title': obj.title,
                'active': obj.path != context.path and
                                context.path.startswith(obj.path),
                'current': (obj.path == context.path),
                'current_parent': (obj.path == context.path[:-3]),
                'path': context.path,
                'children': [],
                'type': obj.type,
                'leaf_module': False,
                'depth': obj.depth,
                'url': base_url + "/".join(obj.short_path)
                }
        cls = []
        for key in ["active", "current", "current_parent"]:
            if info[key]:
                cls.append(key)

        if obj.postponed:
            cls.append("postponed")
        else:
            if isinstance(obj, model.Risk):
                if obj.identification:
                    cls.append("answered")
                if obj.identification == "no":
                    cls.append("risk")
        info["class"] = cls and " ".join(cls) or None
        return info

    # Result is always pointing to the level *above* the current level.
    # At the end it will be the virtual tree root
    result = {'children': [],
              'leaf_module': False,
              'current': False,
              'id': None,
              'title': None}
    result["class"] = None
    children = []
    for obj in context.siblings(filter=filter):
        info = morph(obj)
        if obj.type != 'risk' and obj.zodb_path.find('custom-risks') > -1:
            info['title'] = title_custom_risks
        children.append(info)
    result["children"] = children

    if isinstance(context, model.Module):
        if not context.skip_children:
            # For modules which do not skip children, include the list of
            # children.
            me = first(lambda x: x["current"], result["children"])
            children = []
            for obj in context.children(filter=filter):
                info = morph(obj)
                # XXX: The check for SurveySession is due to Euphorie tests which don't
                # have a proper canonical ZODB survey object and don't test the
                # following OiRA-specific code.
                if obj.depth == 2 \
                        and not getattr(obj, 'is_custom_risk', False) \
                        and not isinstance(request.survey, SurveySession):
                    module = request.survey.restrictedTraverse(obj.zodb_path.split('/'))
                    if IProfileQuestion.providedBy(module) and \
                            not ICustomRisksModule.providedBy(aq_parent(module)):
                        info['type'] = u'location'
                        info['children'] = [
                            morph(sub) for sub in obj.children(filter=filter)]
                children.append(info)
            me["children"] = children
            types = set([c["type"] for c in me["children"]])
            me["leaf_module"] = "risk" in types

    elif isinstance(context, model.Risk):
        # For a risk we also want to include all siblings of its module parent
        parent = parents.pop()
        siblings = []
        for obj in parent.siblings(model.Module, filter=filter):
            info = morph(obj)
            if obj.zodb_path.find('custom-risks') > -1:
                info['title'] = title_custom_risks
            siblings.append(info)
        myparent = first(lambda x: x["active"], siblings)
        myparent["children"] = result["children"]
        myparent["leaf_module"] = True
        result["children"] = siblings

    if parents:
        # Add all parents up to the root
        while len(parents) > 1:
            parent = parents.pop()
            new = morph(parent)
            if isinstance(parent, model.Module) and parent.depth == 2:
                module = request.survey.restrictedTraverse(parent.zodb_path.split('/'))
                if IProfileQuestion.providedBy(module) and \
                        not ICustomRisksModule.providedBy(aq_parent(module)):
                    new['type'] = u'location'
            new["children"] = result["children"]
            result["children"] = [new]

        # Finally list all modules at the root level
        parent = parents.pop()
        roots = []
        for obj in parent.siblings(model.Module, filter=filter):
            info = morph(obj)
            if obj.zodb_path.find('custom-risks') > -1:
                info['title'] = title_custom_risks
            roots.append(info)

        myroot = first(lambda x: x["active"], roots)
        myroot["children"] = result["children"]
        result["children"] = roots

    return result
