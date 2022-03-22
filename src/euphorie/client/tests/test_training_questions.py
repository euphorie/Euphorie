from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zExceptions import Unauthorized
from zope.interface import alsoProvides


class TestTrainingQuestions(EuphorieIntegrationTestCase):
    """There is a possibility to add training questions in a survey and evaluate
    the user comprehension of the training
    """

    def setUp(self):
        super(TestTrainingQuestions, self).setUp()
        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        self.survey = self.portal.client.nl.ict["software-development"]
        alsoProvides(self.survey.REQUEST, IClientSkinLayer)
        api.portal.set_registry_record("euphorie.use_training_module", True)
        survey_session = model.SurveySession(
            title=u"Dummy session",
            zodb_path="nl/ict/software-development",
            account=self.account,
            company=model.Company(country="nl", employees="1-9", referer="other"),
        )
        model.Session.add(survey_session)

    def _create_questions(self):
        with api.env.adopt_user("admin"):
            api.content.create(
                id="question-1",
                container=self.survey,
                type="euphorie.training_question",
                title=u"Why?",
                right_answer=u"Because!",
                wrong_answer_1=u"White",
                wrong_answer_2=u"Black",
            )
            api.content.create(
                id="question-2",
                container=self.survey,
                type="euphorie.training_question",
                title=u"Life on Mars?",
                right_answer=u"Probably not",
                wrong_answer_1=u"In the weekends",
                wrong_answer_2=u"42",
            )
            api.content.create(
                id="question-3",
                container=self.survey,
                type="euphorie.training_question",
                title=u"Who are you?",
                right_answer=u"The Who 🞋",
                wrong_answer_1=u"Annie Lennox",
                wrong_answer_2=u"David Bowie",
            )

    def test_training_questions(self):
        traversed_session = self.survey.restrictedTraverse("++session++1")
        with api.env.adopt_user(user=self.account):
            with self._get_view(
                "training", traversed_session, self.request.clone()
            ) as view:
                # No training if the survey has not enabled it
                self.assertEqual(view.question_intro_url, "")
            self.survey.enable_web_training = True
            with self._get_view(
                "training", traversed_session, self.request.clone()
            ) as view:
                # Jump direcly to the success page if there are no questions
                self.assertEqual(
                    view.question_intro_url,
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question_success",  # noqa: E501
                )
            self._create_questions()
            with self._get_view(
                "training", traversed_session, self.request.clone()
            ) as view:
                self.assertEqual(
                    view.question_intro_url,
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question_intro",  # noqa: E501
                )

            # The slide_question_intro is just a presentation of the questionaire
            with self._get_view(
                "slide_question_intro", traversed_session, self.request.clone()
            ) as view:
                self.assertListEqual(
                    [x.getId() for x in view.questions],
                    ["question-1", "question-2", "question-3"],
                )
                self.assertEqual(
                    view.first_question_url(),
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question/question-1",  # noqa: E501
                )

            # There is a certificate view but we cannot see it
            # if we have not started the training
            with self._get_view(
                "training-certificate", traversed_session, self.request.clone()
            ) as view:
                with self.assertRaises(Unauthorized):
                    view()

            # We can view the slides only if we have completed the previous ones
            with self._get_view(
                "slide_question", traversed_session, self.request.clone()
            ) as view:
                # emulate traversing and test some method/properties
                view.question_id = "question-1"
                self.assertEqual(view.progress, "1/3")
                self.assertEqual(view.question.title, u"Why?")
                self.assertIsNone(view.previous_question)
                self.assertEqual(view.next_question.title, "Life on Mars?")
                self.assertEqual(
                    view.next_url,
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question/question-2",  # noqa: E501
                )

                view.question_id = "question-2"
                view.request.__annotations__.clear()
                self.assertEqual(view.progress, "2/3")
                self.assertEqual(view.question.title, u"Life on Mars?")
                self.assertEqual(view.previous_question.title, "Why?")
                self.assertEqual(view.next_question.title, "Who are you?")
                self.assertEqual(
                    view.next_url,
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question/question-3",  # noqa: E501
                )

                view.question_id = "question-3"
                view.request.__annotations__.clear()
                self.assertEqual(view.progress, "3/3")
                self.assertEqual(view.question.title, u"Who are you?")
                self.assertEqual(view.previous_question.title, "Life on Mars?")
                self.assertIsNone(view.next_question)
                self.assertEqual(
                    view.next_url,
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question_try_again",  # noqa: E501
                )

                # Check validation so that we do not call the wrong slide
                view.question_id = "question-1"
                view.request.__annotations__.clear()
                view.validate()

                view.question_id = "question-2"
                view.request.__annotations__.clear()
                with self.assertRaises(Unauthorized):
                    view.validate()

                view.question_id = "question-3"
                view.request.__annotations__.clear()
                with self.assertRaises(Unauthorized):
                    view.validate()

                # Try to give some answer
                view.question_id = "question-1"
                view.request.__annotations__.clear()
                view.request.method = "POST"
                view.request.form["answer"] = "Because!"
                self.assertEqual(view(), view.next_url)
                self.assertEqual(
                    view.get_or_create_training().answers, '{"question-1": true}'
                )
                self.assertEqual(view.get_or_create_training().status, "in_progress")

                # Now we can see the first two slides
                view.question_id = "question-1"
                view.request.__annotations__.clear()
                self.assertIsNone(view.validate())

                view.question_id = "question-2"
                view.request.__annotations__.clear()
                self.assertIsNone(view.validate())

                # but not yet the last...
                view.question_id = "question-3"
                view.request.__annotations__.clear()
                with self.assertRaises(Unauthorized):
                    view.validate()

                # There is a certificate view but we cannot see it
                # if we have not completed the training
                with self._get_view(
                    "training-certificate", traversed_session, self.request.clone()
                ) as certificate:
                    with self.assertRaises(Unauthorized):
                        certificate()

                # We answer wrongly the second answer
                view.question_id = "question-2"
                view.request.__annotations__.clear()
                view.request.form["answer"] = "Foo"
                self.assertEqual(view(), view.next_url)
                self.assertIn(
                    '"question-2": false', view.get_or_create_training().answers
                )

                # We answer correctly the third answer
                view.question_id = "question-3"
                view.request.__annotations__.clear()
                view.request.form["answer"] = "The Who 🞋"
                self.assertEqual(view(), view.next_url)
                self.assertIn(
                    '"question-3": true', view.get_or_create_training().answers
                )
                self.assertEqual(view.get_or_create_training().status, "failed")

            with self._get_view(
                "slide_question_try_again", traversed_session, self.request.clone()
            ) as view:
                self.assertListEqual(view.failed_questions, [u"Life on Mars?"])

            # There is a certificate view but we cannot see it
            # if we have not completed the training succesfully
            with self._get_view(
                "training-certificate", traversed_session, self.request.clone()
            ) as view:
                with self.assertRaises(Unauthorized):
                    view()

            # We try again
            with self._get_view(
                "slide_question", traversed_session, self.request.clone()
            ) as view:
                view.question_id = "question-1"
                view.request.method = "POST"
                view.request.form["answer"] = "Because!"
                view()

                # Trying again resets resets the answers
                self.assertEqual(
                    view.get_or_create_training().answers, '{"question-1": true}'
                )
                view.question_id = "question-2"
                view.request.__annotations__.clear()
                view.request.form["answer"] = "Probably not"
                view()

                view.question_id = "question-3"
                view.request.__annotations__.clear()
                view.request.form["answer"] = "The Who 🞋"
                view()
                self.assertEqual(view(), view.next_url)
                self.assertEqual(
                    view.next_url,
                    "http://nohost/plone/client/nl/ict/software-development/++session++1/@@slide_question_success",  # noqa: E501
                )

            # Now we can view the certificate!
            with self._get_view(
                "training-certificate", traversed_session, self.request.clone()
            ) as view:
                view()
