from __future__ import absolute_import
import datetime
import logging
import json
import martian
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.component import getMultiAdapter
from zope.publisher.publish import mapply
from five import grok
from zope.i18n import translate
from .interfaces import IAPISkinLayer


log = logging.getLogger(__name__)


def vocabulary_token(field, value):
    term = field.vocabulary.by_value.get(value)
    if term is None:
        return None
    else:
        return term.token


def vocabulary_options(field, request):
    t = lambda txt: translate(txt, context=request)
    return [{'value': term.token,
             'title': t(term.title)}
            for term in field.vocabulary
            if term.token != 'none']


def _nested_get(input, name):
    value = input
    try:
        for part in name.split('.'):
            value = value[part]
    except KeyError:
        return None
    return value


def get_json_token(input, name, field, required=False, default=None):
    value = _nested_get(input, name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    try:
        return field.vocabulary.getTermByToken(value).value
    except LookupError:
        raise ValueError('Invalid value for field %s' % name)


def get_json_unicode(input, name, required=False, default=None, length=None):
    value = _nested_get(input, name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, basestring):
        raise ValueError('Field %s has wrong type' % name)
    if length is not None:
        value = value[:length]
    return value


def get_json_string(input, name, required=False, default=None, length=None):
    return str(get_json_unicode(input, name, required, default, length))


def get_json_bool(input, name, required=False, default=None):
    value = _nested_get(input, name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, bool):
        raise ValueError('Field %s has wrong type' % name)
    return value


def get_json_int(input, name, required=False, default=None):
    value = _nested_get(input, name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, int):
        raise ValueError('Field %s has wrong type' % name)
    return value


def get_json_date(input, name, required=False, default=None):
    value = _nested_get(input, name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        raise ValueError('Field %s is not a valid date' % name)
    return value


def export_image(context, request, image_attr, caption_attr, **kw):
    images_view = getMultiAdapter((context, request), name='images')
    scale = images_view.scale(image_attr, **kw)
    if scale is None:
        return None

    info = {'thumbnail': scale.url,
            'original': '%s/@@download/image/%s' %
                (context.absolute_url(),
                    getattr(context, image_attr).filename),
            'caption': getattr(context, caption_attr, None)}
    return info


class JsonView(grok.View):
    """Generic base class for JSON views.

    This class does two things:

    1. it renders the result as JSON
    2. if a request has a body it will try to JSON-parse it and
       store the result as ``self.input``.

    """
    martian.baseclass()
    grok.layer(IAPISkinLayer)

    input = None

    def render(self):
        # Workaround for grok silliness
        pass

    def do_OPTIONS(self):
        methods = [name[3:] for name in dir(self)
                   if name.startswith('do_')]
        self.response.setHeader('Allow', ','.join(sorted(methods)))
        return None

    def __call__(self):
        input = self.request.stdin.getvalue()
        if input:
            try:
                self.input = json.loads(input)
            except ValueError:
                self.response.setHeader('Content-Type', 'application/json')
                return json.dumps({'type': 'error',
                                   'message': 'Invalid JSON input'})

        mapply(self.update, (), self.request)
        if self.response.getStatus() in [302, 303]:
            return  # Shortcircuit on redirect, no need to render

        self.response.setHeader('Content-Type', 'application/json')
        method = self.request.get('REQUEST_METHOD', 'GET').upper()
        renderer = getattr(self, 'do_%s' % method, None)
        if renderer is None:
            log.info('Invalid HTTP method %s attempted for %s',
                    method, '/'.join(self.context.getPhysicalPath()))
            self.response.setStatus(405)
            response = {'type': 'error',
                        'message': 'HTTP method not allowed'}
        else:
            response = mapply(renderer, (), self.request)
        return json.dumps(response)


class GenericError(JsonView):
    grok.context(Exception)
    grok.name('index.html')

    def do_GET(self):
        return {'type': 'error',
                'message': 'An unknown error occurred.'}


class UnauthorizedError(JsonView):
    grok.context(Unauthorized)
    grok.name('index.html')

    def __call__(self):
        # Jump through hoops to prevent Zope2 Unauthorized handling from
        # messing with our message.
        result = {'type': 'error',
                  'message': 'Access denied.'}
        response = self.request.response
        response.setHeader('Content-Type', 'application/json')
        response._has_challenged = True
        response.setBody(json.dumps(result), lock=True)
        return response


class NotFoundView(JsonView):
    grok.context(NotFound)
    grok.name('index.html')

    def do_GET(self):
        return {'type': 'error',
                'message': 'Unknown resource requested.'}
