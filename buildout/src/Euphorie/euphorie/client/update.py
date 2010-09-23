import logging
from five import grok
from z3c.saconfig import Session
from euphorie.client import model
from euphorie.content.survey import ISurvey
from euphorie.client.interfaces import IClientSkinLayer
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from euphorie.client.session import SessionManager

log=logging.getLogger(__name__)

grok.templatedir("templates")


def getSurveyTree(survey):
    """Return a list of all modules, profile questions and risks in
    a survey. Each entry is represented by a dict with a `zodb_path`
    and `type` key.
    """
    ct=getToolByName(survey, "portal_catalog")
    base_path="/".join(aq_inner(survey).getPhysicalPath())
    nodes=ct(path=base_path,
             portal_type=["euphorie.profilequestion",
                          "euphorie.module", "euphorie.risk"])
    return [dict(zodb_path=brain.getPath()[len(base_path)+1:],
                 type=brain.portal_type[9:])
            for brain in nodes]


class Node(object):
    """Utility class to store information for a survey tree node. This is a
    subset of the data in :obj:`SurveyTreeItem` and is hashable so it can be
    stored in a `set`.
    """
    def __init__(self, item):
        self.zodb_path=item.zodb_path
        self.path=item.path
        self.type=item.type
    def __repr__(self):
        return "<Node zodb_path=%s type=%s path=%s>" % (self.zodb_path, self.type, self.path)
    def __hash__(self):
        return hash(self.path)



def getSessionTree(session):
    """Build and return a list of all survey tree nodes (as :obj:`Node`
    instances) for the current session."""

    sqlsession=Session()
    query=sqlsession.query(model.SurveyTreeItem)\
            .filter(model.SurveyTreeItem.session_id==session.id)\
            .order_by(model.SurveyTreeItem.path)

    return [Node(item) for item in query]



def treeChanges(session, survey):
    """Determine a list of changes in a survey for an existing session. The
    list of changes is returned as a list of tuples listing the ZODB path,
    the object type (one of `profile`, `module` or `risk`) and the change type
    (one of `add` or `remove`).
    """
    surveytree=getSurveyTree(survey)
    sestree=set(getSessionTree(session))
    results=set()
    for entry in surveytree:
        nodes=filter(lambda x: x.zodb_path==entry["zodb_path"], sestree)
        if nodes:
            for node in nodes:
                sestree.remove(node)
            if nodes[0].type==entry["type"] or (nodes[0].type=="module" and entry["type"]=="profilequestion"):
                continue
            results.add((entry["zodb_path"], nodes[0].type, "remove"))
            results.add((entry["zodb_path"], entry["type"], "add"))
        else:
            results.add((entry["zodb_path"], entry["type"], "add"))

    for node in sestree:
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
    published=getattr(survey, "published", None)
    if published is not None and session.modified>=survey.published:
        return False

    changes=treeChanges(session, survey)
    if not changes:
        session.touch()
        return False

    return True


def redirectOnSurveyUpdate(request):
    """Utility method for views to check if a survey has been updated,
    and if so redirect the user to the update confirmation page is
    generated. The return value is `True` if an update is required and
    `False` otherwise."""
    survey=request.survey
    dbsession=SessionManager.session
    if not wasSurveyUpdated(dbsession, survey):
        return False

    request.response.redirect("%s/update" % survey.absolute_url())
    return True



class Update(grok.View):
    """Update a survey session after a survey has been republished. If a
    the survey has a profile the user is asked to confirm the current
    profile before continueing.

    The implementation does not update the current session: instead it
    creates a new session, copies all relevant data from the old session
    over and then deletes the old session.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("updated")

    def extractProfile(self):
        """Determine the profile question answers for the current survey.
        """
        query=Session.query(model.Module)\
                .filter(model.Module.session_id==SessionManager.id)
        profile=[dict(id=child.id,
                     title=child.title,
                     type=child.type)
                 for child in self.context.ProfileQuestions()]
        for question in profile:
            nodes=query.filter(model.Module.zodb_path==question["id"]).all()
            if question["type"]=="optional":
                question["value"]=bool(nodes)
            else:
                question["value"]=[node.title for node in nodes]

        return profile


    def update(self):
        from euphorie.client.survey import BuildSurveyTree

        if self.request.environ["REQUEST_METHOD"]=="POST":
            profile=self.request.form
            for (id, answer) in profile.items():
                if isinstance(answer, list):
                    profile[id]=filter(None, (a.strip() for a in answer))

            survey=self.request.survey
            old_session=SessionManager.session
            new_session=SessionManager.start(old_session.title, survey)
            BuildSurveyTree(survey, profile, new_session)
            new_session.copySessionData(old_session)
            self.request.response.redirect("%s/resume" % survey.absolute_url())
            Session.delete(old_session)
            return

        self.profile=self.extractProfile()

