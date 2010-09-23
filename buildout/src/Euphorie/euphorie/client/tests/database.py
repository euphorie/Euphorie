import z3c.saconfig.tests
import unittest

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        super(DatabaseTests, self).setUp()
        from euphorie.client import model
        from z3c.saconfig import Session
        from Products.Five import zcml
        from Products.Five import fiveconfigure
        import euphorie.client.tests

        fiveconfigure.debug_mode = True
        zcml.load_config("configure.zcml", euphorie.client.tests)
        fiveconfigure.debug_mode = False
        model.metadata.create_all(Session.bind, checkfirst=True)

    def tearDown(self):
        super(DatabaseTests, self).tearDown()
        from euphorie.client import model
        from z3c.saconfig import Session
        Session.remove()
        model.metadata.drop_all(Session.bind)
