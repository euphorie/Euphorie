from five import grok
from euphorie.json import get_json_bool
from euphorie.json import get_json_unicode
from euphorie.json import get_json_token
from ..company import CompanySchema
from ..model import Company
from ..model import SurveySession
from . import JsonView


class View(JsonView):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('company')

    def update(self):
        if self.context.company is None:
            self.context.company = Company()

    def do_GET(self):
        company = self.context.company
        return {'type': 'company',
                'country': getattr(company, 'country', None),
                'employees': getattr(company, 'employees', None),
                'conductor': getattr(company, 'conductor', None),
                'referer': getattr(company, 'referer', None),
                'workers-participated':
                    getattr(company, 'workers_participated', None),
                'needs-met': getattr(company, 'needs_met', None),
                'recommend-tool': getattr(company, 'recommend_tool', None),
               }

    def do_PUT(self):
        company = self.context.company
        try:
            company.country = get_json_unicode(self.input, 'country', False,
                    company.country, length=3)
            company.employees = get_json_token(self.input, 'employees',
                    CompanySchema['employees'], False, company.employees)
            company.conductor = get_json_token(self.input, 'conductor',
                    CompanySchema['conductor'], False, company.conductor)
            company.referer = get_json_token(self.input, 'referer',
                    CompanySchema['referer'], False, company.referer)
            company.workers_participated = get_json_bool(self.input,
                    'workers-participated', False,
                    company.workers_participated)
            company.needs_met = get_json_bool(self.input,
                    'needs-met', False,
                    company.needs_met)
            company.recommend_tool = get_json_bool(self.input,
                    'recommend-tool', False,
                    company.recommend_tool)
        except (KeyError, ValueError) as e:
            return {'type': 'error',
                    'message': str(e)}
        return self.do_GET()
