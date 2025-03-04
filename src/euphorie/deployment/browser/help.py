from logging import getLogger
from plone import api
from plone.memoize.view import memoize_contextless
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import requests


logger = getLogger(__name__)


@implementer(IPublishTraverse)
class EuphorieHelpView(BrowserView):
    """A view that proxies the help pages from this or another site."""

    @property
    @memoize_contextless
    def help_base_url(self) -> str | None:
        """Compute the help_base_url."""
        return api.portal.get_registry_record("euphorie.help.remote_url", default=None)

    @property
    def help_relative_path(self) -> str:
        """Return relative path to the help resource"""
        request_url = self.request.getURL()
        path = request_url.partition(f"/@@{self.__name__}/")[-1]
        if not path:
            path = request_url.partition(f"/{self.__name__}/")[-1]
        return path

    def fetch_resource(self):
        """Fetch the requested resource from the remote URL."""
        remote_url = f"{self.help_base_url}/{self.help_relative_path}"
        response = requests.get(remote_url)

        if response.status_code == 404:
            raise NotFound(f"Resource not found: {remote_url}")
        elif response.status_code != 200:
            raise Exception(
                f"Failed to fetch resource: {remote_url} (status code: {response.status_code})"  # noqa: E501
            )

        return response

    def rewrite_body_links(self, body: str) -> str:
        """Rewrite the body content to use absolute URLs instead of relative paths."""
        portal_url = api.portal.get().absolute_url()
        return body.replace(
            "/assets/",
            f"{portal_url}/@@{self.__name__}/assets/",
        ).replace(
            "/media/",
            f"{portal_url}/@@{self.__name__}/media/",
        )

    def publishTraverse(self, request, name):
        return self

    def __call__(self) -> str | bytes:
        """Fetch the resource from the remote server and return it.

        In case of text content, rewrite the links to use absolute URLs.
        """
        if not self.help_base_url:
            logger.error(
                "Remote URL not set, please configure the registry record: euphorie.help.remote_url"  # noqa: E501
            )
            raise NotFound()

        response = self.fetch_resource()

        content_type: str = response.headers.get("Content-Type", "")

        if content_type.startswith("text/"):
            body = self.rewrite_body_links(response.text)
        else:
            body = response.content

        self.request.response.setHeader("Content-Type", content_type)
        return body
