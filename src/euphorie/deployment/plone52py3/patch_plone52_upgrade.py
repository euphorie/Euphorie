# coding=utf-8
from plone.app.upgrade.v52 import final


def rebuild_redirections(context):
    """For some strange reason, Euphorie does not know about the redirection
    storage. Don't attempt to rebuild it"""
    pass

final.rebuild_redirections = rebuild_redirections
