from zope.deferredimport import deprecated


deprecated(
    (
        "It will be removed in future versions. "
        "Please use the regular image widget instead."
    ),
    LogoWidget="euphorie.content.widgets.logo_bbb:LogoWidget",
    LogoFieldWidget="euphorie.content.widgets.logo_bbb:LogoFieldWidget",
)
