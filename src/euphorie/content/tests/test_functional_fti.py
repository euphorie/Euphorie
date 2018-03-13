# coding=utf-8
from ...ghost import PathGhost
from ..fti import check_fti_paste_allowed
from euphorie.content.fti import ConditionalDexterityFTI
from euphorie.content.fti import IConstructionFilter
from euphorie.content.module import Module
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zope.component import adapts
from zope.component import getGlobalSiteManager
from zope.component import provideAdapter
from zope.interface import implements

import mock
import unittest


class Veto(object):
    adapts(ConditionalDexterityFTI, Module)
    implements(IConstructionFilter)

    def __init__(self, fti, container):
        self.fti = fti
        self.container = container

    def allowed(self):
        return False


class ConditionalDexterityFTITests(EuphorieIntegrationTestCase):

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createContent(self):
        with api.env.adopt_roles(['Member', 'Manager']):
            self.country = self.portal.sectors.nl
            self.sector = self._create(
                self.country, "euphorie.sector", "sector"
            )
            self.surveygroup = self._create(
                self.sector, "euphorie.surveygroup", "group"
            )
            self.survey = self._create(
                self.surveygroup, "euphorie.survey", "survey"
            )
            self.module = self._create(
                self.survey, "euphorie.module", "survey"
            )

    def testConditionalFtiUsedByModule(self):
        fti = getattr(self.portal.portal_types, "euphorie.module")
        self.failUnless(isinstance(fti, ConditionalDexterityFTI))

    def testVeto(self):
        self.createContent()
        provideAdapter(Veto, name="euphorie.module")
        try:
            fti = getattr(self.portal.portal_types, "euphorie.module")
            self.assertEqual(fti.isConstructionAllowed(self.module), False)
        finally:
            getGlobalSiteManager().unregisterAdapter(
                Veto, name="euphorie.module"
            )

    def testVetoRegisteredForOtherType(self):
        self.createContent()
        provideAdapter(factory=Veto, name="euphorie.solution")
        try:
            fti = getattr(self.portal.portal_types, "euphorie.module")
            self.assertEqual(fti.isConstructionAllowed(self.module), True)
        finally:
            getGlobalSiteManager().unregisterAdapter(
                Veto, name="euphorie.solution"
            )


class check_fti_paste_allowed_tests(unittest.TestCase):

    def check_fti_paste_allowed(self, *a, **kw):
        return check_fti_paste_allowed(*a, **kw)

    def test_acceptable_paste(self):
        content = mock.Mock()
        content.portal_type = 'euphorie.risk'
        fti = mock.Mock()
        fti.isConstructionAllowed.return_value = True
        with mock.patch('euphorie.content.fti.queryUtility', return_value=fti):
            self.check_fti_paste_allowed('folder', content)
            fti.isConstructionAllowed.assert_called_once_with('folder')

    def test_refuse_non_portal_content(self):
        self.assertRaises(
            ValueError, self.check_fti_paste_allowed, None, mock.Mock()
        )

    def test_do_not_use_acquisition_to_get_portal_type(self):
        parent = PathGhost('parent')
        parent.portal_type = 'euphorie.risk'
        content = PathGhost('child').__of__(parent)
        self.assertRaises(
            ValueError, self.check_fti_paste_allowed, None, content
        )

    def test_content_without_fti(self):
        content = mock.Mock()
        content.portal_type = 'euphorie.risk'
        self.assertRaises(
            ValueError, self.check_fti_paste_allowed, None, content
        )

    def test_fti_does_not_allow_construction(self):
        content = mock.Mock()
        content.portal_type = 'euphorie.risk'
        fti = mock.Mock()
        fti.isConstructionAllowed.return_value = False
        with mock.patch('euphorie.content.fti.queryUtility', return_value=fti):
            self.assertRaises(
                ValueError, self.check_fti_paste_allowed, 'folder', content
            )
