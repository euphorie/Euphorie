import unittest
from euphorie.content.risk import Risk
from euphorie.client import model

class ShowNegateWarningTests(unittest.TestCase):
    def _call(self, node, zodbnode):
        from euphorie.client.report import IdentificationReport
        report=IdentificationReport(None, None)
        return report.show_negate_warning(node, zodbnode)

    def test_show_Unanswered(self):
        # https//code.simplon.biz/tracker/tno-euphorie/ticket/75
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_RiskNotPresent(self):
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk", identification="yes")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_RiskNotApplicable(self):
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk", identification="n/a")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_Present(self):
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), True)

    def test_HasProblemDescription(self):
        zodbnode=Risk()
        zodbnode.problem_description=u"Negative"
        node=model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_HasEmptyProblemDescription(self):
        zodbnode=Risk()
        zodbnode.problem_description=u"   "
        node=model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), True)

