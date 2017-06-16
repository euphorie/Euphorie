from Acquisition import aq_parent
from AccessControl.Permissions import delete_objects
from zExceptions import Unauthorized
from five import grok
from euphorie.json import get_json_bool
from euphorie.json import get_json_unicode
from ..sector import ISector
from . import JsonView


class View(JsonView):
    grok.context(ISector)
    grok.require('zope2.View')
    grok.name('index_html')

    attributes = [
            ('title', 'title', get_json_unicode),
            ('contact.email', 'contact_email', get_json_unicode),
            ('contact.name', 'contact_name', get_json_unicode),
            ('password', 'password', get_json_unicode),
            ('locked', 'locked', get_json_bool),
            ]

    def do_GET(self):
        return {'type': 'sector',
                'id': self.context.id,
                'title': self.context.title,
                'contact': {
                    'name': self.context.contact_name,
                    'email': self.context.contact_email,
                },
                'login': self.context.login,
                'locked': self.context.locked}

    def do_DELETE(self):
        container = aq_parent(self.context)
        if not self.has_permission(delete_objects, container):
            raise Unauthorized()
        container.manage_delObjects([self.context.id])
        return {'type': 'ok'}

    def do_PUT(self):
        try:
            self.update_object(self.attributes, ISector)
        except ValueError as e:
            return {'type': 'error',
                    'message': str(e)}
        return self.do_GET()
