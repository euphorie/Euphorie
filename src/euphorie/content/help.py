from five import grok
from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from htmllaundry.z3cform import HtmlText
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from euphorie.content import MessageFactory as _
from euphorie.content.utils import StripMarkup
from plone.indexer import indexer

grok.templatedir("templates")


class IOnlineHelp(form.Schema):
    introduction = HtmlText(
            title = _("label_help_introduction", default=u"Introduction"),
            description = _("help_help_introduction",
                default=u"Generic introduction for the client. This text "
                        u"is not associated with specific pages."),
            required = True)
    form.widget(introduction=WysiwygFieldWidget)
    
    authentication = HtmlText(
            title = _("label_authentication", default=u"Authentication"),
            description = _("help_authentication",
                default=u"Describe the user handling. This text is "
                        u"linked from the login, password reminder and "
                        u"registration pages."),
            required = True)
    form.widget(authentication=WysiwygFieldWidget)

    sessions = HtmlText(
            title = _("label_sessions", default=u"Sessions"),
            description = _("help_sessions",
                default=u"Describe the session handling. This text is "
                        u"linked from the session overview page."),
            required = True)
    form.widget(sessions=WysiwygFieldWidget)

    preparation = HtmlText(
            title = _("label_preparation", default=u"Preparation"),
            description = _("help_preparation",
                default=u"Document the first steps in a survey, including "
                        u"how to configure a profile (if needed). This "
                        u"page is linked from the survey start page."),
            required = True)
    form.widget(preparation=WysiwygFieldWidget)

    identification = HtmlText(
            title = _("label_identification", default=u"Identification"),
            description = _("help_identification",
                default=u"Document the identification phase. This information "
                        u"is linked from all identification related pages"),
            required = True)
    form.widget(identification=WysiwygFieldWidget)

    evaluation = HtmlText(
            title = _("label_evaluation", default=u"Evaluation"),
            description = _("help_evaluation",
                default=u"Document the evaluation phase. This information "
                        u"is linked from all evaluation related pages"),
            required = True)
    form.widget(evaluation=WysiwygFieldWidget)

    actionplan = HtmlText(
            title = _("label_actionplan", default=u"Action plan"),
            description = _("help_actionplan",
                default=u"Document the action plan phase. This information "
                        u"is linked from all action plan related pages"),
            required = True)
    form.widget(actionplan=WysiwygFieldWidget)

    report = HtmlText(
            title = _("label_reports", default=u"Reports"),
            description = _("help_reports",
                default=u"Describe the reporting options. This page is "
                        u"linked from report page."),
            required = True)
    form.widget(report=WysiwygFieldWidget)

    finalwords = HtmlText(
            title = _("label_finalwords", default=u"Final words"),
            description = _("help_finalwords",
                default=u"Any final words that should be shown at the end "
                        u"of the help. This information is not linked "
                        u"directly."),
            required = True)
    form.widget(finalwords=WysiwygFieldWidget)



class View(grok.View):
    grok.context(IOnlineHelp)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("help_view")



@indexer(IOnlineHelp)
def SearchableTextIndexer(obj):
    return " ".join([StripMarkup(obj.introduction),
                     StripMarkup(obj.authentication),
                     StripMarkup(obj.sessions),
                     StripMarkup(obj.identification),
                     StripMarkup(obj.evaluation),
                     StripMarkup(obj.actionplan),
                     StripMarkup(obj.report),
                     StripMarkup(obj.finalwords)])

