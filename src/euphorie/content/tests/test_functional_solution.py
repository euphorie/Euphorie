from euphorie.content import utils
from euphorie.content.solution import Solution
from euphorie.testing import EuphorieIntegrationTestCase
from zope.component.hooks import getSite
from zope.i18n import translate


def _create(container, *args, **kwargs):
    newid = container.invokeFactory(*args, **kwargs)
    return getattr(container, newid)


def createSolution(algorithm=u'kinney'):
    portal = getSite()
    country = portal.sectors.nl
    sector = _create(country, "euphorie.sector", "sector")
    surveygroup = _create(
        sector,
        "euphorie.surveygroup",
        "group",
        evaluation_algorithm=algorithm
    )
    survey = _create(surveygroup, "euphorie.survey", "survey")
    module = _create(survey, "euphorie.module", "module")
    risk = _create(module, "euphorie.risk", "risk")
    solution = _create(risk, "euphorie.solution", "solution")
    return solution


class RiskTests(EuphorieIntegrationTestCase):

    def testNotGloballyAllowed(self):
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.solution" not in types)

    def testCanBeCopied(self):
        solution = createSolution()
        self.assertTrue(solution.cb_isCopyable())

    def testCMFAccessors(self):
        """ CMF-Style accessors must return utf8-encoded strings.
        """
        self.loginAsPortalOwner()
        solution = createSolution()
        title = solution.Title()
        self.assertEqual(type(title), str)
        survey = utils.getSurvey(solution)
        self.assertEqual(
            title, translate(Solution.title, target_language=survey.language)
        )
