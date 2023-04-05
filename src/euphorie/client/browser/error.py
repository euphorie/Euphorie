from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zExceptions.ExceptionFormatter import format_exception

import logging
import sys


log = logging.getLogger(__name__)


class ErrorView(BrowserView):
    basic_template = ViewPageTemplateFile("templates/basic_error_message.pt")

    def is_manager(self):
        return getSecurityManager().checkPermission("Manage portal", self.context)

    def __call__(self):
        self.exception = aq_inner(self.context)
        self.context = aq_parent(self)
        log.exception("Error at %r", self.context)
        error_type = self.exception.__class__.__name__
        exc_type, value, traceback = sys.exc_info()
        error_tb = "".join(format_exception(exc_type, value, traceback, as_html=False))
        try:
            return self.index()
        except Exception:
            return self.basic_template(error_type=error_type, error_tb=error_tb)


class NotFound(ErrorView):
    @property
    @memoize
    def plone_redirector_view(self):
        return api.content.get_view(
            context=self.__parent__, request=self.request, name="plone_redirector_view"
        )

    def __call__(self):
        exception = self.context
        error_type = exception.__class__.__name__
        if error_type == "NotFound" and self.plone_redirector_view.attempt_redirect():
            # if a redirect is possible attempt_redirect returns True
            # and sets the proper location header
            return
        super().__call__()
