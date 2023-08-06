#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from cpskin.caching.interfaces import ICpskinCachingLayer
from cpskin.caching.rewrite import CPSkinRewriter
from cpskin.caching.testing import CPSKIN_CACHING_INTEGRATION_TESTING
from cpskin.minisite.minisite import MinisiteConfig, decorateRequest
from plone.app.testing import TEST_USER_ID, setRoles
from zope.interface import directlyProvides


class TestCpskinRewriter(unittest.TestCase):
    layer = CPSKIN_CACHING_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.app.REQUEST
        directlyProvides(self.request, ICpskinCachingLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.request = self.app.REQUEST
        self._prepareVHMRequest("/")
        self.rewriter = CPSkinRewriter(self.request)

    def tearDown(self):
        if os.environ.get("DOMAINS"):
            del os.environ["DOMAINS"]

    def _prepareVHMRequest(
        self, path, domain="imio.be", root="/plone", prefix="", protocol="http"
    ):
        translatedPrefix = "/".join(["_vh_%s" % p for p in prefix.split("/")])

        self.request["URL"] = "%s://%s%s%s" % (protocol, domain, prefix, path)
        self.request["ACTUAL_URL"] = "%s://%s%s%s" % (protocol, domain, prefix, path)
        self.request["SERVER_URL"] = "%s://%s" % (protocol, domain)
        self.request["PATH_INFO"] = (
            "/VirtualHostBase/%s/%s:80%s/VirtualHostRoot%s%s"
            % (protocol, domain, root, translatedPrefix, path)
        )
        self.request["VIRTUAL_URL"] = "%s://%s%s" % (protocol, domain, path)

        if prefix:
            self.request["VIRTUAL_URL_PARTS"] = (
                "%s://%s" % (protocol, domain),
                prefix[1:],
                path[1:],
            )
        else:
            self.request["VIRTUAL_URL_PARTS"] = (
                "%s://%s" % (protocol, domain),
                path[1:],
            )

        self.request["VirtualRootPhysicalPath"] = tuple(root.split("/"))

    def test_purge_paths_no_minisite(self):
        self.assertEqual(
            self.rewriter("/foo"),
            ["/VirtualHostBase/http/imio.be:80/plone/VirtualHostRoot/foo"],
        )

    def test_purge_paths_with_domains_no_minisite(self):
        os.environ["DOMAINS"] = "https://communesplone.be http://imio.be"
        self.assertListEqual(
            self.rewriter("/foo"),
            [
                "/VirtualHostBase/https/communesplone.be:443/plone/VirtualHostRoot/foo",
                "/VirtualHostBase/http/imio.be:80/plone/VirtualHostRoot/foo",
            ],
        )

    def test_purge_paths_with_minisite(self):
        minisite = MinisiteConfig(
            main_portal_url="http://localhost",
            minisite_url="https://loisirs.imio.be",
            search_path="/plone/test_minisite",
            filename="minisite_config.txt",
        )
        decorateRequest(self.request, minisite)
        self.assertListEqual(
            self.rewriter("/foo"),
            [
                "/VirtualHostBase/https/loisirs.imio.be:443/plone/VirtualHostRoot/foo",
                "/VirtualHostBase/http/imio.be:80/plone/VirtualHostRoot/foo",
            ],
        )

    def test_set_protocol_on_domain(self):
        self.assertEqual(
            self.rewriter.set_protocol_on_domain("imio.be"), "http://imio.be:80"
        )
        self.assertEqual(
            self.rewriter.set_protocol_on_domain("imio.be:443"), "https://imio.be:443"
        )
        self._prepareVHMRequest("/", protocol="https")
        self.assertEqual(
            self.rewriter.set_protocol_on_domain("bla.imio.be"),
            "https://bla.imio.be:443",
        )
        self._prepareVHMRequest("/", protocol="http")
        self.assertEqual(
            self.rewriter.set_protocol_on_domain("https://communesplone.be"),
            "https://communesplone.be:443",
        )
        self.assertEqual(
            self.rewriter.set_protocol_on_domain("https://bla.imio.be"),
            "https://bla.imio.be:443",
        )

    def test_raise_parsing_domain(self):
        with self.assertRaises(ValueError):
            self.rewriter.set_protocol_on_domain("")
