import collections
import datetime
import logging
import json
import re
import martian
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.publisher.publish import mapply
from five import grok
from zope.i18n import translate
from z3c.appconfig.interfaces import IAppConfig
from euphorie.client.navigation import getTreeData
from euphorie.client.update import wasSurveyUpdated
from euphorie.client.api.interfaces import IClientAPISkinLayer


log = logging.getLogger(__name__)


def context_menu(request, context, phase, filter):
    menu = getTreeData(request, context, phase, filter)['children']
    todo = collections.deque(menu)
    matcher = re.compile(r'^.*%s' % phase)
    url_root = request.survey_session.absolute_url()
    while todo:
        node = todo.popleft()
        if node['type'] == 'risk':
            node['status'] = None
            if node['class']:
                if 'postponed' in node['class']:
                    node['status'] = 'postponed'
                elif 'risk' in node['class']:
                    node['status'] = 'present'
                elif 'answered' in node['class']:
                    node['status'] = 'not-present'
        del node['id']
        del node['class']
        del node['leaf_module']
        del node['path']
        del node['current_parent']
        node['url'] = matcher.sub(url_root, node['url'])
        todo.extend(node['children'])
    return menu


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


def get_json_token(input, name, field, required=False, default=None):
    value = input.get(name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    try:
        return field.vocabulary.getTermByToken(value).value
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


def get_json_int(input, name, required=False, default=None):
    value = input.get(name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, int):
        raise ValueError('Field %s has wrong type' % name)
    return value


def get_json_date(input, name, required=False, default=None):
    value = input.get(name)
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
    config = getUtility(IAppConfig)
    client_url = config.get("euphorie", {}).get("client")
    if client_url:
        client_url = client_url.rstrip('/')
        old_base = request.client.absolute_url()
        info['thumbnail'] = info['thumbnail'].replace(old_base, client_url)
        info['original'] = info['original'].replace(old_base, client_url)
    return info


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

    phase = 'identification'
    previous_phase = None
    next_phase = None
    question_filter = None
    check_update = False

    def _step(self, info, key, finder, next_phase=None):
        node = finder(self.context, self.request.survey_session,
                self.question_filter)
        if node is not None:
            info[key] = '%s/%s/%s' % \
                    (self.request.survey_session.absolute_url(),
                    '/'.join(node.short_path), self.phase)
        elif next_phase:
            info[key] = '%s/%s' % \
                    (self.request.survey_session.absolute_url(),
                     next_phase)

    def render(self):
        # Workaround for grok silliness
        pass

    def __call__(self):
        if self.check_update and \
            wasSurveyUpdated(self.request.survey_session, self.request.survey):
            url = '%s/update' % self.request.survey_session.absolute_url()
            return {'type': 'update',
                    'next-step': url}

        input = self.request.stdin.getvalue()
        if input:
            try:
                self.input = json.loads(input)
            except ValueError:
                self.response.setHeader(
                        'Content-Type', 'application/json')
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
                    method, '.'.join(self.context.getPhysicalPath()))
            self.response.setStatus(405)
            response = {'type': 'error',
                        'message': 'HTTP method not allowed'}
        else:
            response = mapply(renderer, (), self.request)
        return json.dumps(response)
