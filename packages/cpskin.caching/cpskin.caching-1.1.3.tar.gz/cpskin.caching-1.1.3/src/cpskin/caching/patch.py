# -*- coding: utf-8 -*-
from plone.cachepurging import utils
from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility


def isCachePurgingEnabled(registry=None):
    """
    we redefine this function because we don't want to check if there are
    cachingProxies in the registry
    """
    if registry is None:
        registry = queryUtility(IRegistry)
    if registry is None:
        return False
    settings = registry.forInterface(ICachePurgingSettings, check=False)
    return settings.enabled


utils.isCachePurgingEnabled = isCachePurgingEnabled
