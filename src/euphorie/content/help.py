"""
Help
----

A Help document with multiple rich text fields.

https://admin.oiraproject.eu/documents/en/help

portal_type: euphorie.help
"""

from five import grok
from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from htmllaundry.z3cform import HtmlText
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from .. import MessageFactory as _
from euphorie.content.utils import StripMarkup
from plone.indexer import indexer

grok.templatedir("templates")


class IOnlineHelp(form.Schema):
    introduction = HtmlText(
            title=_("label_help_introduction", default=u"Introduction"),
            description=_("help_help_introduction",
                default=u"General information on risk assessment"),
            required=True)
    form.widget(introduction=WysiwygFieldWidget)

    authentication = HtmlText(
            title=_("label_help_authentication", default=u"Registration"),
            description=_("help_authentication",
                default=u"This text should explain how to register and login."),
            required=True)
    form.widget(authentication=WysiwygFieldWidget)

    sessions = HtmlText(
            title=_("label_help_sessions", default=u"Carrying out your risk assessment"),
            description=_("help_sessions",
                default=u"This text should describe the main functions of the OiRA Tool."),
            required=True)
    form.widget(sessions=WysiwygFieldWidget)

    preparation = HtmlText(
            title=_("label_help_preparation", default=u"1. Preparation"),
            description=_("help_preparation",
                default=u"This text should explain the 2 types of profile questions."),
            required=True)
    form.widget(preparation=WysiwygFieldWidget)

    identification = HtmlText(
            title=_("label_help_identification", default=u"2. Identification"),
            description=_("help_identification",
                default=u"This text should explain how the risk identification works."),
            required=True)
    form.widget(identification=WysiwygFieldWidget)

    evaluation = HtmlText(
            title=_("label_help_evaluation", default=u"3. Evaluation"),
            description=_("help_evaluation",
                default=u"This text should explain how to evaluate the identified risks."),
            required=True)
    form.widget(evaluation=WysiwygFieldWidget)

    actionplan = HtmlText(
            title=_("label_help_actionplan", default=u"4. Action Plan"),
            description=_("help_actionplan",
                default=u"This text should explain how to fill in the Action plan."),
            required=True)
    form.widget(actionplan=WysiwygFieldWidget)

    report = HtmlText(
            title=_("label_help_reports", default=u"5. Report"),
            description=_("help_reports",
                default=u"This text should describe how the report can either be saved or printed."),
            required=True)
    form.widget(report=WysiwygFieldWidget)

    finalwords = HtmlText(
            title=_("label_help_finalwords", default=u"What happens next?"),
            description=_("help_finalwords",
                default=u"General final recommendations."),
            required=True)
    form.widget(finalwords=WysiwygFieldWidget)


class View(grok.View):
    """ View name: @@nuplone-view
    """
    grok.context(IOnlineHelp)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("help_view")


@indexer(IOnlineHelp)
def SearchableTextIndexer(obj):
    """ Index the introduction, authentication, sessions, identification,
    evaluation, actionplan, report and finalwords.
    """
    return " ".join([StripMarkup(obj.introduction),
                     StripMarkup(obj.authentication),
                     StripMarkup(obj.sessions),
                     StripMarkup(obj.identification),
                     StripMarkup(obj.evaluation),
                     StripMarkup(obj.actionplan),
                     StripMarkup(obj.report),
                     StripMarkup(obj.finalwords)])
