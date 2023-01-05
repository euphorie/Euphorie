from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.content import MessageFactory as _
from Products.PlonePAS.plugins import passwordpolicy
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from zope import globalrequest
from zope.interface import implementer

import re


@implementer(IValidationPlugin)
class EuphoriePasswordPolicy(passwordpolicy.PasswordPolicyPlugin):
    """Simple Password Policy to ensure password is 5 chars long."""

    id = "euphorie_password_policy"
    meta_type = "Euphorie Password Policy"
    security = ClassSecurityInfo()

    security.declarePrivate("validateUserInfo")

    def validateUserInfo(self, user, set_id, set_info):
        """See IValidationPlugin.

        Used to validate password property
        """
        if IClientSkinLayer.providedBy(globalrequest.getRequest()):
            # We don't enforce the custom password policy for client users
            return super().validateUserInfo(user, set_id, set_info)

        if not set_info:
            return []
        password = set_info.get("password", None)
        if password is None:
            return []

        failed = False
        if len(password) < 5:
            failed = True
        elif len([letter for letter in password if letter.isupper()]) == 0:
            # Must have capital letter(s)
            failed = True
        elif not re.search("[1-9]", password):
            # Must have numbers(s)
            failed = True
        elif not re.search("[^a-zA-Z1-9]", password):
            # Must have special chars (i.e. not alphanumerical)
            failed = True

        if failed:
            return [
                {
                    "id": "password",
                    "error": _(
                        "password_policy_conditions",
                        default="Your password must contain at least 5 characters, "
                        "including at least one capital letter, one number and "
                        "one special character (e.g. $, # or @).",
                    ),
                }
            ]
        else:
            return []


InitializeClass(EuphoriePasswordPolicy)
