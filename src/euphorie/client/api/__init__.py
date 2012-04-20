import json
import martian
from zope.publisher.publish import mapply
from five import grok
from euphorie.client.api.interfaces import IClientAPISkinLayer


class JsonView(grok.View):
    """Generic base class for JSON views.

    This class does two things:

    1. it renders the result as JSON
    2. it a request has a body it will try to JSON-parse it and
       store the result as ``self.input``.

    """
    martian.baseclass()
    grok.layer(IClientAPISkinLayer)

    input = None

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        input = self.request.stdin.getvalue()
        if input:
            try:
                self.input = json.loads(input)
            except ValueError:
                return {'type': 'error',
                        'message': 'Invalid JSON input'}

        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in [302, 303]:
            return  # Shortcircuit on redirect, no need to render

        self.request.response.setHeader('Content-Type', 'application/json')
        response = mapply(self.render, (), self.request)
        return json.dumps(response)
