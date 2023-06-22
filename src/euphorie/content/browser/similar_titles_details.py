from euphorie.content import MessageFactory as _
from euphorie.content.surveygroup import ISurveyGroup
from plone import api
from Products.Five import BrowserView


class SimilarTitlesDetails(BrowserView):
    """The upload view for a :obj:`euphorie.content.sector"""

    @property
    def tool_cache(self):
        return {}

    def get_tool_for_brain(self, risk):
        cache_key = "/".join(risk.getPhysicalPath()[:6])
        cache = self.tool_cache
        value = cache.get(cache_key)
        if value is not None:
            return value
        for obj in risk.aq_chain:
            if ISurveyGroup.providedBy(obj):
                value = obj
                cache[cache_key] = value
                return value

    def label(self):
        return _("Risks similar to ${title}", mapping={"title": self.context.Title()})

    def get_solutions(self, risk):
        return [
            obj for obj in risk.objectValues() if obj.portal_type == "euphorie.solution"
        ]

    def solutions_by_risk(self):
        risks = [self.context] + [
            api.content.get(path) for path in self.request.form.get("paths", []) or []
        ]
        return {risk: self.get_solutions(risk) for risk in risks}
