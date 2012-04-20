from zExceptions import NotFound
import json
from five import grok
from euphorie.client.api.interfaces import IClientAPISkinLayer


class GenericError(grok.View):
    grok.context(Exception)
    grok.layer(IClientAPISkinLayer)
    grok.name('index.html')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps({'type': 'error',
                           'message': 'An unknown error occurred.'})

class NotFoundView(grok.View):
    grok.context(NotFound)
    grok.layer(IClientAPISkinLayer)
    grok.name('index.html')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps({'type': 'error',
                           'message': 'Unknown resource requested'})



