"""
Navigation
----------

Assemble data for a navigation tree.
"""

from Acquisition import aq_parent
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.model import SurveySession
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion
from plone import api
from Products.Five import BrowserView
from sqlalchemy import sql
from z3c.saconfig import Session


def FindFirstQuestion(dbsession, filter=None):
    query = (
        Session.query(model.SurveyTreeItem)
        .filter(model.SurveyTreeItem.session == dbsession)
        .filter(sql.not_(model.SKIPPED_PARENTS))
    )
    if filter is not None:
        query = query.filter(filter)
    return query.order_by(model.SurveyTreeItem.path).first()


def FindNextQuestion(after, dbsession, filter=None):
    query = (
        Session.query(model.SurveyTreeItem)
        .filter(model.SurveyTreeItem.session == dbsession)
        .filter(model.SurveyTreeItem.path > after.path)
        .filter(sql.not_(model.SKIPPED_PARENTS))
    )
    # Skip modules without a description.
    if filter is None:
        filter = model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER
    else:
        filter = sql.and_(model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER, filter)
    query = query.filter(filter)
    return query.order_by(model.SurveyTreeItem.path).first()


def FindPreviousQuestion(after, dbsession, filter=None):
    query = (
        Session.query(model.SurveyTreeItem)
        .filter(model.SurveyTreeItem.session == dbsession)
        .filter(model.SurveyTreeItem.path < after.path)
        .filter(sql.not_(model.SKIPPED_PARENTS))
    )
    # Skip modules without a description.
    if filter is None:
        filter = model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER
    else:
        filter = sql.and_(model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER, filter)
    query = query.filter(filter)
    return query.order_by(model.SurveyTreeItem.path.desc()).first()


def first(func, iter):
    """Find the first item in an iterable for which func(item) is True.

    If not item is find None is returned.
    """

    for i in iter:
        if func(i):
            return i
    else:
        return None


class TreeDataCreator(BrowserView):
    """Browser view for creating tree data for the navigation."""

    def __call__(
        self,
        element=None,
        phase="identification",
        filter=None,
        survey=None,
        no_current=False,
    ):
        if not survey:
            # Standard, real-world case
            webhelpers = api.content.get_view("webhelpers", self.context, self.request)
            survey = webhelpers._survey
            traversed_session = webhelpers.traversed_session
        else:
            # XXX Fixme
            # Only in tests...
            # In some tests in test_navigation, the view "webhelpers" cannot be found
            # for the given context. That's why we pass in the survey item directly.
            traversed_session = survey

        # This is the tree element that we start from.  It can be the same as the
        # context that gets passed in, if it has an Acquisition chain.
        # On views that are called outside of the context of a module or risk,
        # e.g. the initial @@identification view, the tree-element that we find is not
        # in an acqusition context, so that we cannot use it for fetching the traversed
        # session via webhelpers.
        if not element:
            element = self.context

        query = Session.query(model.SurveyTreeItem)
        title_custom_risks = utils.get_translated_custom_risks_title(self.request)
        root = element
        parents = []
        while root.parent_id is not None:
            parent = query.get(root.parent_id)
            parents.append(parent)
            root = parent
        parents.reverse()

        def morph(obj):
            number = obj.number
            # The custom risks don't have a real number, but an Omega instead
            if obj.zodb_path.find("custom-risks") > -1:
                num_elems = number.split(".")
                number = ".".join(["Ω"] + num_elems[1:])
            info = {
                "id": obj.id,
                "number": number,
                "title": obj.title,
                "active": (
                    obj.path != element.path and element.path.startswith(obj.path)
                ),
                "current": (obj.path == element.path),
                "current_parent": (obj.path == element.path[:-3]),
                "path": element.path,
                "children": [],
                "type": obj.type,
                "leaf_module": False,
                "depth": obj.depth,
                "url": "{session_url}/{obj_path}/@@{phase}".format(
                    session_url=traversed_session.absolute_url(),
                    obj_path="/".join(obj.short_path),
                    phase=phase,
                ),
                "css_id": "",
            }
            cls = []
            for key in ["active", "current", "current_parent"]:
                if info[key]:
                    if key == "current" and no_current:
                        continue
                    cls.append(key)

            if obj.postponed:
                cls.append("postponed")
            else:
                if isinstance(obj, model.Risk):
                    if obj.identification or obj.scaled_answer:
                        cls.append("answered")
                    if obj.identification == "no":
                        cls.append("risk")
                    if obj.scaled_answer:
                        info["scaled_answer"] = obj.scaled_answer

            info["class"] = cls and " ".join(cls) or None
            return info

        # Result is always pointing to the level *above* the current level.
        # At the end it will be the virtual tree root
        result = {
            "children": [],
            "leaf_module": False,
            "current": False,
            "id": None,
            "title": None,
        }
        result["class"] = None
        children = []
        for obj in element.siblings(filter=filter):
            info = morph(obj)
            if obj.type != "risk" and obj.zodb_path.find("custom-risks") > -1:
                info["title"] = title_custom_risks
                info["css_id"] = "other-risks"
            children.append(info)
        result["children"] = children

        if isinstance(element, model.Module):
            # If this is an optional module, check the "postponed" flag.
            # As long as the optional question has not been answered, skip
            # showing its children.
            # Only a "Yes" answer will set skip_children to False
            module = survey.restrictedTraverse(element.zodb_path.split("/"))
            # In the custom risks module, we never skip children
            # Due to historical reasons, some custom modules might be set to
            # postponed. Here, we ignore that setting.
            if ICustomRisksModule.providedBy(module):
                element.skip_children = False
            elif getattr(module, "optional", False) and element.postponed in (
                True,
                None,
            ):
                element.skip_children = True
            if not element.skip_children:
                # For modules which do not skip children, include the list of
                # children.
                me = first(lambda x: x["current"], result["children"])
                children = []
                for obj in element.children(filter=filter):
                    info = morph(obj)
                    # XXX: The check for SurveySession is due to Euphorie tests which
                    # don't have a proper canonical ZODB survey object and don't test
                    # the following OiRA-specific code.
                    if (
                        obj.depth == 2
                        and not getattr(obj, "is_custom_risk", False)
                        and not isinstance(survey, SurveySession)
                    ):
                        module = survey.restrictedTraverse(obj.zodb_path.split("/"))
                        if IProfileQuestion.providedBy(
                            module
                        ) and not ICustomRisksModule.providedBy(aq_parent(module)):
                            info["type"] = "location"
                            info["children"] = [
                                morph(sub) for sub in obj.children(filter=filter)
                            ]
                    children.append(info)
                me["children"] = children
                types = {c["type"] for c in me["children"]}
                me["leaf_module"] = "risk" in types

        elif isinstance(element, model.Risk):
            # For a risk we also want to include all siblings of its module parent
            parent = parents.pop()
            siblings = []
            for obj in parent.siblings(model.Module, filter=filter):
                info = morph(obj)
                if obj.zodb_path.find("custom-risks") > -1:
                    info["title"] = title_custom_risks
                    info["css_id"] = "other-risks"
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
                siblings = []
                if isinstance(parent, model.Module) and parent.depth == 2:
                    module = survey.restrictedTraverse(parent.zodb_path.split("/"))
                    if IProfileQuestion.providedBy(
                        module
                    ) and not ICustomRisksModule.providedBy(aq_parent(module)):
                        new["type"] = "location"
                        # Include the siblings and the first level of the sibling trees
                        # so that they are still visible and browsable from the sidebar.
                        for sibling in parent.siblings(model.Module, filter=filter):
                            if sibling.id == new["id"]:
                                new["children"] = result["children"]
                                siblings.append(new)
                            else:
                                info = morph(sibling)
                                info["type"] = "location"
                                children = []
                                for child in sibling.children(filter=filter):
                                    child_info = morph(child)
                                    children.append(child_info)
                                info["children"] = children
                                siblings.append(info)
                if not siblings:
                    new["children"] = result["children"]
                    siblings.append(new)
                result["children"] = siblings

            # Finally list all modules at the root level
            parent = parents.pop()
            roots = []
            for obj in parent.siblings(model.Module, filter=filter):
                info = morph(obj)
                if obj.zodb_path.find("custom-risks") > -1:
                    info["title"] = title_custom_risks
                roots.append(info)

            myroot = first(lambda x: x["active"], roots)
            myroot["children"] = result["children"]
            result["children"] = roots

        return result


def getTreeData(
    request,
    context,
    element=None,
    phase="identification",
    filter=None,
    survey=None,
    no_current=False,
):
    """Assemble data for a navigation tree.

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

    We now put all logic into a class, making it more easily overridable.
    """
    try:
        tree_data_creator = api.content.get_view(
            "oira_navigation_tree", context, request
        )
    except api.exc.InvalidParameterError:
        # XXX Fixme
        # In the GetTreeDataTests in test_navigation, the view "oira_navigation_tree"
        # cannot be found.   Same is true for the "webhelpers" view, which we call in
        # the "oira_navigation_tree" view.  In fact only 8 views are found.
        # So test setup could be improved, but that has been the case for a while.
        tree_data_creator = TreeDataCreator(context, request)

    tree_data = tree_data_creator(
        element=element,
        phase=phase,
        filter=filter,
        survey=survey,
        no_current=no_current,
    )
    return tree_data
