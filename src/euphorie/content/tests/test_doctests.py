import unittest
import glob
import os.path
from Testing.ZopeTestCase import FunctionalDocFileSuite
import doctest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase


def test_suite():
    location = os.path.dirname(__file__) or '.'
    doctests = ['stories/' + os.path.basename(test)
             for test in glob.glob(os.path.join(location, 'stories', '*.txt'))]

    options = doctest.REPORT_ONLY_FIRST_FAILURE | \
              doctest.ELLIPSIS | \
              doctest.NORMALIZE_WHITESPACE

    suites = [FunctionalDocFileSuite(test,
                        optionflags=options,
                        test_class=EuphorieFunctionalTestCase,
                        module_relative=True,
                        package='euphorie.content.tests',
                        encoding='utf-8')
               for test in doctests]
    return unittest.TestSuite(suites)
