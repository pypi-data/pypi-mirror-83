# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from cpskin.caching.patch import isCachePurgingEnabled
from cpskin.caching.testing import CPSKIN_CACHING_INTEGRATION_TESTING
from plone import api
from plone.app.testing import quickInstallProduct


class TestSetup(unittest.TestCase):
    """Test that cpskin.caching is properly installed."""

    layer = CPSKIN_CACHING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if cpskin.caching is installed."""
        self.assertTrue(self.installer.isProductInstalled("cpskin.caching"))

    def test_browserlayer(self):
        """Test that ICpskinCachingLayer is registered."""
        from cpskin.caching.interfaces import ICpskinCachingLayer
        from plone.browserlayer import utils

        self.assertIn(ICpskinCachingLayer, utils.registered_layers())

    def testReinstall(self):
        portal = self.layer["portal"]
        quickInstallProduct(portal, "kuleuven.caching")
        quickInstallProduct(portal, "kuleuven.caching")

    def testIsCachingEnabled(self):
        self.assertEqual(isCachePurgingEnabled(), True)
