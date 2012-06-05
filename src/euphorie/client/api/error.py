from zExceptions import NotFound
from five import grok
from euphorie.client.api import JsonView


class GenericError(JsonView):
    grok.context(Exception)
    grok.name('index.html')

    def render(self):
        return {'type': 'error',
                'message': 'An unknown error occurred.'}


class NotFoundView(JsonView):
    grok.context(NotFound)
    grok.name('index.html')

    def do_GET(self):
        return {'type': 'error',
                'message': 'Unknown resource requested'}
