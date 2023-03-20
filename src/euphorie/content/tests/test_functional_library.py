from euphorie.content.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.content.tests.utils import createSector
from euphorie.testing import EuphorieFunctionalTestCase
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from unittest import mock


class LibraryTests(EuphorieFunctionalTestCase):
    _default_credentials = {
        "username": SITE_OWNER_NAME,
        "password": SITE_OWNER_PASSWORD,
    }
    library = [
        {
            "title": "Library Sector Title",
            "url": "http://localhost/sector",
            "surveys": [
                {
                    "title": "Library Survey Title",
                    "path": "/portal/sector/survey/version",
                    "url": "http://localhost/portal/sector/survey/version",
                    "portal_type": "euphorie.sector",
                    "children": [
                        {
                            "title": "Library Risk",
                            "number": "1",
                            "path": "/portal/sector/surveys/version/1",
                            "url": "http://localhost/portal/sector/surveys/version/1",
                            "disabled": False,
                            "portal_type": "euphorie.risk",
                            "children": [],
                        }
                    ],
                }
            ],
        }
    ]

    def test_render(self):
        self.loginAsPortalOwner()
        sector = createSector(self.portal)
        with api.env.adopt_user("admin"):
            survey = addSurvey(sector, BASIC_SURVEY)
        browser = self.get_browser(logged_in=True)
        browser.handleErrors = False
        with mock.patch(
            "euphorie.content.browser.library.get_library", return_value=self.library
        ):
            browser.open(survey.absolute_url() + "/@@library")
        assert "Library Sector Title" in browser.contents
        assert "Library Survey Title" in browser.contents
        assert "Library Risk" in browser.contents
