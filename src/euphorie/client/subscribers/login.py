from datetime import datetime
from euphorie.client.model import Account
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from zope.component import adapter


@adapter(Account, IUserLoggedInEvent)
def record_last_login(account, event=None):
    account.last_login = datetime.now()
