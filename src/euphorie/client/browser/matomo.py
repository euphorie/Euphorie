# Helper to assist with tuning the matomo/piwik tracking code for Euphorie
from euphorie.client.interfaces import IClientSkinLayer
from plone import api
from Products.Five import BrowserView
from zope.interface import alsoProvides

import json
import logging
import urllib.parse


logger = logging.getLogger("MatomoView")


class JSONTrackingVariablesView(BrowserView):
    """A helper that returns variables needed for tracking as json
    must be called on the tool, not on the session
    """

    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        self.request.response.setHeader(
            "Cache-Control", "no-cache, no-store, must-revalidate"
        )
        self.request.response.setHeader("Pragma", "no-cache")
        self.request.response.setHeader("Expires", "0")
        alsoProvides(self.request, IClientSkinLayer)
        webhelpers = api.content.get_view("webhelpers", self.context, self.request)

        data = {
            "country_name": webhelpers.country_name,
            "sector_name": webhelpers.sector_name,
            "tool_name": webhelpers.tool_name,
            "language_code": webhelpers.language_code,
        }
        came_from = self.request.form.get("came_from", "")

        # Get the data from the came_from query string if not already set
        if came_from:
            # Parse query string from
            # came_from=/oira-tools/eu/eu-automation-of-tasks/eu-automation-of-tasks .
            path_elems = came_from.split("/")

            # Extract missing values from `came_from`
            if not data["country_name"] and len(path_elems) > 2:
                data["country_name"] = path_elems[2]
            if not data["sector_name"] and len(path_elems) > 3:
                data["sector_name"] = path_elems[3]
            if not data["tool_name"] and len(path_elems) > 4:
                data["tool_name"] = path_elems[4]

        return json.dumps(data, indent=2)


class MockTrackingView(BrowserView):
    """A simple tracking endpoint mimicking a piwik.php request"""

    def __call__(self):
        request = self.request
        method = request.get("REQUEST_METHOD", "GET")

        # Extract tracking parameters from GET or POST
        params = (
            request.form
            if method == "POST"
            else request.environ.get("QUERY_STRING", "")
        )
        parsed_params = urllib.parse.parse_qs(params)
        logger.info("\n--- Decoded Tracking Request ---\n")

        # Log the request details
        for key, value in parsed_params.items():
            logger.info(f"{key}: {', '.join(value)}")

        # Return a 1x1 transparent pixel to simulate tracking
        self.request.response.setHeader("Content-Type", "image/gif")
        self.request.response.setHeader(
            "Cache-Control", "no-cache, no-store, must-revalidate"
        )
        self.request.response.setHeader("Pragma", "no-cache")
        self.request.response.setHeader("Expires", "0")

        # Return a simple 1x1 pixel
        pixel = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b"  # noqa: E501
        return pixel
