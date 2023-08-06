#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

import zope.component.testing
from cpskin.caching.hooks import purge
from cpskin.caching.testing import CPSKIN_CACHING_INTEGRATION_TESTING  # noqa
from plone.cachepurging.interfaces import ICachePurgingSettings, IPurger
from plone.cachepurging.tests.test_hooks import FauxRequest
from plone.registry import Registry
from plone.registry.fieldfactory import persistentFieldAdapter
from plone.registry.interfaces import IRegistry
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable
from zope.component import provideAdapter, provideHandler, provideUtility
from zope.event import notify
from zope.interface import alsoProvides, implements
from ZPublisher.pubevents import PubSuccess


class TestPurgeHandler(unittest.TestCase):
    def setUp(self):
        provideAdapter(AttributeAnnotations)
        provideAdapter(persistentFieldAdapter)
        provideHandler(purge)

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_purge_no_config(self):
        request = FauxRequest()
        alsoProvides(request, IAttributeAnnotatable)

        IAnnotations(request)["plone.cachepurging.urls"] = set(["/foo", "/bar"])

        registry = Registry()
        registry.registerInterface(ICachePurgingSettings)
        provideUtility(registry, IRegistry)
        settings = registry.forInterface(ICachePurgingSettings)
        settings.enabled = True

        class FauxPurger(object):
            implements(IPurger)

            def __init__(self):
                self.purged = []

            def purgeAsync(self, url, httpVerb="PURGE"):
                self.purged.append(url)

        purger = FauxPurger()
        provideUtility(purger)

        notify(PubSuccess(request))

        self.assertEquals([], purger.purged)

    def test_purge_with_config(self):
        request = FauxRequest()
        alsoProvides(request, IAttributeAnnotatable)

        IAnnotations(request)["plone.cachepurging.urls"] = set(["/foo", "/bar"])

        registry = Registry()
        registry.registerInterface(ICachePurgingSettings)
        provideUtility(registry, IRegistry)

        settings = registry.forInterface(ICachePurgingSettings)
        settings.enabled = True

        class FauxPurger(object):
            implements(IPurger)

            def __init__(self):
                self.purged = []

            def purgeAsync(self, url, httpVerb="PURGE"):
                self.purged.append(url)

        purger = FauxPurger()
        provideUtility(purger)
        os.environ["CACHING_SERVERS"] = "http://localhost:1234 http://10.0.100.1:1235"
        notify(PubSuccess(request))

        self.assertEquals(
            [
                "http://localhost:1234/foo",
                "http://10.0.100.1:1235/foo",
                "http://localhost:1234/bar",
                "http://10.0.100.1:1235/bar",
            ],
            purger.purged,
        )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
