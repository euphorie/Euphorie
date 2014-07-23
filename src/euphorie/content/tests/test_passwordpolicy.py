from euphorie.deployment.tests.functional import EuphorieTestCase
from plone import api


class PasswordPolicyTests(EuphorieTestCase):

    def testPasswordPolicy(self):
        err_msg = \
            u"Your password must contain at least 5 characters, " \
            u"including at least one capital letter, one number and " \
            u"one special character (e.g. $, # or @')."
        regtool = api.portal.get_tool('portal_registration')
        self.assertEqual(regtool.pasValidation('password', 'secret'), err_msg)
        self.assertEqual(regtool.pasValidation('password', 'Secret'), err_msg)
        self.assertEqual(regtool.pasValidation('password', 'Secret1'), err_msg)
        self.assertIsNone(regtool.pasValidation('password', 'Secret1!'))
