from five import grok
from euphorie.json import get_json_bool
from euphorie.json import get_json_unicode
from ..countrymanager import ICountryManager
from . import JsonView


class View(JsonView):
    grok.context(ICountryManager)
    grok.require('zope2.View')
    grok.name('index_html')

    attributes = [
            ('title', 'title', get_json_unicode),
            ('email', 'contact_email', get_json_unicode),
            ('password', 'password', get_json_unicode),
            ('locked', 'locked', get_json_bool),
            ]

    def do_GET(self):
        return {'type': 'countrymanager',
                'id': self.context.id,
                'title': self.context.title,
                'email': self.context.contact_email,
                'login': self.context.login,
                'locked': self.context.locked}

    def do_PUT(self):
        try:
            self.update_object(self.attributes, ICountryManager)
        except ValueError as e:
            return {'type': 'error',
                    'message': str(e)}
        return self.do_GET()
