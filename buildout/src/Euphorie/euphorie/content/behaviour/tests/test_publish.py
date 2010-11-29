import unittest

class Mock(object):
    pass


class HandleWorkflowTransitionTests(unittest.TestCase):
    def handleWorklowTransition(self, obj, event):
        from euphorie.content.behaviour.publish import handleWorklowTransition
        handleWorklowTransition(obj, event)

    def testPublishTransitionNoFlagPresent(self):
        survey=Mock()
        event=Mock()
        event.action="publish"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, True)

    def testPublishTransitionFlagPresent(self):
        survey=Mock()
        survey.published=False
        event=Mock()
        event.action="publish"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, True)

    def testDoNothingOnOtherTransition(self):
        survey=Mock()
        survey.published=False
        event=Mock()
        event.action="update"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, False)

    def testRetract(self):
        survey=Mock()
        survey.published=True
        event=Mock()
        event.action="retract"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, False)

