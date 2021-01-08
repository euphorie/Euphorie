import unittest
import z3c.saconfig.tests


z3c.saconfig.tests  # Keep PyFlakes happy


class DatabaseTests(unittest.TestCase):
    create_tables = True

    def setUp(self):
        super(DatabaseTests, self).setUp()
        from euphorie.client import model
        from Products.Five import fiveconfigure
        from Products.Five import zcml
        from z3c.saconfig import Session

        import euphorie.client.tests

        fiveconfigure.debug_mode = True
        zcml.load_config("configure.zcml", euphorie.client.tests)
        fiveconfigure.debug_mode = False
        if self.create_tables:
            model.metadata.create_all(Session.bind, checkfirst=True)

    def tearDown(self):
        super(DatabaseTests, self).tearDown()
        from euphorie.client import model
        from z3c.saconfig import Session

        Session.remove()
        model.metadata.drop_all(Session.bind)
