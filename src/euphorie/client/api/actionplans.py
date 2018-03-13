from . import JsonView
from ..model import ActionPlan
from .actionplan import View as ActionPlanView
from .actionplan import plan_info
from euphorie.ghost import PathGhost
from five import grok
from plone.protect.interfaces import IDisableCSRFProtection
from sqlalchemy.orm import object_session
from zope.interface import alsoProvides


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
        return [plan_info(plan) for plan in self.context.risk.action_plans]

    def do_GET(self):
        return {'action-plans': self.plans()}

    def do_POST(self):
        action_plan = ActionPlan()
        view = ActionPlanView(action_plan, self.request)
        view.input = self.input
        response = view.do_PUT()
        if response['type'] != 'error':
            self.context.risk.action_plans.append(action_plan)

        alsoProvides(self.request, IDisableCSRFProtection)
        return response
