from AccessControl.Permissions import manage_users as ManageUsers
from euphorie.client import authentication
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
from zope.i18nmessageid import MessageFactory as mf

import mimetypes


mimetypes.add_type("image/svg+xml", ".svg")


MessageFactory = mf("euphorie")
del mf

#: Version number for terms and conditions. Updating this version will
#: require all users to (re)confirm their acceptance of the terms and
#: conditions
CONDITIONS_VERSION = 1


def initialize(context):
    registerMultiPlugin(authentication.EuphorieAccountPlugin.meta_type)
    context.registerClass(
        authentication.EuphorieAccountPlugin,
        permission=ManageUsers,
        constructors=(
            authentication.manage_addEuphorieAccountPlugin,
            authentication.addEuphorieAccountPlugin,
        ),
        visibility=None,
    )

    # Instruct the email module to use quoted printable for UT8
    import email.charset

    email.charset.add_charset("utf-8", email.charset.QP, email.charset.QP, "utf-8")

    # Monkeypatch the publisher to disable its WebDAV logic so we can use
    # all request methods for our REST API.
    import ZPublisher.HTTPRequest

    ZPublisher.HTTPRequest.HTTPRequest.maybe_webdav_client = 0
