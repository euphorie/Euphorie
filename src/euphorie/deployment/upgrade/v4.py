import logging
from Acquisition import aq_parent
from euphorie.client.api.entry import API


log = logging.getLogger(__name__)


def add_client_api(context):
    siteroot = aq_parent(context)
    client = siteroot.client
    if 'api' in client:
        log.info('Client API already configured.')
        return

    log.info('Enabling client API.')
    client['api'] = API('api')
