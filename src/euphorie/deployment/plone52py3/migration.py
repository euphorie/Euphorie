# coding=utf-8
from Products.Five import BrowserView
from plone.behavior.registration import lookup_behavior_registration
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

import logging
logger = logging.getLogger(__name__)


class Prepare(BrowserView):
    def __call__(self):
        ptt = api.portal.get_tool("portal_types")
        ftis = [fti for fti in ptt.objectValues() if IDexterityFTI.providedBy(fti)]
        for fti in ftis:
            bad_behaviors = []
            for behavior in fti.behaviors:
                try:
                    lookup_behavior_registration(behavior)
                except:
                    bad_behaviors.append(behavior)
            if bad_behaviors:
                behaviors = [x for x in fti.behaviors if x not in bad_behaviors]
                fti.behaviors = behaviors
                logger.info("Removed {} for FTI {}".format(bad_behaviors, fti.id))
        return "Finished preparations for v52 migration"
