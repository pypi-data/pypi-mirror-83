# -*- coding: utf-8 -*-
# from plone import api


def reload_registry_xml(context):
    # kid = 'plone.cachepurging.interfaces.ICachePurgingSettings.virtualHosting'
    # api.portal.set_registry_record(kid, True)
    context.runImportStepFromProfile(
        'profile-cpskin.caching:default', 'plone.app.registry')
