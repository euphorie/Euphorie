from five import grok
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.client.profile import extractProfile
from euphorie.client.profile import set_session_profile


class View(JsonView):
    grok.context(SurveySession)
    grok.name('profile')
    grok.require('zope2.Public')

    def survey(self):
        return self.request.client.restrictedTraverse(
                self.context.zodb_path.split('/'))

    def do_GET(self):
        survey = self.survey()
        answers = extractProfile(survey, self.context)
        result = []
        for (key, answer) in answers.items():
            question = survey[key]
            info = {'id': question.id,
                    'question': question.question or question.title,
                    'value': answer}
            result.append(info)
        return {'id': self.context.id,
                'type': 'profile',
                'title': self.context.title,
                'profile': result}

    def do_PUT(self):
        survey = self.survey()
        questions = survey.ProfileQuestions()
        if set([q.id for q in questions]) != set(self.input):
            return {'type': 'error',
                    'message': 'Provided data does not match profile.'}
        for question in questions:
            input = self.input[question.id]
            if isinstance(input, list) and \
                    all(isinstance(v, unicode) for v in input):
                continue
            return {'type': 'error',
                    'message': 'Invalid profile data.'}

        self.context = set_session_profile(survey, self.context, self.input)
        return self.do_GET()
