# coding=utf-8
from euphorie.content.tests.utils import _create
from euphorie.testing import EuphorieIntegrationTestCase
from plone.dexterity.interfaces import IDexterityFTI
from z3c.form.interfaces import IDataManager
from zope import component

import bcrypt


class CountryManagerTests(EuphorieIntegrationTestCase):

    def createCountryManager(self):
        manager = _create(
            self.portal.sectors["nl"], "euphorie.countrymanager", "mgr"
        )
        return manager

    def testCanNotBeCopied(self):
        self.loginAsPortalOwner()
        manager = self.createCountryManager()
        self.assertFalse(manager.cb_isCopyable())

    def testPasswordsAreHashed(self):
        self.loginAsPortalOwner()
        manager = self.createCountryManager()

        fti = component.queryUtility(IDexterityFTI, name=manager.portal_type)
        field = fti.lookupSchema().get('password')
        component.getMultiAdapter((manager, field), IDataManager).set('secret')

        self.assertFalse(manager.password == 'secret')
        self.assertTrue(
            bcrypt.hashpw('secret', manager.password) == manager.password
        )
