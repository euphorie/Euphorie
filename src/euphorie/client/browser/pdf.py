# coding=utf-8
from plone import api
from plone.memoize.view import memoize
from Products.CMFPlone.utils import safe_bytes
from Products.Five import BrowserView
from six import StringIO
from six.moves.urllib.parse import quote

import logging
import zipfile


try:
    from base64 import decodebytes
except ImportError:
    # PY27
    from base64 import decodestring as decodebytes

try:
    from base64 import encodebytes
except ImportError:
    # PY27
    from base64 import encodestring as encodebytes

try:
    from xmlrpc.client import ServerProxy
    from xmlrpc.client import Transport
except ImportError:
    # PY2
    from xmlrpclib import ServerProxy
    from xmlrpclib import Transport

try:
    from http.client import HTTPConnection
except ImportError:
    # PY2
    from httplib import HTTPConnection

log = logging.getLogger(__name__)


class TimeoutTransport(Transport):
    def make_connection(self, host):
        return HTTPConnection(host, timeout=120.0)


class PdfView(BrowserView):
    """We use smartprintng to convert an HTML view into a PDF file.

    This requires that we render the view, add the contents to a ZIP
    file, and send it to the smartprintng server via an xmlrpc call.
    """

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        context = self.context
        view_name = self.request.get("view", "view")
        view = context.restrictedTraverse(view_name)
        pdf = self.view_to_pdf(view)

        filename = u"{} - {}.pdf".format(
            api.portal.translate(view.label), view.session.title
        ).encode("utf-8")

        context.REQUEST.RESPONSE.setHeader("Content-Type", "application/pdf")
        context.REQUEST.RESPONSE.setHeader(
            "Content-Disposition", "attachment;filename*=UTF-8''%s" % quote(filename)
        )
        return pdf

    def view_to_pdf(self, view):
        content = view()
        html = self.untidy_html(content)
        zip_content = self.string_to_zip(
            filename=self.context.getId() + ".html", content=html
        )
        return self.zip_to_pdf(zip_content)

    def untidy_html(self, content):
        """smartprintng insists on replacing "<html." with a tag which
        includes the xmlns attribute. Our content already has the
        xmlns attribute and lang, so we need to replace that with
        "<html>" to keep smartprintng happy :/
        """
        html_index = content.find("<html")
        everything_before_html = content[:html_index]
        everything_after_html = content[content.find(">", html_index) + 1 :]
        content = everything_before_html + "<html>" + everything_after_html
        return content.encode("utf-8")

    def zip_to_pdf(self, zip_content):
        """xmlrpclib changed between Python 2.7 and 2.6, since the code for
        the server was written with the 2.6 version in mind we need to
        call the xmlrpc methods in an unusual way.

        We cannot call the method directly, so we create a ServerProxy
        object with the full URL of the xmlrpc method and then we
        trigger the call of the method by trying to access any
        attribute i.e. "dummy", but any imaginary attribute lookup
        will suffice.
        """
        proxy = ServerProxy
        print_url = api.portal.get_registry_record(
            "euphorie.smartprintng_url", default="http://localhost:6543"
        )
        timeout_transport = TimeoutTransport()

        ping = proxy(print_url + "/ping")
        if ping.dummy.data() != "zopyx.smartprintng.server":
            log.error("Can't connect to smartprintng server")
            return

        convert2ZIP = proxy(print_url + "/convertZIP", transport=timeout_transport)
        encoded_pdf = convert2ZIP.dummy("", encodebytes(zip_content), "pdf-prince")
        pdf = decodebytes(safe_bytes(encoded_pdf))
        # There might be bogus content before the %PDF marker:
        # brute-force remove it, because it prevents the PDF from being
        # opened in some versions of Acrobat
        idx = pdf.find("%PDF")
        if idx > 0:
            pdf = pdf[idx:]
        return pdf

    def string_to_zip(self, filename, content):
        zip_file = StringIO()
        with zipfile.ZipFile(zip_file, "w") as zf:
            zf.writestr(filename, content)
        zip_file.seek(0)
        return zip_file.read()
