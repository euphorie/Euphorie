from five import grok
from euphorie.client.api import JsonView
from euphorie.client.sector import IClientSector
from euphorie.client.survey import ISurvey


class View(JsonView):
    grok.context(IClientSector)
    grok.name('index_html')
    grok.require('zope2.Public')

    def do_GET(self):
        info = {'id': self.context.id,
                'title': self.context.title}
        surveys = [survey for survey in self.context.values()
                   if ISurvey.providedBy(survey)]
        language = self.request.form.get('language')
        if language:
            surveys = [survey for survey in surveys
                       if survey.language == language]
        info['surveys'] = [{'id': survey.id,
                            'title': survey.title,
                            'language': survey.language}
                           for survey in surveys]
        return info
