from euphorie.client import model
from euphorie.client.browser.risk import IdentificationView
from euphorie.client.model import Risk
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.risk import IFrenchEvaluation as IFr
from euphorie.content.risk import IKinneyEvaluation as IKi
from euphorie.content.survey import Survey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.base.utils import safe_text
from Products.CMFPlone.tests.dummy import Image
from unittest import mock
from zope.publisher.interfaces import NotFound

import unittest


class EvaluationViewTests(unittest.TestCase):
    def EvaluationView(self, **kw):
        """
        Note: the EvaluationView does not exist as a separate view any more.
        Its functionality was merged to the identification view.
        For these tests, we just keep the name EvaluationView but return
        IdentificationView, since it contains all the relevant code
        """
        return IdentificationView(Risk(**kw), None)

    def Risk(self, **kw):
        return Risk(**kw)

    def reply(self, freq, effect, prob=None):
        if prob is None:  # French
            return {
                "frequency": IFr["default_frequency"]
                .vocabulary.getTermByToken(freq)
                .value,
                "severity": IFr["default_severity"]
                .vocabulary.getTermByToken(effect)
                .value,
            }
        else:  # Kinney
            return {
                "frequency": IKi["default_frequency"]
                .vocabulary.getTermByToken(freq)
                .value,
                "effect": IKi["default_effect"].vocabulary.getTermByToken(effect).value,
                "probability": IKi["default_probability"]
                .vocabulary.getTermByToken(prob)
                .value,
            }

    def test_evaluation_algorithm_fallback(self):
        view = self.EvaluationView()
        risk = self.Risk()
        self.assertEqual(view.evaluation_algorithm(risk), "kinney")

    def test_evaluation_algorithm_survey_parent(self):
        view = self.EvaluationView()
        survey = Survey()
        survey.evaluation_algorithm = "dummy"
        risk = self.Risk().__of__(survey)
        self.assertEqual(view.evaluation_algorithm(risk), "dummy")

    def test_calculatePriority_kinney_nothing_set(self):
        view = self.EvaluationView()
        risk = self.Risk()
        risk.evaluation_method = "calculated"
        with mock.patch(
            "euphorie.client.browser.risk.evaluation_algorithm", return_value="kinney"
        ):
            self.assertEqual(view.calculatePriority(risk, {}), None)

    def test_calculatePriority_french_nothing_set(self):
        view = self.EvaluationView()
        risk = self.Risk()
        risk.evaluation_method = "calculated"
        with mock.patch(
            "euphorie.client.browser.risk.evaluation_algorithm", return_value="french"
        ):
            self.assertEqual(view.calculatePriority(risk, {}), None)

    def test_calculatePriority_french(self):
        view = self.EvaluationView()
        with mock.patch(
            "euphorie.client.browser.risk.evaluation_algorithm", return_value="french"
        ):
            risk = self.Risk()
            risk.evaluation_method = "calculated"
            # Risks with weak severity are always low priority
            for freq in ["rare", "not-often", "often", "regularly"]:
                self.assertEqual(
                    view.calculatePriority(risk, self.reply(freq, "weak")), "low"
                )
            # High priority items
            self.assertEqual(
                view.calculatePriority(risk, self.reply("often", "severe")), "high"
            )
            self.assertEqual(
                view.calculatePriority(risk, self.reply("often", "very-severe")), "high"
            )
            self.assertEqual(
                view.calculatePriority(risk, self.reply("regularly", "severe")), "high"
            )
            self.assertEqual(
                view.calculatePriority(risk, self.reply("regularly", "very-severe")),
                "high",
            )
            # Some medium priority items
            self.assertEqual(
                view.calculatePriority(risk, self.reply("rare", "very-severe")),
                "medium",
            )
            self.assertEqual(
                view.calculatePriority(risk, self.reply("not-often", "not-severe")),
                "medium",
            )

    def test_calculatePriority_kinney(self):
        view = self.EvaluationView()
        risk = self.Risk()
        risk.evaluation_method = "calculated"
        with mock.patch(
            "euphorie.client.browser.risk.evaluation_algorithm", return_value="kinney"
        ):
            # Risks with weak severity are always low priority
            for freq in ["almost-never", "regular", "constant"]:
                self.assertEqual(
                    view.calculatePriority(risk, self.reply(freq, "weak", "small")),
                    "low",
                )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("constant", "significant", "medium")
                ),
                "high",
            )
            self.assertEqual(
                view.calculatePriority(risk, self.reply("constant", "high", "medium")),
                "high",
            )
            self.assertEqual(
                view.calculatePriority(risk, self.reply("constant", "weak", "medium")),
                "medium",
            )


class TestRiskImageDownloadUpload(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        self.account = addAccount(password="secret")
        addSurvey(self.portal, BASIC_SURVEY)
        survey_session = model.SurveySession(
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=self.account,
        )
        self.risk = survey_session.addChild(
            model.Risk(title="risk 1", zodb_path="1")
        ).__of__(survey_session.traversed_session)
        model.Session.add(survey_session)

    def test_upload(self):
        with api.env.adopt_user(user=self.account):
            with self._get_view("image-upload", self.risk) as view:
                # Just calling the view with no request returns to the
                # @@identification page
                view()
                self.assertDictEqual(
                    view.request.response.headers,
                    {
                        "location": "http://nohost/plone/client/nl/ict/software-development/++session++1/1/@@identification"  # noqa: E501
                    },
                )

                # Uploading an image will save it to the risk
                view.request.form["image"] = Image()
                view()
                self.assertTrue(self.risk.image_data.startswith(b"GIF"))
                self.assertEqual(self.risk.image_filename, "dummy.gif")

                # We can also require to remove the image
                view.request.form.pop("image")
                view.request.form["image-remove"] = "1"
                view()
                self.assertIsNone(self.risk.image_data)
                self.assertFalse(self.risk.image_filename)

                # If we have a scale wipe it
                self.risk.image_data_scaled = b"foo"
                view.request.form["image"] = Image()
                view()
                self.assertEqual(self.risk.image_filename, "dummy.gif")
                self.assertIsNone(self.risk.image_data_scaled)

                # but do not wipe it if we are uploading the same image again
                self.risk.image_data_scaled = b"foo"
                view()
                self.assertEqual(self.risk.image_data_scaled, b"foo")

    def test_download(self):
        with api.env.adopt_user(user=self.account):
            with self._get_view("image-display", self.risk) as view:
                # If the risk has no image raise a not found
                with self.assertRaises(NotFound):
                    view()

                # Otherwise return the file
                self.risk.image_data = Image.data
                self.risk.image_filename = safe_text(Image.filename)
                self.assertTrue(view().startswith(b"GIF"))
                self.assertDictEqual(
                    view.request.response.headers,
                    {
                        "accept-ranges": "bytes",
                        "content-length": "168",
                        "content-type": "image/gif",
                        "link": '<http://nohost/plone/client/nl/ict/software-development/%2B%2Bsession%2B%2B1/1/@@download/None/dummy.gif>; rel="canonical"',  # noqa: E501
                    },
                )

                # Check that we can crop and scale the image on the fly
                view.fieldname = "image_training"
                self.assertTrue(view().startswith(b"\x89PNG"))

                headers = view.request.response.headers.copy()
                self.assertAlmostEqual(
                    int(headers.pop("content-length")), 6971, delta=10
                )
                self.assertDictEqual(
                    headers,
                    {
                        "accept-ranges": "bytes",
                        "content-type": "image/png",
                        "link": '<http://nohost/plone/client/nl/ict/software-development/%2B%2Bsession%2B%2B1/1/@@download/image_training/dummy.gif>; rel="canonical"',  # noqa: E501
                    },
                )
