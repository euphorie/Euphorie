"""
Survey views
------------
"""

from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.country import IClientCountry
from euphorie.client.profile import extractProfile
from euphorie.content.interfaces import ICustomRisksModule
from plone import api
from plone.memoize.instance import memoize
from plone.memoize.view import memoize_contextless
from sqlalchemy import case
from sqlalchemy import func
from sqlalchemy import orm
from sqlalchemy import sql
from z3c.saconfig import Session

import decimal
import logging


log = logging.getLogger(__name__)


class _StatusHelper:
    COUNTRIES_WITHOUT_HIGH_RISKS = ["it"]

    @property
    @memoize
    def sql_session(self):
        return Session()

    @property
    @memoize_contextless
    def preferred_language(self):
        return api.portal.get_tool("portal_languages").getPreferredLanguage()

    def module_query(self, sessionid, optional_modules):
        if optional_modules:
            case_clause = case(
                [
                    (
                        sql.and_(
                            model.SurveyTreeItem.profile_index != -1,
                            model.SurveyTreeItem.zodb_path.in_(optional_modules),
                        ),
                        func.substr(model.SurveyTreeItem.path, 1, 6),
                    ),
                    (
                        sql.and_(
                            model.SurveyTreeItem.profile_index == -1,
                            model.SurveyTreeItem.zodb_path.in_(optional_modules),
                        ),
                        func.substr(model.SurveyTreeItem.path, 1, 3) + "000-profile",
                    ),
                    (
                        sql.and_(
                            model.SurveyTreeItem.profile_index != -1,
                            model.SurveyTreeItem.depth < 2,
                        ),
                        func.substr(model.SurveyTreeItem.path, 1, 3),
                    ),
                ]
            )
        else:
            case_clause = case(
                [
                    (
                        sql.and_(
                            model.SurveyTreeItem.profile_index != -1,
                            model.SurveyTreeItem.depth < 2,
                        ),
                        func.substr(model.SurveyTreeItem.path, 1, 3),
                    )
                ]
            )

        query = (
            self.sql_session.query(case_clause.label("module"))
            .filter(
                sql.and_(
                    model.SurveyTreeItem.session_id == sessionid,
                    model.SurveyTreeItem.type == "module",
                )
            )
            .group_by("module")
            .order_by("module")
        )
        return query

    def slicePath(self, path):
        while path:
            yield path[:3].lstrip("0")
            path = path[3:]

    def getModulePaths(self):
        """Return a list of all the top-level modules belonging to this
        survey."""
        session_id = self.session.id
        if not session_id:
            return []
        profile = extractProfile(self.context.aq_parent, self.context.session)
        module_query = self.module_query(
            sessionid=session_id, optional_modules=profile.keys()
        )
        module_res = module_query.all()
        modules_and_profiles = {}
        for row in module_res:
            if row.module is not None:
                if row.module.find("profile") > 0:
                    path = row.module[:3]
                    modules_and_profiles[path] = "profile"
                else:
                    modules_and_profiles[row[0]] = ""
        module_paths = [m.module for m in module_res if m.module is not None]
        module_paths = modules_and_profiles.keys()
        module_paths = sorted(module_paths)
        self.modules_and_profiles = modules_and_profiles
        return module_paths

    def getModules(self):
        """Return a list of dicts of all the top-level modules and locations
        belonging to this survey."""
        sql_session = self.sql_session
        session_id = self.session.id
        module_paths = self.getModulePaths()
        url_schema = "%s/{0}/@@identification" % self.context.absolute_url()
        parent_node = orm.aliased(model.Module)
        titles = dict(
            sql_session.query(model.Module.path, model.Module.title)
            .filter(model.Module.session_id == session_id)
            .filter(model.Module.path.in_(module_paths))
        )

        location_titles = dict(
            sql_session.query(model.Module.path, parent_node.title)
            .filter(model.Module.session_id == session_id)
            .filter(model.Module.path.in_(module_paths))
            .filter(
                sql.and_(
                    parent_node.session_id == session_id,
                    parent_node.depth < model.Module.depth,
                    model.Module.path.like(parent_node.path + "%"),
                )
            )
        )
        modules = {}
        toc = {}
        title_custom_risks = utils.get_translated_custom_risks_title(self.request)

        for path in module_paths:
            number = ".".join(self.slicePath(path))
            # top-level module, always include it in the toc
            if len(path) == 3:
                title = titles[path]
                if (
                    title == "title_other_risks"
                    or title == "Other risks"
                    or title == "Custom risks"
                    or title == "label_custom_risks"
                ):
                    title = title_custom_risks
                toc[path] = {
                    "path": path,
                    "title": title,
                    "locations": [],
                    "number": number,
                }
                # If this is a profile (aka container for locations), skip
                # adding to the list of modules
                if self.modules_and_profiles[path] == "profile":
                    continue
            # sub-module (location) or location container
            else:
                if path in location_titles:
                    title = f"{location_titles[path]} - {titles[path]}"
                    toc[path[:3]]["locations"].append(
                        {"path": path, "title": titles[path], "number": number}
                    )
                else:
                    log.warning(
                        "Status: found a path for a submodule {} for which "
                        "there's no location title.".format(path)
                    )
                    continue

            modules[path] = {
                "path": path,
                "title": title,
                "url": url_schema.format("/".join(self.slicePath(path))),
                "todo": 0,
                "ok": 0,
                "postponed": 0,
                "risk_with_measures": 0,
                "risk_without_measures": 0,
                "number": number,
            }
        self.tocdata = toc
        return modules

    def getRisks(self, module_paths, skip_unanswered=False):
        """Return a list of risk dicts for risks that belong to the modules
        with paths as specified in module_paths."""
        global request
        request = self.request
        if not len(module_paths):
            return []
        sql_session = self.sql_session
        session_id = self.session.id
        # First, we need to compute the actual module paths, making sure that
        # skipped optional modules are excluded
        # This means top-level module paths like 001 or 001002 can be replaced
        # by several sub-modules paths like 001002, 001003 and 001002001
        path_clause = [model.SurveyTreeItem.path.like(f"{mp}%") for mp in module_paths]

        module_query = (
            sql_session.query(model.SurveyTreeItem)
            .filter(
                sql.and_(
                    model.SurveyTreeItem.session_id == session_id,
                    model.SurveyTreeItem.type == "module",
                    sql.or_(*path_clause),
                )
            )
            .order_by(model.SurveyTreeItem.path)
        )

        module_res = module_query.all()
        modules_by_path = {m.path: m for m in module_res}

        def nodes(modules):
            global use_nodes, s_paths
            use_nodes = []
            s_paths = sorted(modules, key=lambda x: x.path)
            # In case of repeatable profile questions, the top-level module
            # path will be 6 digits long.
            top_nodes = [
                elem
                for elem in s_paths
                if (
                    len(elem.path) == 3
                    or (len(elem.path) == 6 and elem.path[:3] not in s_paths)
                )
                and not elem.skip_children
            ]

            def use_node(elem):
                # Recursively find the nodes that are not disabled
                global use_nodes  # noqa: F824
                # Skip this elem?
                # If this is an optional module, check the "postponed" flag.
                # As long as the optional question has not been answered, skip
                # showing its children.
                # Only a "Yes" answer on the module will be considered as "do
                # not skip children"
                zodb_elem = self.context.aq_parent.restrictedTraverse(
                    elem.zodb_path.split("/"), None
                )
                if not zodb_elem:
                    log.error(
                        "Cannot traverse to %r from %r",
                        elem.zodb_path,
                        self.context.aq_parent,
                    )
                    return
                if getattr(zodb_elem, "optional", False):
                    if (
                        elem.postponed in (True, None) or elem.skip_children
                    ) and not ICustomRisksModule.providedBy(zodb_elem):
                        return
                children = [
                    x
                    for x in s_paths
                    if x.path.startswith(elem.path)
                    and len(x.path) == len(elem.path) + 3
                ]
                if children:
                    for child in children:
                        use_node(child)
                else:
                    use_nodes.append(elem.path)

            for elem in top_nodes:
                use_node(elem)
            ret = []
            # Here we make sure that only the longest paths of sub-modules
            # are used, but not the parents. Example
            # (001, 002, 001001, 001003) will be turned into
            # (001001, 001003, 002), since the parent 001 contains sub-modules,
            # and some of those might have been de-selected, like 001002
            for elem in sorted(use_nodes, reverse=True):
                if not [x for x in ret if x.startswith(elem)]:
                    ret.append(elem)
            return ret

        filtered_module_paths = nodes(tuple(module_res))

        child_node = orm.aliased(model.Risk)
        risks = (
            sql_session.query(model.Module, model.Risk)
            .filter(
                sql.and_(
                    model.Module.session_id == session_id,
                    model.Module.path.in_(filtered_module_paths),
                    sql.and_(
                        child_node.session_id == model.Module.session_id,
                        child_node.depth > model.Module.depth,
                        child_node.path.like(model.Module.path + "%"),
                    ),
                )
            )
            .join(
                (
                    model.Risk,
                    sql.and_(
                        model.Risk.path.startswith(model.Module.path),
                        model.Risk.session_id == session_id,
                    ),
                )
            )
            .order_by(model.Risk.path)
        )

        def _module_path(path):
            # Due to the extended query above that replaces top-module paths
            # with sub-module paths (if present), we need to cut back the path
            # under which we store each risk back to the original top-level
            # module path
            for mp in module_paths:
                if path.startswith(mp):
                    return mp

        filtered_risks = []
        for module, risk in risks.all():
            if risk.identification != "n/a":
                if (
                    skip_unanswered
                    and risk.identification is None
                    and not risk.postponed
                ):
                    continue
                module_path = _module_path(module.path)
                # And, since we might have truncated the path to represent
                # the top-level module, we also need to get the corresponding
                # module object.
                module = modules_by_path[module_path]
                filtered_risks.append((module, risk))
        return filtered_risks

    def as_decimal(self, num):
        return decimal.Decimal(num)

    @property
    @memoize
    def show_high_risks(self):
        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                if obj.id in self.COUNTRIES_WITHOUT_HIGH_RISKS:
                    return False
        return True
