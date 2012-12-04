import collections
import json
import re
import martian
from five import grok
from euphorie.json import JsonView as BaseJsonView
from ..navigation import getTreeData
from ..update import wasSurveyUpdated
from .interfaces import IClientAPISkinLayer


class JsonView(BaseJsonView):
    martian.baseclass()
    grok.layer(IClientAPISkinLayer)

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

    def __call__(self):
        if self.check_update and wasSurveyUpdated(
                self.request.survey_session, self.request.survey):
            url = '%s/update' % self.request.survey_session.absolute_url()
            self.response.setHeader('Content-Type', 'application/json')
            return json.dumps(
                    {'type': 'update',
                     'next-step': url})
        return super(JsonView, self).__call__()


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
