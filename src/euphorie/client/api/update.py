from five import grok
from euphorie.client.model import SurveySession
from euphorie.client.api.profile import View as ProfileView


class View(ProfileView):
    grok.context(SurveySession)
    grok.name('update')
    grok.require('zope2.Public')

    def do_GET(self):
        info = super(View, self).do_GET()
        info['type'] = 'update'
        return info

    def do_PUT(self):
        info = super(View, self).do_PUT()
        info['type'] = 'profile'
        return info
