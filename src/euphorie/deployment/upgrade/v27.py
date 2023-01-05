from datetime import date
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.content.risk import IRisk
from euphorie.content.solution import ISolution
from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from json import loads
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
from sqlalchemy import and_
from transaction import commit
from z3c.saconfig import Session
from zope.interface import alsoProvides

import logging


log = logging.getLogger(__name__)


def alembic_upgrade(context):
    alembic_upgrade_to("27")


def walk(node):
    for idx, sub_node in node.ZopeFind(node, search_sub=0):
        if ISolution.providedBy(sub_node):
            yield sub_node
        if IDexterityContainer.providedBy(sub_node):
            yield from walk(sub_node)


def unifiy_fields(walker):
    count = 0
    for solution in walker:
        count += 1
        if not getattr(solution, "action", None):
            # Only take action if the "action" field has not been set
            action = solution.action_plan.strip()
            prevention_plan = solution.prevention_plan
            prevention_plan = prevention_plan and prevention_plan.strip() or ""
            if prevention_plan:
                action = f"{action}\n{prevention_plan}"
            solution.action = action
            if count % 100 == 0:
                log.info("Handled %d items" % count)
            if count % 1000 == 0:
                log.info("Intermediate commit")
                commit()
        else:
            if count % 100 == 0:
                log.info(
                    "Skipped %d items, since they have already been handled." % count
                )
            if count % 1000 == 0:
                log.info("Intermediate commit")
                commit()
    log.info("Finished. Updated %d solutions" % count)


def unify_action_fields_in_solution(context):
    site = api.portal.get()
    section = "sectors"
    walker = walk(getattr(site, section))
    log.info(f'Iterating over section "{section}"')
    unifiy_fields(walker)


def unify_action_fields_in_solution_client(context):
    site = api.portal.get()
    section = "client"
    walker = walk(getattr(site, section))
    log.info(f'Iterating over section "{section}"')
    unifiy_fields(walker)


def get_pre_defined_measures(solutions, country):
    """Iterate over the Solution items on this risk."""
    measures = {}

    for item in solutions:
        description = item.description and item.description.strip() or ""
        prevention_plan = item.prevention_plan and item.prevention_plan.strip() or ""
        measure = description
        if country in ("it",):
            if prevention_plan:
                measure = f"{measure}: {prevention_plan}"
        measures[measure] = item.id

    return measures


def migrate_actgion_plans(context):
    # Work in chunks of 25
    max_tools = 25
    site = api.portal.get()
    client = getattr(site, "client")
    today = date.today()
    request = context.REQUEST.clone()
    alsoProvides(request, IClientSkinLayer)
    # path = "eu/maritime-transport/maritime-transport-1"
    tool_paths = Session.query(model.SurveySession.zodb_path).distinct()
    # .filter(model.SurveySession.zodb_path==path).distinct()
    tool_count = 0
    skip_count = 0
    for result in tool_paths:
        tool_path = str(result[0])
        try:
            tool = client.restrictedTraverse(tool_path)
        except KeyError:
            log.warning(f"No tool in client found for {tool_path}")
            continue
        country = tool_path.split("/")[0]
        sessions = (
            Session.query(model.SurveySession)
            .filter(
                and_(
                    model.Account.id == model.SurveySession.account_id,
                    model.Account.account_type != "guest",
                    model.SurveySession.zodb_path == tool_path,
                    model.SurveySession.migrated == None,  # noqa: E711
                )
            )
            .order_by(model.SurveySession.zodb_path)
        )
        if not sessions.count():
            skip_count += 1
            if skip_count % 5 == 0:
                log.info("Skipped the first %d, already handled" % skip_count)
            continue
        log.info(f"\n\nHandle tool {tool_path}")
        risks_by_path = {}
        solutions_by_path = {}
        measures_by_path = {}
        for session in sessions:
            log.info(f"Session {session.id}")
            risks = (
                Session.query(model.Risk)
                .filter(model.Risk.session_id == session.id)
                .order_by(model.Risk.path)
            )
            for risk in risks:
                risk_path = str(risk.zodb_path)
                is_custom = "custom" in risk_path
                if is_custom:
                    zodb_risk = None
                elif risk_path not in risks_by_path:
                    try:
                        zodb_risk = tool.restrictedTraverse(risk_path)
                    except Exception:
                        log.warning(f"Risk {risk_path} not found in tool {tool_path}")
                        continue
                    else:
                        if not IRisk.providedBy(zodb_risk):
                            zodb_risk = None
                            solutions_by_path[risk_path] = []
                            measures_by_path[risk_path] = []
                        else:
                            solutions = zodb_risk._solutions
                            solutions_by_path[risk_path] = solutions
                            measures_by_path[risk_path] = get_pre_defined_measures(
                                solutions, country
                            )
                        risks_by_path[risk_path] = zodb_risk

                else:
                    zodb_risk = risks_by_path[risk_path]

                # convert ActionPlan items that are clearly based on solutions
                # to "standard" type
                if not is_custom:
                    for ap in risk.custom_measures:
                        for solution in solutions_by_path[risk_path]:
                            if solution.action_plan == (ap.action_plan or "").strip():
                                if (
                                    getattr(solution, "prevention_plan", "") or ""
                                ).strip() == (ap.prevention_plan or "") and (
                                    getattr(solution, "requirements", "") or ""
                                ).strip() == (
                                    ap.requirements or ""
                                ):
                                    ap.plan_type = "measure_standard"
                                    ap.solution_id = solution.id
                # Convert the measures-in-place to their respective ActionPlan items
                try:
                    saved_existing_measures = (
                        risk.existing_measures and loads(risk.existing_measures) or []
                    )
                except ValueError:
                    saved_existing_measures = []
                # Backwards compat. We used to save dicts before we
                # switched to list of tuples.
                if isinstance(saved_existing_measures, dict):
                    saved_existing_measures = [
                        (k, v) for (k, v) in saved_existing_measures.items()
                    ]
                new_action_plans = []
                already_converted_measure_ids = [
                    x.solution_id for x in risk.in_place_standard_measures
                ]
                already_converted_custom_texts = [
                    x.action for x in risk.in_place_custom_measures
                ]
                if saved_existing_measures:
                    custom = []
                    while saved_existing_measures:
                        text, active = saved_existing_measures.pop()
                        if not active:
                            continue
                        if not is_custom and text in measures_by_path[risk_path]:
                            solution_id = measures_by_path[risk_path][text]
                            if solution_id not in already_converted_measure_ids:
                                new_action_plans.append(
                                    model.ActionPlan(
                                        action=text,
                                        plan_type="in_place_standard",
                                        solution_id=solution_id,
                                    )
                                )
                        else:
                            if text not in already_converted_custom_texts:
                                custom.append(text)
                    for text in custom:
                        new_action_plans.append(
                            model.ActionPlan(action=text, plan_type="in_place_custom")
                        )
                if new_action_plans:
                    risk.action_plans.extend(new_action_plans)
            session.migrated = today
        tool_count += 1
        if max_tools > 0 and tool_count >= max_tools:
            log.info("Broke off after %d tools" % tool_count)
            return
