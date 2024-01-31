from euphorie import MessageFactory as _
from path import Path
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from urllib.parse import quote
from weasyprint import CSS
from weasyprint import HTML

import logging


try:
    from tempfile import TemporaryDirectory
except ImportError:
    # PY2
    from backports.tempfile import TemporaryDirectory

log = logging.getLogger(__name__)

# The INFO/WARNING log levels log way to many messages for our needs.
# We have seen 3k log lines for a single pdf conversion in weasyprint 60.2.
# Limit weasyprint's log level to be less chatty.
# This could also be done through configuration:
# https://docs.python.org/3/library/logging.config.html#configuration-file-format
logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.WARNING)


class PdfView(BrowserView):
    """We use weasyprint to convert an HTML view into a PDF file."""

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def extra_css(self):
        return """
    @page {{
        @bottom-right {{
            content: "{label_page} " counter(page) " {label_page_of} " counter(pages);
        }}
    }}
        """.format(
            label_page=api.portal.translate(_("label_page", default="Page")),
            label_page_of=api.portal.translate(_("label_page_of", default="of")),
        )

    def view_to_pdf(self, view):
        content = view()
        extra_css = CSS(string=self.extra_css)

        with TemporaryDirectory(prefix="euphoprient") as tmpdir:
            html_file = Path(tmpdir) / "index.html"
            pdf_file = Path(tmpdir) / "index.pdf"
            html_file.write_text(content)
            HTML(html_file).write_pdf(
                pdf_file,
                stylesheets=[extra_css],
            )
            return pdf_file.bytes()

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        context = self.context
        view_name = self.request.get("view", "view")
        view = context.restrictedTraverse(view_name)
        pdf = self.view_to_pdf(view)

        filename = "{} - {}.pdf".format(
            api.portal.translate(view.label), view.session.title
        ).encode("utf-8")

        context.REQUEST.RESPONSE.setHeader("Content-Type", "application/pdf")
        context.REQUEST.RESPONSE.setHeader(
            "Content-Disposition", "attachment;filename*=UTF-8''%s" % quote(filename)
        )
        return pdf
