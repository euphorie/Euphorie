from plone.app.upgrade.v52 import final


def rebuild_redirections(context):
    """For Euphorie does not have the registration tool (look for the
    disableRedirectTracking setuphandler), so we must skip this upgrade.

    This patch can be removed after the upgrade to Plone 5.2 is not
    needed anymore
    """
    pass


final.rebuild_redirections = rebuild_redirections
