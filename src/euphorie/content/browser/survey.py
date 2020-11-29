# coding=utf-8
from ..module import IModule
from ..profilequestion import IProfileQuestion
from ..utils import DragDropHelper
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five import BrowserView
from zope.component import getMultiAdapter


class SurveyView(BrowserView, DragDropHelper):
    def _morph(self, child):
        state = getMultiAdapter((child, self.request), name="plone_context_state")
        return {"id": child.id, "title": child.title, "url": state.view_url()}

    @property
    def children(self):
        return [
            self._morph(child)
            for child in self.context.values()
            if IModule.providedBy(child) or IProfileQuestion.providedBy(child)
        ]

    @property
    def group(self):
        return aq_parent(aq_inner(self.context))
