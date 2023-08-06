#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import urlparse

from cpskin.caching.interfaces import ICpskinCachingLayer
from plone.cachepurging.interfaces import ICachePurgingSettings, IPurgePathRewriter
from plone.registry.interfaces import IRegistry
from zope.component import adapts, queryUtility
from zope.interface import implements


class CPSkinRewriter(object):
    """Default rewriter, which is aware of virtual hosting and minisites
    """

    implements(IPurgePathRewriter)
    adapts(ICpskinCachingLayer)

    def __init__(self, request):
        self.request = request

    def set_protocol_on_domain(self, domain):
        portSchemeMap = {"http": 80, "https": 443, "80": "http", "443": "https"}
        parsedDomain = re.search(
            "(?:(?P<scheme>http?|https?)://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*",
            domain,
        )
        if parsedDomain is not None:
            parsedDomain = parsedDomain.groupdict()
        else:
            raise ValueError("Unable to parse domain: {}".format(domain))
        currentScheme = parsedDomain.get("scheme")
        if not currentScheme and parsedDomain.get("port"):
            currentScheme = portSchemeMap[parsedDomain.get("port")]
        if not currentScheme:
            currentScheme = urlparse.urlparse(self.request.URL).scheme
        hostname = parsedDomain.get("host")
        if hostname is None:
            hostname = domain
        return "%s://%s:%s" % (currentScheme, hostname, portSchemeMap[currentScheme])

    def __call__(self, path):
        request = self.request
        # No rewriting necessary
        virtualURL = request.get("VIRTUAL_URL", None)
        if virtualURL is None:
            return [path]

        registry = queryUtility(IRegistry)
        if registry is None:
            return [path]

        settings = registry.forInterface(ICachePurgingSettings, check=False)

        virtualHosting = settings.virtualHosting

        # We don't want to rewrite
        if not virtualHosting:
            return [path]

        # We need to reconstruct VHM URLs for each of the domains
        virtualUrlParts = request.get("VIRTUAL_URL_PARTS")
        virtualRootPhysicalPath = request.get("VirtualRootPhysicalPath")
        # Make sure request is compliant
        if (
            not virtualUrlParts
            or not virtualRootPhysicalPath
            or not isinstance(virtualUrlParts, (list, tuple))
            or not isinstance(virtualRootPhysicalPath, (list, tuple))
            or len(virtualUrlParts) < 2
            or len(virtualUrlParts) > 3
        ):
            return [path]

        def get_env_domains():
            domains = os.environ.get("DOMAINS")
            if domains:
                return domains.split(" ")
            else:
                return []

        environ_domains = set(get_env_domains())
        registry_domains = set(settings.domains)
        domains = environ_domains.union(registry_domains)
        if not domains:
            domains = set([virtualUrlParts[0]])

        # Minisites
        minisite = request.get("cpskin_minisite", None)
        if minisite and minisite.is_minisite:
            domains.add(request.cpskin_minisite.minisite_url)

        # Virtual root, e.g. /Plone. Clear if we don't have any virtual root
        virtualRoot = "/".join(virtualRootPhysicalPath)
        if virtualRoot == "/":
            virtualRoot = ""

        # Prefix, e.g. /_vh_foo/_vh_bar. Clear if we don't have any.
        pathPrefix = len(virtualUrlParts) == 3 and virtualUrlParts[1] or ""
        if pathPrefix:
            pathPrefix = "/" + "/".join(["_vh_%s" % p for p in pathPrefix.split("/")])

        # Path, e.g. /front-page
        if not path.startswith("/"):
            path = "/" + path

        paths = []
        for domain in domains:
            domain = self.set_protocol_on_domain(domain)
            scheme, host = urlparse.urlparse(domain)[:2]
            paths.append(
                "/VirtualHostBase/%(scheme)s/%(host)s%(root)s/VirtualHostRoot%(prefix)s%(path)s"
                % {
                    "scheme": scheme,
                    "host": host,
                    "root": virtualRoot,
                    "prefix": pathPrefix,
                    "path": path,
                }
            )
        return paths
