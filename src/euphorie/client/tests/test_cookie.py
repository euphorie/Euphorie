# coding=utf-8
from euphorie.client.cookie import _sign
from euphorie.client.cookie import getCookie
from euphorie.client.cookie import setCookie
from euphorie.client.tests.utils import testRequest
from ZPublisher.HTTPResponse import HTTPResponse

import binascii
import unittest


class SetCookieTests(unittest.TestCase):

    def setCookie(self, response, secret, name, value, timeout=0):
        return setCookie(response, secret, name, value, timeout)

    def test_basic(self):
        response = HTTPResponse()
        self.setCookie(response, "secret", "euphorie", "123")
        self.assertTrue('euphorie' in response.cookies)
        cookie = response.cookies['euphorie']
        self.assertTrue('expires' not in cookie)
        self.assertEqual(cookie['path'], '/')
        self.assertEqual(cookie['http_only'], True)
        self.assertEqual(cookie['value'], 's2QukE8flTyx94ketu53fjEyMw==')

    def test_timeout(self):
        response = HTTPResponse()
        self.setCookie(response, "secret", "euphorie", "123", 3600)
        cookie = response.cookies['euphorie']
        self.assertTrue('expires' in cookie)


class GetCookieTests(unittest.TestCase):

    def getCookie(self, request, secret, name):
        return getCookie(request, secret, name)

    def test_no_cookie(self):
        request = testRequest()
        self.assertEqual(self.getCookie(request, "secret", "euphorie"), None)

    def test_bad_base64(self):
        request = testRequest()
        request.cookies["euphorie"] = "invalid"
        self.assertEqual(self.getCookie(request, "secret", "euphorie"), None)

    def test_invalid_format(self):
        request = testRequest()
        request.cookies["euphorie"] = binascii.b2a_base64("invalid").rstrip()
        self.assertEqual(self.getCookie(request, "secret", "euphorie"), None)

    def test_short_cookie(self):
        request = testRequest()
        request.cookies["euphorie"] = binascii.b2a_base64("short").rstrip()
        self.assertEqual(self.getCookie(request, "secret", "euphorie"), None)

    def test_invalid_signature(self):
        request = testRequest()
        request.cookies["euphorie"] = binascii.b2a_base64(
            "12345678901234567890"
        ).rstrip()
        self.assertEqual(self.getCookie(request, "secret", "euphorie"), None)

    def test_valid_signature(self):
        request = testRequest()
        value = "%s1" % _sign("secret", "1")
        request.cookies["euphorie"] = binascii.b2a_base64(value).rstrip()
        self.assertEqual(self.getCookie(request, "secret", "euphorie"), "1")
