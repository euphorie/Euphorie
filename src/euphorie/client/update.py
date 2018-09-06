from euphorie.client import model
from euphorie.client.session import SessionManager
from euphorie.client.utils import HasText
from euphorie.content.interfaces import IQuestionContainer
from five import grok
from z3c.saconfig import Session

import collections


grok.templatedir("templates")


def getSurveyTree(survey):
    """Return a list of all modules, profile questions and risks in
    a survey. Each entry is represented by a dict with a `zodb_path`
    and `type` key.
    """
    # XXX Can this be cached on the survey instance?
    nodes = []
    base_length = len(survey.getPhysicalPath())
    queue = collections.deque(survey.values())
    while queue:
        node = queue.popleft()
        if node.portal_type not in \
                ['euphorie.profilequestion', 'euphorie.module',
                 'euphorie.risk']:
            continue
        # Note that in profile.AddToTree, we pretend that an optional module
        # always has a description. This logic needs to be replicated here.
        if node.portal_type == 'euphorie.module':
            has_description = HasText(node.description) or node.optional
        else:
            has_description = HasText(node.description)
        nodes.append({
            'zodb_path': '/'.join(node.getPhysicalPath()[base_length:]),
            'type': node.portal_type[9:],
            'has_description': has_description,
            'always_present': node.portal_type[9:] == "risk" and node.risk_always_present or False,
            'optional': node.optional, })
        if IQuestionContainer.providedBy(node):
            queue.extend(node.values())
    return nodes


class Node(object):
    """Utility class to store information for a survey tree node. This is a
    subset of the data in :py:class:`euphorie.client.model.SurveyTreeItem` and
    is hashable so it can be stored in a `set`.
    """
    def __init__(self, item):
        self.zodb_path = item.zodb_path
        self.path = item.path
        self.type = item.type
        self.skip_children = item.skip_children
        self.has_description = item.has_description
        self.identification = item.type == 'risk' and item.identification or None

    def __repr__(self):
        return "<Node zodb_path=%s type=%s path=%s>" % \
                (self.zodb_path, self.type, self.path)

    def __hash__(self):
        return hash(self.path)


def getSessionTree(session):
    """Build and return a list of all survey tree nodes (as :obj:`Node`
    instances) for the current session."""
    sqlsession = Session()
    query = sqlsession.query(model.SurveyTreeItem)\
            .filter(model.SurveyTreeItem.session_id == session.id)\
            .order_by(model.SurveyTreeItem.path)
    return [Node(item) for item in query]


def treeChanges(session, survey):
    """Determine a list of changes in a survey for an existing session. The
    list of changes is returned as a list of tuples listing the ZODB path,
    the object type (one of `profile`, `module` or `risk`) and the change type
    (one of `add`, `remove` or 'modified').
    """
    surveytree = getSurveyTree(survey)
    sestree = set(getSessionTree(session))
    results = set()
    for entry in surveytree:
        nodes = [node for node in sestree
                 if node.zodb_path == entry['zodb_path']]
        if nodes:
            for node in nodes:
                sestree.remove(node)

            if nodes[0].type == entry['type'] == 'module':
                if entry['optional'] == False and \
                        nodes[0].skip_children == True:
                    # skip_children cannot be True if the module is not
                    # optional, so this is requires a SessionTree update
                    results.add(
                            (entry["zodb_path"], nodes[0].type, "modified"))
                elif entry['has_description'] != nodes[0].has_description:
                    # Log module description changes since this changes
                    # client behaviour: modules without description are
                    # skipped.
                    results.add(
                            (entry["zodb_path"], nodes[0].type, "modified"))
            if node.type == entry['type'] == 'risk':
                if entry['always_present'] and node.identification != u'no':
                    results.add(
                        (entry["zodb_path"], node.type, "modified"))
            if nodes[0].type == entry["type"] or \
                    (nodes[0].type == "module" and
                     entry["type"] == "profilequestion"):
                continue
            # Flag a type change as remove & add
            results.add((entry["zodb_path"], nodes[0].type, "remove"))
            results.add((entry["zodb_path"], entry["type"], "add"))
        else:
            results.add((entry["zodb_path"], entry["type"], "add"))

    for node in sestree:
        if node.zodb_path.find('custom-risks') != -1:
            continue
        results.add((node.zodb_path, node.type, "remove"))

    return results


def wasSurveyUpdated(session, survey):
    """Check if a survey was updated (ie republished) after the last
    modification in a session. If the survey was updated but no changes
    were made in its structure, for example if there were only textual
    changes, this method updates the timestap on the survey session
    and pretends there was no update.
    """
    # BBB: Old surveys had no published timestamp. Can be removed post
    # site launch.
    published = getattr(survey, "published", None)
    if published is not None:
        if isinstance(published, tuple):
            timestamp = published[2]
        else:
            # BBB: Euphorie 1.x did not use a tuple to store extra information.
            timestamp = published
        if session.modified >= timestamp:
            return False

    changes = treeChanges(session, survey)
    if not changes:
        session.touch()
        return False

    return True


def redirectOnSurveyUpdate(request):
    """Utility method for views to check if a survey has been updated,
    and if so redirect the user to the update confirmation page is
    generated. The return value is `True` if an update is required and
    `False` otherwise."""
    survey = request.survey
    dbsession = SessionManager.session
    if not wasSurveyUpdated(dbsession, survey):
        return False

    request.response.redirect("%s/update?initial_view=1" % survey.absolute_url())
    return True
