from plone.app.upgrade.v52 import final


# from z3c.saconfig.utility import SESSION_DEFAULTS


# TODO There should be nicer ways via zcml to do this,
# but for now this gets the job done, so we can test with it.
# SESSION_DEFAULTS["autoflush"] = False
# print("WARNING: patched z3c.saconfig to NOT autoflush.")


def rebuild_redirections(context):
    """For Euphorie does not have the registration tool (look for the
    disableRedirectTracking setuphandler), so we must skip this upgrade.

    This patch can be removed after the upgrade to Plone 5.2 is not
    needed anymore
    """
    pass


final.rebuild_redirections = rebuild_redirections
