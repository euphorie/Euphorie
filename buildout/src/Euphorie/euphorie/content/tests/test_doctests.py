import unittest
import glob
import os.path
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from euphorie.content.tests.functional import EuphorieContentFunctionalTestCase


def test_suite():
    location=os.path.dirname(__file__) or "."
    doctests=["stories/"+os.path.basename(test)
             for test in glob.glob(os.path.join(location, "stories", "*.txt"))]

    options=doctest.REPORT_ONLY_FIRST_FAILURE | \
            doctest.ELLIPSIS | \
            doctest.NORMALIZE_WHITESPACE

    suites=[FunctionalDocFileSuite(test,
                                   optionflags=options,
                                   test_class=EuphorieContentFunctionalTestCase,
                                   module_relative=True,
                                   package="euphorie.content.tests")
            for test in doctests]
    return unittest.TestSuite(suites)

