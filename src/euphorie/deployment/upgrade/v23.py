# -*- coding: UTF-8 -*-
from euphorie.client import MessageFactory as _
from euphorie.client.country import IClientCountry
from euphorie.client.publish import EnableCustomRisks
from euphorie.client.sector import IClientSector
from plone import api
from z3c.appconfig.interfaces import IAppConfig
from z3c.appconfig.utils import asBool
import logging
import zope.component
import datetime

log = logging.getLogger(__name__)


def update_custom_risks_module_texts(context):
    """ """
    appconfig = zope.component.getUtility(IAppConfig)
    if not asBool(appconfig["euphorie"].get("allow_user_defined_risks")):
        log.warning(
            "Custom risks are not enabled. Set 'allow_user_defined_risks' to "
            "true in euphorie.ini for enabling them.")
        return
    portal = api.portal.get()
    client = portal.client
    count = 0
    for country in client.objectValues():
        if IClientCountry.providedBy(country):
            for sector in country.objectValues():
                if IClientSector.providedBy(sector):
                    for survey in sector.objectValues():

                        is_new = EnableCustomRisks(survey)
                        count += 1
                        custom = getattr(survey, 'custom-risks', None)
                        if custom:
                            # custom.title = _(u'title_other_risks', default=u"Added risks (by you)")
                            # custom.description = _(
                            #     u"description_other_risks",
                            #     default=u"In case you have identified risks not included in "
                            #     u"the tool, you are able to add them now:")
                            custom.question = _(
                                u"question_other_risks",
                                default=u"<p><strong>Important:</strong> In "
                                u"order to avoid duplicating risks, we strongly recommend you "
                                u"to go first through all the previous modules, if you have not "
                                u"done it yet.</p><p>If you don't need to add risks, please continue.</p>")
                        if is_new:
                            survey.published = (
                                survey.id, survey.title, datetime.datetime.now())
                        # except Exception as e:
                        #     log.error("Could not enable custom risks for module. %s" % e)
