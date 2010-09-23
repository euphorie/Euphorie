# coding=utf-8

def addAccount(login="jane@example.com", password=u"Øle"):
    from z3c.saconfig import Session
    from euphorie.client import model
    account=model.Account(loginname="jane@example.com", password=u"Øle")
    session=Session()
    session.add(account)
    session.flush()



def addSurvey(portal, xml_survey):
    """Add a survey to the portal. This function requires that you are already
    loggin in as portal owner."""
    from euphorie.content import upload
    from euphorie.client import publish
    importer=upload.SectorImporter(portal.sectors.nl)
    sector=importer(xml_survey, None, None, None, u"test import")
    survey=sector.values()[0]["test-import"]
    publisher=publish.PublishSurvey(survey, portal.REQUEST)
    publisher.publish()


def testRequest():
    """Create a new request object. This is based on the code in
    :py:func`Testing.makerequest.makerequest`."""
    import sys
    from ZPublisher.HTTPRequest import HTTPRequest
    from ZPublisher.HTTPResponse import HTTPResponse
    environ={"SERVER_NAME": "localhost",
             "SERVER_PORT": "80",
             "REQUEST_METHOD": "GET"}
    request=HTTPRequest(sys.stdin, environ, HTTPResponse())
    request._steps=["Plone"]
    return request


def registerUserInClient(browser):
    browser.getLink("register").click()
    browser.getControl(name="email").value="guest"
    browser.getControl(name="password1:utf8:ustring").value="guest"
    browser.getControl(name="password2:utf8:ustring").value="guest"
    browser.getControl(name="next", index=1).click()

