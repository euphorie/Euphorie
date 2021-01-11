# -*- coding: UTF-8 -*-
from euphorie.client import MessageFactory as _
from euphorie.client.browser.publish import EnableCustomRisks
from euphorie.client.country import IClientCountry
from euphorie.client.sector import IClientSector
from plone import api

import datetime
import logging


log = logging.getLogger(__name__)


def update_custom_risks_module_texts(context):
    """ """
    if not api.portal.get_registry_record("euphorie.allow_user_defined_risks"):
        log.warning(
            "Custom risks are not enabled. Set 'allow_user_defined_risks' to "
            "true in euphorie.ini for enabling them."
        )
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
                        custom = getattr(survey, "custom-risks", None)
                        if custom:
                            custom.question = _(
                                u"question_other_risks",
                                default=(
                                    u"<p><strong>Important:</strong> In "
                                    u"order to avoid duplicating risks, "
                                    u"we strongly recommend you "
                                    u"to go first through all the previous modules, "
                                    u"if you have not done it yet.</p>"
                                    u"<p>If you don't need to add risks, "
                                    u"please continue.</p>"
                                ),
                            )
                        if is_new:
                            survey.published = (
                                survey.id,
                                survey.title,
                                datetime.datetime.now(),
                            )
