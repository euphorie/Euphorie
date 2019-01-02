# coding=utf-8
from euphorie.client.session import SessionManager
from logging import getLogger
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from euphorie.client.update import redirectOnSurveyUpdate

logger = getLogger(__name__)


class TrainingSlide(BrowserView):
    """ Template / macro to hold the training slide markup
    Currently not active in default Euphorie
    """

    def __call__(self):
        return self


class TrainingView(BrowserView):
    """ The view that shows the main-menu Training module
    Currently not active in default Euphorie
    """

    def __call__(self):
        if redirectOnSurveyUpdate(self.request):
            return
        pptx_view = self.context.restrictedTraverse('pptx', None)
        if pptx_view:
            self.slide_data = pptx_view.get_data()
        else:
            self.slide_data = None
        if self.request.environ["REQUEST_METHOD"] == "POST":

            for entry in self.request.form:
                if entry.startswith("training_notes"):
                    try:
                        index = int(entry.split("-")[-1])
                    except:
                        continue
                    risk_data = self.slide_data['slides'][index]
                    sql_item = risk_data['row']
                    value = safe_unicode(self.request[entry])
                    sql_item.training_notes = value
                    self.slide_data['slides'][index]['row'] = sql_item
                    risk_data['training_notes'] = value
                SessionManager.session.touch()

        return self.index()
