# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class RegisterTests(EuphorieTestCase):
    def afterSetUp(self):
        from zope.interface import alsoProvides
        from euphorie.client.interfaces import IClientSkinLayer
        super(RegisterTests, self).afterSetUp()
        self.loginAsPortalOwner()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)

    def testConflictWithPloneAccount(self):
        view=self.portal.client.restrictedTraverse("register")
        view.errors={}
        view.request.form["email"]=self.portal._owner[1]
        view.request.form["password1"]="secret"
        view.request.form["password2"]="secret"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)

    def testBasicEmailVerification(self):
        view=self.portal.client.restrictedTraverse("register")
        view.errors={}
        view.request.form["email"]="wichert"
        view.request.form["password1"]="secret"
        view.request.form["password2"]="secret"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)

        view.errors.clear()
        view.request.form["email"]="wichert@wiggy net"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)

        view.errors.clear()
        view.request.form["email"]="wichert@wiggy.net"
        self.assertNotEqual(view._tryRegistration(), False)



class ReminderTests(EuphorieFunctionalTestCase):
    def addDummySurvey(self):
        from euphorie.client.tests.utils import addSurvey
        survey="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Sector title</title>
                    <survey>
                      <title>Survey title</title>
                    </survey>
                  </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)


    def testUnknownAccount(self):
        self.addDummySurvey()
        browser=Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink("I forgot my password").click()
        browser.getControl(name="loginname").value="jane@example.com"
        browser.getControl(name="next").click()
        self.failUnless("Unknown email address" in browser.contents)


    def testEmail(self):
        import email
        from email.header import decode_header
        from email.header import make_header
        from Products.MailHost.mailer import SMTPMailer
        from euphorie.client.tests.utils import addAccount
        self.addDummySurvey()
        addAccount()

        params=[]

        def send(self, *args, **kw):
            params.append((args, kw))

        original_send=SMTPMailer.send
        SMTPMailer.send=send
        try:
            self.portal.email_from_address="discard@simplon.biz"
            self.portal.email_from_name="Euphorie website"

            browser=Browser()
            browser.open(self.portal.client.nl.absolute_url())
            browser.getLink("I forgot my password").click()
            browser.getControl(name="loginname").value="jane@example.com"
            browser.getControl(name="next").click()

            self.assertEqual(len(params), 1)
            (args, kw)=params[0]
            self.assertEqual(args[0], "discard@simplon.biz")
            self.assertEqual(args[1], ["jane@example.com"])
            msg=email.message_from_string(args[2])
            subject=make_header(decode_header(msg["Subject"]))
            self.assertEqual(unicode(subject), u"OiRA registration reminder")
            body=msg.get_payload(0)
            body=body.get_payload(decode=True).decode(body.get_content_charset("utf-8"))
            self.failUnless(u"Øle" in body)
        finally:
            SMTPMailer.send=original_send

