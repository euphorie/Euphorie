# coding=utf-8
from Products.Five import BrowserView
from logging import getLogger

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
    pass
