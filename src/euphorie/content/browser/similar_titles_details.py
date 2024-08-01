from euphorie.content import MessageFactory as _
from euphorie.content.surveygroup import ISurveyGroup
from io import StringIO
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView

import csv
import datetime


class SimilarTitlesDetails(BrowserView):
    """A view that shows the risks that have a title similar to the title
    of the current risk.
    """

    @property
    @memoize
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


class SimilarTitlesDetailsCSV(SimilarTitlesDetails):
    def write_data(self, data, writer):
        """Write data to CSV writer.
        First cell is the risk title (heading).
        Starting from the second row, every column is headed by a tool title
        and contains one solution per row.
        """
        writer.writerow([self.context.Title()])
        solutions = [
            [self.get_tool_for_brain(risk).Title()]
            + [solution.Description() for solution in solutions]
            for risk, solutions in data.items()
        ]
        max_len = max(map(len, solutions))
        for idx in range(max_len):
            writer.writerow((sub[idx] if len(sub) > idx else "") for sub in solutions)

    def __call__(self):
        buffer = StringIO()
        writer = csv.writer(buffer, delimiter=";")

        self.write_data(self.solutions_by_risk(), writer)

        csv_data = buffer.getvalue()
        buffer.close()
        response = self.request.RESPONSE
        today_iso = datetime.date.today().isoformat()
        response.setHeader(
            "Content-Disposition",
            (
                f"attachment; filename=similar_titles_details_{self.context.Title()}_"
                f"{today_iso}.csv"
            ),
        )
        response.setHeader("Content-Type", "text/csv;charset=utf-8")
        return csv_data
