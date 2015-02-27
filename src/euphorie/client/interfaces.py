from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client.
    """


class IIdentificationPhaseSkinLayer(Interface):
    """Skin layer used during the identification phase."""


class ICustomizationPhaseSkinLayer(Interface):
    """Skin layer used during the evaluation phase."""


class IEvaluationPhaseSkinLayer(Interface):
    """Skin layer used during the evaluation phase."""


class IActionPlanPhaseSkinLayer(Interface):
    """Skin layer used during the action plan phase."""


class IReportPhaseSkinLayer(Interface):
    """Skin layer used during the action plan phase."""
