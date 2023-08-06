# -*- coding: utf-8 -*-
from Products.MemcachedManager.MemcachedManager import manage_addMemcachedManager

CACHEAUTHID = "MemcachedAuth"


def post_install(context):
    """Post install script"""
    if context.readDataFile("cpskincaching_default.txt") is None:
        return
    portal = context.getSite()
    setupMemcachedManager(portal)


def setupMemcachedManager(portal):
    if CACHEAUTHID not in portal.objectIds():
        manage_addMemcachedManager(portal, CACHEAUTHID)
    cacheMgr = getattr(portal, CACHEAUTHID)
    settings = {
        "request_vars": ["AUTHENTICATED_USER"],
        "servers": ("172.17.0.1:11211",),
        "mirrors": (),
        "max_age": 900,
        "debug": 0,
    }
    cacheMgr.manage_editProps("Memcached caching for auth", settings)
