from zope.component import getMultiAdapter
from Products.CMFCore.utils import _checkPermission
from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase


class SectorTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        return sector

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.assertTrue("euphorie.sector" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        sector = self.createSector()
        types = [fti.id for fti in sector.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.surveygroup"]))

    def testCanNotBeCopied(self):
        self.loginAsPortalOwner()
        sector = self.createSector()
        self.assertFalse(sector.cb_isCopyable())

    def testDeleteWithoutPublishedSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        addSurvey(sector, EMPTY_SURVEY)
        surveygroup = sector["test-survey"]
        self.assertEqual(surveygroup.published, None)
        deleteaction = getMultiAdapter((sector, sector.REQUEST), name='delete')
        self.assertEqual(deleteaction.verify(sector.aq_parent, sector), True)

    def testDeleteWithPublishedSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector, EMPTY_SURVEY)
        surveygroup = sector["test-survey"]
        publishview = getMultiAdapter((survey, survey.REQUEST), name='publish')
        publishview.publish()
        self.assertEqual(surveygroup.published, "standard-version")
        deleteaction = getMultiAdapter((sector, sector.REQUEST), name='delete')
        self.assertEqual(deleteaction.verify(sector.aq_parent, sector), False)


class SectorAsUserTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        sector.login = "sector"
        sector.indexObject()
        return sector

    def testGetUser(self):
        self.loginAsPortalOwner()
        self.createSector()
        account = self.portal.acl_users.getUser("sector")
        self.assertTrue(account.getUserId())
        self.assertEqual(account.getUserName(), "sector")

    def testGetUserById(self):
        from plone.uuid.interfaces import IUUID
        self.loginAsPortalOwner()
        sector = self.createSector()
        uid = IUUID(sector)
        account = self.portal.acl_users.getUserById(uid)
        self.assertEqual(account.getUserId(), uid)
        self.assertEqual(account.getUserName(), "sector")

    def testGetUserProperties(self):
        self.loginAsPortalOwner()
        sector = self.createSector()
        sector.title = u"This is a sector"
        sector.contact_email = u"sector@example.com"
        account = self.portal.acl_users.getUser("sector")
        self.assertEqual(account.getProperty("fullname"), "This is a sector")
        self.assertEqual(account.getProperty("email"), "sector@example.com")

    def testSetProperties(self):
        self.loginAsPortalOwner()
        sector = self.createSector()
        sector.title = u"This is a sector"
        account = self.portal.acl_users.getUser("sector")
        account.setProperties(fullname=u"My New Name")
        self.assertEqual(sector.title, u"My New Name")

    def testResetPassword(self):
        # Part of https://code.simplon.biz/tracker/tno-euphorie/ticket/111
        from euphorie.content.user import UserAuthentication
        self.loginAsPortalOwner()
        sector = self.createSector()
        sector.title = u"This is a sector"
        pas = self.portal.acl_users
        auth = UserAuthentication(sector)
        self.assertEqual(
                auth.authenticateCredentials(dict(password="s3cr3t")), None)
        pas.userSetPassword(auth.getUserId(), "s3cr3t")
        self.assertEqual(
                auth.authenticateCredentials(dict(password="s3cr3t")),
                (auth.getUserId(), auth.getUserName()))


class SectorBrowserTests(EuphorieFunctionalTestCase):

    def testDuplicateLoginNotAllowed(self):
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/152
        from euphorie.content.tests.utils import createSector
        createSector(self.portal, login="sector")
        browser = self.adminBrowser()
        browser.open(
                "%s/sectors/nl/@@manage-users" % self.portal.absolute_url())
        browser.getLink("Add new sector").click()
        browser.getControl(name="form.widgets.title").value = "New sector"
        browser.getControl(name="form.widgets.login").value = "sector"
        browser.getControl(name="form.widgets.password").value = "secret"
        browser.getControl(
                name="form.widgets.password.confirm").value = "secret"
        browser.getControl(
                name="form.widgets.contact_name").value = "John Doe"
        browser.getControl(
                name="form.widgets.contact_email").value = "john@example.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertTrue("This login name is already taken" in browser.contents)

    def testPasswordPolicy(self):
        from euphorie.content.tests.utils import createSector
        createSector(self.portal, login="sector")
        browser = self.adminBrowser()
        browser.open(
                "%s/sectors/nl/@@manage-users" % self.portal.absolute_url())
        browser.getLink("Add new sector").click()
        browser.getControl(name="form.widgets.title").value = "New sector"
        browser.getControl(name="form.widgets.login").value = "sector"
        browser.getControl(name="form.widgets.password").value = "secret"
        browser.getControl(
                name="form.widgets.password.confirm").value = "secret"
        browser.getControl(
                name="form.widgets.contact_name").value = "Max Mustermann"
        browser.getControl(
                name="form.widgets.contact_email").value = "max@example.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertTrue(
            u"Your password must contain at least 5 characters, "
            u"including at least one capital letter, one number and "
            u"one special character (e.g. $, # or @)." in browser.contents)


class PermissionTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        sector.login = "sector"
        sector.indexObject()
        return sector

    def testSectorWorkflowUsed(self):
        self.setRoles(["Manager"])
        sector = self.createSector()
        wt = self.portal.portal_workflow
        self.assertEqual(wt.getChainFor(sector), ("sector",))
        self.assertEqual(wt.getInfoFor(sector, "review_state"), "hidden")

    def testAnonymous(self):
        self.setRoles(["Manager"])
        sector = self.createSector()
        self.logout()
        self.assertTrue(
                not _checkPermission("Euphorie: Add new RIE Content", sector))
        self.assertTrue(
                not _checkPermission("Access contents information", sector))
        self.assertTrue(not _checkPermission("Change portal events", sector))
        self.assertTrue(not _checkPermission("Modify portal content", sector))
        self.assertTrue(not _checkPermission("View", sector))

    def testSector(self):
        from plone.uuid.interfaces import IUUID
        self.setRoles(["Manager"])
        sector = self.createSector()
        self.login(IUUID(sector))
        self.assertTrue(
                _checkPermission("Euphorie: Add new RIE Content", sector))
        self.assertTrue(
                _checkPermission("Access contents information", sector))
        self.assertTrue(_checkPermission("Change portal events", sector))
        self.assertTrue(_checkPermission("Modify portal content", sector))
        self.assertTrue(_checkPermission("View", sector))

    def testCountryManager(self):
        self.setRoles(["Manager"])
        sector = self.createSector()
        self.portal.acl_users._doAddUser(
                "support", "secret", ["CountryManager"], [])
        self.login("support")
        self.assertTrue(
                _checkPermission("Euphorie: Add new RIE Content", sector))
        self.assertTrue(
                _checkPermission("Access contents information", sector))
        self.assertTrue(_checkPermission("Change portal events", sector))
        self.assertTrue(_checkPermission("Modify portal content", sector))
        self.assertTrue(_checkPermission("View", sector))

    def testManager(self):
        self.setRoles(["Manager"])
        sector = self.createSector()
        self.portal.acl_users._doAddUser("manager", "secret", ["Manager"], [])
        self.login("manager")
        self.assertTrue(
                _checkPermission("Euphorie: Add new RIE Content", sector))
        self.assertTrue(
                _checkPermission("Access contents information", sector))
        self.assertTrue(_checkPermission("Change portal events", sector))
        self.assertTrue(_checkPermission("Modify portal content", sector))
        self.assertTrue(_checkPermission("View", sector))


class GetSurveysTests(EuphorieTestCase):
    def getSurveys(self, context):
        from euphorie.content.sector import getSurveys
        return getSurveys(context)

    def testOutsideSector(self):
        self.assertEqual(self.getSurveys(None), [])

    def testSingleUnpublishedSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector, EMPTY_SURVEY)
        self.assertEqual(self.getSurveys(survey),
                [{"url": "http://nohost/plone/sectors/nl/sector/test-survey",
                  "published": False,
                  "id": "test-survey",
                  "title": u"Test survey",
                  "surveys": [
                      {"id": "standard-version",
                       "title": u"Standard version",
                       "current": True,
                       "url": "http://nohost/plone/sectors/nl/sector/"
                                "test-survey/standard-version",
                       "versions": [],
                       "modified": False,
                       "published": False}],
                 }])

    def testTwoUnpublishedSurveysgroups(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector, EMPTY_SURVEY)
        addSurvey(sector, EMPTY_SURVEY, "Test survey 2")
        result = self.getSurveys(survey)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], u"Test survey")
        self.assertEqual(result[1]["title"], u"Test survey 2")

    def testSurveygroupTwoSurveys(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector, EMPTY_SURVEY)
        surveygroup = sector["test-survey"]
        surveygroup.invokeFactory("euphorie.survey", "next-edition",
                title=u"Very latest")
        result = self.getSurveys(survey)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]["surveys"]), 2)
        self.assertEqual(result[0]["surveys"][0]["current"], True)
        self.assertEqual(result[0]["surveys"][1]["current"], False)
        self.assertEqual(result[0]["surveys"][1]["title"], u"Very latest")

    def testPublishedSurvey(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector, EMPTY_SURVEY)
        surveygroup = sector["test-survey"]
        surveygroup.published = "standard-version"
        result = self.getSurveys(survey)
        self.assertEqual(result[0]["published"], True)
        self.assertEqual(result[0]["surveys"][0]["published"], True)
