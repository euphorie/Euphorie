# coding=utf-8
from collections import namedtuple
from euphorie import MessageFactory as _
from path import Path
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from sh import wkhtmltopdf
from six.moves.urllib.parse import quote

import logging
import six


try:
    from sh import xvfb_run
except ImportError:
    xvfb_run = namedtuple("xvfb_run", "wkhtmltopdf")(wkhtmltopdf=wkhtmltopdf)

try:
    from tempfile import TemporaryDirectory
except ImportError:
    # PY2
    from backports.tempfile import TemporaryDirectory

log = logging.getLogger(__name__)


class PdfView(BrowserView):
    """We use wkhtmltopdf to convert an HTML view into a PDF file."""

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def footer_options(self):
        return (
            "--footer-right",
            u"{} [page] {} [topage]".format(
                api.portal.translate(_(u"label_page", default=u"Page")),
                api.portal.translate(_(u"label_page_of", default=u"of")),
            ),
            "--footer-font-size",
            "8",
        )

    def view_to_pdf(self, view):
        content = view()
        wkhtmltopdf_args = api.portal.get_registry_record(
            "euphorie.wkhtmltopdf.options",
            default=(
                "--margin-bottom 2cm --margin-left 2cm "
                "--margin-right 2cm --margin-top 3cm "
                "--disable-javascript --viewport-size 10000x1000"
            ),
        ).split()
        wkhtmltopdf_args.extend(self.footer_options)

        with TemporaryDirectory(prefix="euphoprient") as tmpdir:
            html_file = Path(tmpdir) / "index.html"
            pdf_file = Path(tmpdir) / "index.pdf"
            if six.PY2:
                html_file.write_text(content.encode("utf-8"))
            else:
                html_file.write_text(content)
            wkhtmltopdf_args.extend([html_file, pdf_file])
            xvfb_run.wkhtmltopdf(*wkhtmltopdf_args)
            return pdf_file.bytes()

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
