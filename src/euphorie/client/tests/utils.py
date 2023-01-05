from euphorie.client import CONDITIONS_VERSION
from euphorie.client import model
from euphorie.client.browser import publish
from euphorie.content.browser import upload
from Products.MailHost.MailHost import MailHost
from z3c.saconfig import Session
from zope.sendmail.mailer import SMTPMailer
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.HTTPResponse import HTTPResponse

import sys


def addAccount(login="jane@example.com", password="Øle"):
    account = model.Account(
        loginname=login,
        password=password,
        tc_approved=CONDITIONS_VERSION,
    )
    session = Session()
    session.add(account)
    session.flush()
    return account


def addSurvey(portal, xml_survey):
    """Add a survey to the portal.

    This function requires that you are already loggin in as portal
    owner.
    """
    importer = upload.SectorImporter(portal.sectors.nl)
    sector = importer(xml_survey, None, None, None, "test import")
    survey = sector.values()[0]["test-import"]
    publisher = publish.PublishSurvey(survey, portal.REQUEST)
    publisher.publish()


def testRequest():
    """Create a new request object.

    This is based on the code in
    :py:func`Testing.makerequest.makerequest`.
    """
    environ = {"SERVER_NAME": "localhost", "SERVER_PORT": "80", "REQUEST_METHOD": "GET"}
    request = HTTPRequest(sys.stdin, environ, HTTPResponse())
    request._steps = ["Plone"]
    return request


def registerUserInClient(browser, link="Registreer"):
    browser.getLink(link).click()
    browser.getControl(name="email").value = "guest@example.com"
    browser.getControl(name="password1:utf8:ustring").value = "Guest12345#!"
    browser.getControl(name="password2:utf8:ustring").value = "Guest12345#!"
    browser.getControl(name="terms").controls[0].click()
    browser.getControl(name="register").click()
    # Screw the terms and conditions, just go to the Dashboard...
    browser.getLink("Dashboard").click()
    # # XXX Why does this not always happen??
    # if "terms-and-conditions" in browser.url:
    #     browser.getForm().submit()


class MockMailFixture:
    def __init__(self):
        self.storage = storage = []

        def send(self, *a, **kw):
            storage.append((a, kw))

        self._original_send = MailHost.send
        MailHost.send = send

    def __del__(self):
        SMTPMailer.send = self._original_send
