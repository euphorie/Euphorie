"""
Maximum depth
-------------

It is not desirable for a survey to have too many layers. This results in 
a too complex user interface and overly complex survey structure. To prevent
this we limit the depth in a survey at 3 levels.

Unfortunately neither Plone nor CMF provide a way to restrict the depth. This
implementation uses the :obj:`euphorie.content.fti.IConstructionFilter` hook
to add a new condition on object creation.

It is used by for `euphorie.module` and `euphorie.risk` by registeringn the
:obj:`SurveyDepthConstructionFilter` adapter for those portal types.
"""
from Acquisition import aq_inner
from Acquisition import aq_chain
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from euphorie.content.fti import IConstructionFilter
from euphorie.content.fti import ConditionalDexterityFTI
from euphorie.content.survey import ISurvey

class SurveyDepthConstructionFilter(object):
    """Object creation filter.

    This filter tests creation of a new object does not create to
    many levels in a survey. If the current context is not located
    in a :obj:`ISurvey` context no depth check is done.
    """

    adapts(ConditionalDexterityFTI, Interface)
    implements(IConstructionFilter)

    maxdepth = 3

    def __init__(self, fti, container):
        self.fti=fti
        self.container=container

    def allowed(self):
        depth=1
        for position in aq_chain(aq_inner(self.container)):
            if ISurvey.providedBy(position):
                break
            depth+=1
        else:
            return True

        return depth<=self.maxdepth


