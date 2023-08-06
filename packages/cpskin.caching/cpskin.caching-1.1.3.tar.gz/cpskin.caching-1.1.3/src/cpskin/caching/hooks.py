# -*- coding: utf-8 -*-
import logging
import os

from cpskin.caching.patch import isCachePurgingEnabled
from plone.cachepurging.hooks import KEY
from plone.cachepurging.interfaces import IPurger
from plone.cachepurging.utils import getURLsToPurge
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter, queryUtility
from ZPublisher.interfaces import IPubSuccess

logger = logging.getLogger("cpskin.caching")


@adapter(IPubSuccess)
def purge(event):
    """
    Sends Purge requests based to proxies based on configuration
    defined in environment variables
    Code based on plone.cachepuring.hooks
    """
    request = event.request

    annotations = IAnnotations(request, None)
    if annotations is None:
        return

    paths = annotations.get(KEY, None)
    if paths is None:
        return

    registry = queryUtility(IRegistry)
    if registry is None:
        return

    if not isCachePurgingEnabled(registry=registry):
        return

    purger = queryUtility(IPurger)
    if purger is None:
        return

    proxies_url = getCachingConfiguration()
    if proxies_url:
        proxies_url = proxies_url.split(" ")
    else:
        return

    for path in paths:
        for url in getURLsToPurge(path, proxies_url):
            logger.debug("purging " + url)
            purger.purgeAsync(url)


def getCachingConfiguration():
    caching_servers = os.environ.get("CACHING_SERVERS", None)
    return caching_servers
