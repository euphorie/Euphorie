from zExceptions import NotFound
import json
import martian
from zope.publisher.publish import mapply
from five import grok
from euphorie.client.api.interfaces import IClientAPISkinLayer



def get_json_token(input, name, field, required=False, default=None):
    value = input.get(name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    try:
        return field.vocabulary.getTerm(value).token
    except LookupError:
        raise ValueError('Invalid value for field %s' % name)


def get_json_string(input, name, required=False, default=None, length=None):
    value = input.get(name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, basestring):
        raise ValueError('Field %s has wrong type' % name)
    if length is not None:
        value = value[:length]
    return value


def get_json_bool(input, name, required=False, default=None):
    value = input.get(name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, bool):
        raise ValueError('Field %s has wrong type' % name)
    return value


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

    def render(self):
        # Workaround for grok silliness
        pass

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
        method = self.request.get('REQUEST_METHOD', 'GET').upper()
        renderer = getattr(self, method, None)
        if renderer is None:
            raise NotFound()
        response = mapply(renderer, (), self.request)
        return json.dumps(response)
