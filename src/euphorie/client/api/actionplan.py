from five import grok
from sqlalchemy.orm import object_session
from euphorie.json import get_json_date
from euphorie.json import get_json_int
from euphorie.json import get_json_unicode
from ..model import ActionPlan
from . import JsonView


def plan_info(plan):
    return {'id': plan.id,
            'plan': plan.action_plan,
            'prevention': plan.prevention_plan,
            'requirements': plan.requirements,
            'responsible': plan.responsible,
            'budget': plan.budget,
            'planning-start': plan.planning_start.isoformat()
                    if plan.planning_start else None,
            'planning-end': plan.planning_end.isoformat()
                    if plan.planning_end else None,
            'reference': plan.reference}


class View(JsonView):
    grok.context(ActionPlan)
    grok.require('zope2.View')
    grok.name('index_html')

    def do_GET(self):
        info = plan_info(self.context)
        info['type'] = 'actionplan'
        return info

    def do_DELETE(self):
        session = object_session(self.context)
        session.delete(self.context)
        return {}

    def do_PUT(self):
        plan = self.context
        try:
            for (attr, key) in [('action_plan', 'plan'),
                                ('prevention_plan', 'prevention'),
                                ('requirements', 'requirements'),
                                ('responsible', 'responsible'),
                                ('reference', 'reference')]:
                setattr(plan, attr,
                        get_json_unicode(self.input, key, False,
                            getattr(plan, attr)))
            plan.budget = get_json_int(self.input, 'budget', False,
                    plan.budget)
            plan.planning_start = get_json_date(self.input, 'planning-start',
                    False, plan.planning_start)
            plan.planning_end = get_json_date(self.input, 'planning-end',
                    False, plan.planning_end)
        except (KeyError, ValueError) as e:
            return {'type': 'error',
                    'message': str(e)}
        return self.do_GET()
