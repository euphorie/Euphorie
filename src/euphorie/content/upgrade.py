from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

import logging


log = logging.getLogger(__file__)


class CleanupContent(BrowserView):
    def __call__(self):
        ct = getToolByName(self.context, "portal_catalog")
        output = []
        for brain in ct(portal_type="euphorie.risk"):
            obj = brain.getObject()
            pd = getattr(obj, "problem_description", None)
            if pd and "[info]" in pd:
                path = "/".join(obj.getPhysicalPath())
                msg = "Removing bogus problem description for %s" % path
                log.debug(msg)
                output.append(msg)
                obj.problem_description = ""

        if not output:
            return "No problematic problem descriptions found"

        return "\n".join(output)
