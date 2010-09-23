import binascii
import hmac
import logging
import rfc822
import time
from euphorie.client.utils import getRequest

log = logging.getLogger(__name__)


def _sign(secret, data):
    """Generate a signature for a bit of data. The signature can
    be used to authenticate data coming in from an untrustted source,
    such as a HTTP cookie.
    """
    return hmac.new(secret, data).digest()


def setCookie(secret, name, value, timeout=0):
    """Set a secure HTTP cookie. The cookie will be signed using :obj:`secret`.
    An expiration time for the cookie will be set if :obj:`timeout` is
    specified.
    """
    request=getRequest()
    signature=_sign(secret, str(value))
    cookie="%s%s" % (signature, value)
    cookie=binascii.b2a_base64(cookie).rstrip()
    if timeout:
        expires=rfc822.formatdate(time.time()+timeout)
        request.response.setCookie(name, cookie, path="/", expires=expires)
    else:
        request.response.setCookie(name, cookie, path="/")



def getCookie(secret, name):
    """Get a potentially secure HTTP cookie. This method decodes
    a cookie and returns a tuple with its signature and data. If no
    cookie is found or the cookie has an invalid signature None is
    returned instead.
    """
    request=getRequest()

    cookie=request.cookies.get(name)
    if not cookie:
        return None

    try:
        cookie=binascii.a2b_base64(cookie)
    except binascii.Error:
        log.warn("Cookie with invalid base64 encoding: %r", cookie)
        return None

    if len(cookie)<17:
        log.warn("Cookie is too short: %r", cookie)
        return None

    (signature,value)=(cookie[:16], cookie[16:])

    if signature!=hmac.new(secret, value).digest():
        log.warn("Cookie with invalid signature: %r %r", signature, value)
        return None

    return value


def deleteCookie(name):
    """Remove an existing cookie."""
    request=getRequest()
    request.response.expireCookie(name)


