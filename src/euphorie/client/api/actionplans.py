from five import grok
from sqlalchemy.orm import object_session
from euphorie.client.survey import PathGhost
from euphorie.client.api import JsonView
from euphorie.client.model import ActionPlan



class RiskActionPlans(PathGhost):
    """Virtual container for all action plans for a risk data."""

    def __init__(self, id, request, risk):
        super(RiskActionPlans, self).__init__(id, request)
        self.risk = risk

    def __getitem__(self, key):
        try:
            plan_id = int(key)
        except ValueError:
            raise KeyError(key)

        session = object_session(self.risk)
        plan = session.query(ActionPlan)\
                .filter(ActionPlan.risk == self.risk)\
                .filter(ActionPlan.id == plan_id)\
                .first()
        if plan is None:
            raise KeyError(key)
        return plan.__of__(self)


class View(JsonView):
    grok.context(RiskActionPlans)
    grok.require('zope2.View')
    grok.name('index_html')

    def plans(self):
        return [{'id': plan.id,
                 'plan': plan.action_plan,
                 'prevention': plan.prevention_plan,
                 'requirements': plan.requirements,
                 'responsible': plan.responsible,
                 'budget': plan.budget,
                 'planning-start': plan.planning_start.isoformat() \
                         if plan.planning_start else None,
                 'planning-end': plan.planning_end.isoformat() \
                         if plan.planning_end else None,
                 'reference': plan.reference}
                for plan in self.context.risk.action_plans]

    def do_GET(self):
        return {'action-plans': self.plans()}
