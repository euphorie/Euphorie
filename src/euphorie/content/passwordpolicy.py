from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PlonePAS.plugins import passwordpolicy
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from euphorie.content import MessageFactory as _
from zope.interface import implements


class EuphoriePasswordPolicy(passwordpolicy.PasswordPolicyPlugin):
    """Simple Password Policy to ensure password is 5 chars long.
    """
    id = "euphorie_password_policy"
    meta_type = "Euphorie Password Policy"
    implements(IValidationPlugin)
    security = ClassSecurityInfo()

    security.declarePrivate('validateUserInfo')
    def validateUserInfo(self, user, set_id, set_info ):
        """ See IValidationPlugin. Used to validate password property
        """
        # FIXME: still using the stock Plone policy

        if not set_info:
            return []
        password = set_info.get('password', None)
        if password is None:
            return []
        elif password == '':
            return [{'id':'password','error':_(u'Minimum 5 characters.')}]
        elif len(password) < 5:
            return [{'id':'password','error':
                _(u'Your password must contain at least 5 characters.')}]
        else:
            return []

InitializeClass(EuphoriePasswordPolicy)

