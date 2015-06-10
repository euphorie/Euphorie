# coding=utf-8
from z3c.saconfig import Session
from euphorie.client import model


def addAccount(login="jane@example.com", password=u"Øle"):
    from euphorie.client import CONDITIONS_VERSION
    account = model.Account(loginname=login, password=password,
            tc_approved=CONDITIONS_VERSION)
    session = Session()
    session.add(account)
    session.flush()
    return account


def createSurvey():
    session = Session()
    account = model.Account(loginname=u"jane", password=u"secret")
    session.add(account)
    survey = model.SurveySession(title=u"Session", zodb_path="survey",
            account=account)
    session.add(survey)
    return (session, survey)


def addSurvey(portal, xml_survey):
    """Add a survey to the portal. This function requires that you are already
    loggin in as portal owner."""
    from euphorie.content import upload
    from euphorie.client import publish
    importer = upload.SectorImporter(portal.sectors.nl)
    sector = importer(xml_survey, None, None, None, u"test import")
    survey = sector.values()[0]["test-import"]
    publisher = publish.PublishSurvey(survey, portal.REQUEST)
    publisher.publish()


def testRequest():
    """Create a new request object. This is based on the code in
    :py:func`Testing.makerequest.makerequest`."""
    import sys
    from ZPublisher.HTTPRequest import HTTPRequest
    from ZPublisher.HTTPResponse import HTTPResponse
    environ = {"SERVER_NAME": "localhost",
               "SERVER_PORT": "80",
               "REQUEST_METHOD": "GET"}
    request = HTTPRequest(sys.stdin, environ, HTTPResponse())
    request._steps = ["Plone"]
    return request


def registerUserInClient(browser, link="register"):
    browser.getLink(link).click()
    browser.getControl(name="email").value = "guest@example.com"
    browser.getControl(name="password1:utf8:ustring").value = "guest"
    browser.getControl(name="password2:utf8:ustring").value = "guest"
    browser.getControl(name="next", index=0).click()
    # XXX Why does this not always happen??
    if "terms-and-conditions" in browser.url:
        browser.getForm().submit()


class MockMailFixture(object):
    def __init__(self):
        self.storage = storage = []

        from Products.MailHost.MailHost import MailHost

        def send(self, *a, **kw):
            storage.append((a, kw))
        self._original_send = MailHost.send
        MailHost.send = send

    def __del__(self):
        from Products.MailHost.mailer import SMTPMailer
        SMTPMailer.send = self._original_send
