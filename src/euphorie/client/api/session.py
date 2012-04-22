from five import grok
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView


class View(JsonView):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('index_html')

    def GET(self):
        return {'id': self.context.id,
                'type': 'session',
                'modified': self.context.modified.isoformat(),
                'title': self.context.title,
               }
