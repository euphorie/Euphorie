# vim: fileencoding=utf-8
from euphorie.testing import EuphorieIntegrationTestCase
from plone.namedfile.file import NamedBlobImage


class PublicationTests(EuphorieIntegrationTestCase):

    @property
    def client(self):
        return self.portal.client

    def createSurvey(self):
        self.portal.sectors.nl.invokeFactory(
            "euphorie.sector", "dining", title=u"Fine diningÂ®"
        )
        self.sector = self.portal.sectors.nl.dining
        self.sector.invokeFactory(
            "euphorie.surveygroup", "survey", title=u"Survey"
        )
        self.surveygroup = self.sector.survey
        self.surveygroup.invokeFactory(
            "euphorie.survey", "version1", title=u"Version 1"
        )
        self.survey = self.surveygroup.version1
        return self.survey

    def testPublishEmptySurvey(self):
        self.createSurvey()
        self.surveygroup.evaluation_algorithm = u"dummy"
        view = self.survey.restrictedTraverse("@@publish")
        view.publish()
        self.assertEqual(set(self.client.objectIds()), set(['nl', 'api']))
        self.assertEqual(self.client.nl.objectIds(), ["dining"])
        sector = self.client.nl.dining
        self.assertEqual(sector.portal_type, "euphorie.clientsector")
        self.assertEqual(sector.Title(), u"Fine diningÂ®")
        survey = sector.survey
        self.assertEqual(survey.portal_type, "euphorie.survey")
        self.assertEqual(survey.evaluation_algorithm, u"dummy")
        self.assertEqual(survey.title, u"Survey")
        self.assertEqual(survey.objectIds(), [])

    def testPublishSurveyWithQuestion(self):
        self.createSurvey()
        modid = self.survey.invokeFactory("euphorie.module", "module")
        module = getattr(self.survey, modid)
        qid = module.invokeFactory(
            "euphorie.risk", "risk", title=u"Do you offer take away?"
        )
        view = self.survey.restrictedTraverse("@@publish")
        view.publish()
        self.assertEqual(self.client.nl.objectIds(), ["dining"])
        survey = self.client.nl.dining.survey
        self.assertEqual(survey.objectIds(), [modid])
        self.assertEqual(getattr(survey, modid).objectIds(), [qid])

    def testPublishRemovesExistingObject(self):
        self.createSurvey()
        self.client.invokeFactory("euphorie.clientcountry", "nl")
        self.client.nl.invokeFactory("euphorie.clientsector", "dining")
        self.client.nl.dining.invokeFactory("euphorie.survey", "survey")
        self.client.nl.dining.survey.old_object = True
        view = self.survey.restrictedTraverse("@@publish")
        view.publish()
        self.assertEqual(
            getattr(self.client.nl.dining, "old_object", False), False
        )

    def testPublishUpdatesLogo(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/136
        white_gif = (
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff,'
            '\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        )
        black_gif = (
            'GIF89a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xff\xff\xff,'
            '\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        )
        self.createSurvey()
        self.sector.logo = NamedBlobImage(
            data=white_gif, contentType="image/gif", filename=u"white.gif"
        )
        view = self.survey.restrictedTraverse("@@publish")
        view.publish()
        client_sector = self.client.nl["dining"]
        self.assertEqual(client_sector.logo.data, white_gif)
        images = client_sector.restrictedTraverse("@@images")
        white_scale = images.scale(
            "logo", height=100, direction="up"
        ).data.data
        self.sector.logo = NamedBlobImage(
            data=black_gif, contentType="image/gif", filename=u"black.gif"
        )
        view.publish()
        self.assertEqual(client_sector.logo.data, black_gif)
        images = client_sector.restrictedTraverse("@@images")
        black_scale = images.scale(
            "logo", height=100, direction="up"
        ).data.data
        self.assertNotEqual(white_scale, black_scale)


class PreviewTests(EuphorieIntegrationTestCase):

    def testPreviewGetsCorrectUrl(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/95
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        survey = addSurvey(sector)
        view = survey.restrictedTraverse("@@preview")
        preview = view.publish()
        self.assertEqual(preview.id, "preview")
        self.assertEqual(
            preview.absolute_url(),
            "http://nohost/plone/client/nl/sector/preview"
        )
