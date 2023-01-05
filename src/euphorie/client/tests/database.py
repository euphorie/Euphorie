import unittest
import z3c.saconfig.tests


z3c.saconfig.tests  # Keep PyFlakes happy


class DatabaseTests(unittest.TestCase):
    create_tables = True

    def setUp(self):
        super().setUp()
        from euphorie.client import model
        from Products.Five import fiveconfigure
        from z3c.saconfig import Session
        from Zope2.App.zcml import load_config

        import euphorie.client.tests

        fiveconfigure.debug_mode = True
        load_config("configure.zcml", euphorie.client.tests)
        fiveconfigure.debug_mode = False
        if self.create_tables:
            model.metadata.create_all(Session.bind, checkfirst=True)

    def tearDown(self):
        super().tearDown()
        from euphorie.client import model
        from z3c.saconfig import Session

        import transaction

        Session.remove()
        model.metadata.drop_all(Session.bind)
        transaction.abort()
