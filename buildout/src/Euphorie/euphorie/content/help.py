from zope.interface import implements
from plone.directives import dexterity
from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from htmllaundry.z3cform import HtmlText
from euphorie.content import MessageFactory as _


class IOnlineHelp(form.Schema):
    introduction = HtmlText(
            title = _(u"Introduction"),
            description = _(u"Generic introduction for the client. This text "
                            u"is not associated with specific pages."),
            required = True)
    form.widget(introduction=WysiwygFieldWidget)
    
    authentication = HtmlText(
            title = _(u"Authentication"),
            description = _(u"Describe the user handling. This text is "
                            u"linked from the login, password reminder and "
                            u"registration pages."),
            required = True)
    form.widget(authentication=WysiwygFieldWidget)

    sessions = HtmlText(
            title = _(u"Sessions"),
            description = _(u"Describe the session handling. This text is "
                            u"linked from the session overview page."),
            required = True)
    form.widget(sessions=WysiwygFieldWidget)

    preparation = HtmlText(
            title = _(u"Preparation"),
            description = _(u"Document the first steps in a survey, including "
                            u"how to configure a profile (if needed). This "
                            u"page is linked from the survey start page."),
            required = True)
    form.widget(preparation=WysiwygFieldWidget)

    identification = HtmlText(
            title = _(u"Identification"),
            description = _(u"Document the identification phase. This information "
                            u"is linked from all identification related pages"),
            required = True)
    form.widget(identification=WysiwygFieldWidget)

    evaluation = HtmlText(
            title = _(u"Evaluation"),
            description = _(u"Document the evaluation phase. This information "
                            u"is linked from all evaluation related pages"),
            required = True)
    form.widget(evaluation=WysiwygFieldWidget)

    actionplan = HtmlText(
            title = _(u"Action plan"),
            description = _(u"Document the action plan phase. This information "
                            u"is linked from all action plan related pages"),
            required = True)
    form.widget(actionplan=WysiwygFieldWidget)

    report = HtmlText(
            title = _(u"Reports"),
            description = _(u"Describe the reporting options. This page is "
                            u"linked from report page."),
            required = True)
    form.widget(report=WysiwygFieldWidget)

    finalwords = HtmlText(
            title = _(u"Final words"),
            description = _(u"Any final words that should be shown at the end "
                            u"of the help. This information is not linked "
                            u"directly."),
            required = True)
    form.widget(finalwords=WysiwygFieldWidget)



class OnlineHelp(dexterity.Item):
    implements(IOnlineHelp)

    id = "help"
    title = _(u"Help")
    description = u""

