"""

    Default user-agent sniffing information based on mobile.sniffer and wurlf products.

    Wurlf database is supplied with pywurlf package.

"""

__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

import logging

import zope.interface
from zope.annotation.interfaces import IAnnotations

logger = logging.getLogger("Plone")

try:
    from mobile.sniffer.wurlf.sniffer import WurlfSniffer

    # Wrapper sniffer instance
    # All start-up delay goes on this line
    _sniffer = WurlfSniffer()
except ImportError, e:
    logger.exception(e)
    logger.error("Could not import Wurlf sniffer... probably python-Lehvenstein egg missing")
    _sniffer = None

# Annotations cache key
KEY = "sniffer_user_agent"

def cached_wurlf_ua_sniffer(context, request):
    """ Resolve user-agent record for the request.

    User agent look-up may be expensive.
    Store cached value on the request object itself and
    session.

    @return: mobile.sniffer.base.UserAgent instance or None if no user agent found or it cannot be looked up
    """


    if _sniffer == None:
        # For some reason, coudln't initialize
        return None

    # First check if we have cached hit on HTTP request
    annotations = IAnnotations(request)
    ua = annotations.get(KEY, None)

    # Then check if we have cached hit on session
    if not ua:
        sdm = context.session_data_manager
        session = sdm.getSessionData(create=True)

        ua = session.get(KEY, None)

    if not ua:
        ua = _sniffer.sniff(request)

        # TODO: Session based caching is disabled for now,
        # as pywurfl objects are not pickable

        # Session set may start transaction
        # Is this too expensive?
        # session.set(KEY, ua)

    annotations[KEY] = ua

    return ua

