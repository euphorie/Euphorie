from euphorie.testing import EUPHORIE_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import glob
import os.path
import unittest


def test_suite():
    location = os.path.dirname(__file__) or "."
    doctests = [
        "stories/" + os.path.basename(test)
        for test in glob.glob(os.path.join(location, "stories", "*.txt"))
    ]

    options = (
        doctest.REPORT_ONLY_FIRST_FAILURE
        | doctest.ELLIPSIS
        | doctest.NORMALIZE_WHITESPACE
    )

    suites = [
        layered(
            doctest.DocFileSuite(
                test,
                optionflags=options,
                module_relative=True,
                package="euphorie.content.tests",
                encoding="utf-8",
            ),
            layer=EUPHORIE_FUNCTIONAL_TESTING,
        )
        for test in doctests
    ]
    return unittest.TestSuite(suites)
