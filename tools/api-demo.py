#!bin/python

import argparse
import collections
import json
import sys
import requests


class API(object):
    """Minimal wrapper around the Euphorie API.

    This is pure convenience to make it easier to call the API and not have
    to provide the auth_token by hand for every request.
    """
    api_url = 'http://api.euphorie.hosting.simplon.biz'

    def __init__(self, auth_token=None, api_url=None):
        self.auth_token = auth_token
        if api_url is not None:
            self.api_url = api_url

    def _request(self, func, url_path, **kw):
        if not url_path.startswith(self.api_url):
            url = '%s/%s' % (self.api_url, url_path)
        else:
            url = url_path
        data = json.dumps(kw) if kw else None
        if self.auth_token:
            headers = {'X-Euphorie-Token': self.auth_token}
            response = func(url, data=data, headers=headers)
        else:
            response = func(url, data=data)
        if response.status_code != 200:
            raise RuntimeError('Server returned HTTP error %d' %
                    response.status_code)
        return response.json

    def get(self, *a, **kw):
        return self._request(requests.get, *a, **kw)

    def post(self, *a, **kw):
        return self._request(requests.post, *a, **kw)

    def put(self, *a, **kw):
        return self._request(requests.put, *a, **kw)

    def delete(self, *a, **kw):
        return self._request(requests.delete, *a, **kw)


def show_menu(info):
    menu = info.get('menu')
    if not menu:
        return

    todo = collections.deque((entry, 0) for entry in menu)
    while todo:
        (entry, level) = todo.popleft()
        print '%s - %s %s' % ('  ' * level, entry['number'], entry['title'])
        todo.extendleft((sub, level + 1) for sub in entry['children'])


def main():
    parser = argparse.ArgumentParser(
            description='Euphorie client API test tool')
    parser.add_argument('-s', '--server',
            default='https://api.instrumenten.rie.nl',
            help='URL for API server')
    parser.add_argument('-S', '--survey', default='nl/stigas/bos-en-natuur',
            help='Survey path to use')
    parser.add_argument('-m', '--menu', action='store_true', default=False,
            help='Show menu for every step.')
    parser.add_argument('login', help='Login name for online client')
    parser.add_argument('password', help='Password used to login')
    options = parser.parse_args()

    api = API()
    api.api_url = options.server
    version = api.get('/')
    print 'Euphorie version: %s' % version['euphorie-version']
    print 'API version: %s' % version['api-version']

    # First we must authenticate the user
    user_info = api.post('/users/authenticate',
            login=options.login, password=options.password)
    api.auth_token = user_info['token']
    print 'Succesfully authenticated user %s' % user_info['login']
    print 'Authentication token: %s' % api.auth_token
    if user_info.get('sessions'):
        print 'Currently known sessions for this user:'
        for session in user_info['sessions']:
            print ' - %s, last modified on %s' % \
                    (session['title'],
                            session['modified'])
            if session['survey'] == options.survey:
                print '  -> Removing this old demo session'
                api.delete('/users/%d/sessions/%d' %
                        (user_info['id'], session['id']))

    # Start a new session
    print 'Creating a new survey session.'
    info = api.post('/users/%d/sessions' % user_info['id'],
            survey=options.survey, title='API demonstratie')
    if info['type'] == 'error':
        print >> sys.stderr, 'Error: %s' % info['message']
        return 1

    company_url = '/users/%d/sessions/%d/company' % \
            (user_info['id'], info['id'])
    company = api.get(company_url)
    if company['type'] == 'dutch-company':
        print 'Dutch company type detected. Modifying data.'
        company = api.put(company_url,
                **{'visit-address': {
                    'address': 'Dorpstraat 2',
                    'city': 'Ons Dorp'},
                 'absentee-percentage': 15})

    # Keep moving forward through the survey, always following next-step
    while 'next-step' in info:
        print
        print 'Moving on to %s' % info['next-step']
        info = api.get('%s?menu' % info['next-step'])
        if 'title' in info:
            print 'Title: %s' % info['title']
        if options.menu:
            show_menu(info)


if __name__ == '__main__':
    main()
