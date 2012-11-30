from AccessControl import getSecurityManager
from zExceptions import Unauthorized
from zope.component import getUtility
from zope.interface import Invalid
from zope.security.interfaces import IPermission
from Products.CMFCore.permissions import ModifyPortalContent
from five import grok
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from euphorie.json import get_json_bool
from euphorie.json import get_json_string
from ..countrymanager import ICountryManager
from . import JsonView


class View(JsonView):
    grok.context(ICountryManager)
    grok.require('zope2.View')
    grok.name('index_html')

    attributes = [
            ('title', 'title', get_json_string),
            ('email', 'contact_email', get_json_string),
            ('password', 'password', get_json_string),
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
        checkPermission = getSecurityManager().checkPermission
        permissions = ICountryManager.queryTaggedValue(WRITE_PERMISSIONS_KEY, {})
        try:
            for (field, attribute, getter) in self.attributes:
                value = getter(self.input, field)
                if value is None:
                    continue
                ztk_permission = permissions.get(attribute, None)
                if ztk_permission is not None:
                    permission = getUtility(IPermission, name=ztk_permission).title
                else:
                    permission = ModifyPortalContent
                if not checkPermission(permission, self.context):
                    raise Unauthorized()
                ICountryManager[attribute].validate(value)
                setattr(self.context, attribute, value)
        except (Invalid, ValueError) as e:
            return {'type': 'error',
                    'message': str(e)}
        return self.do_GET()
