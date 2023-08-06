# -*- coding: utf-8 -*-
"""Init and utils."""

from cpskin.caching import patch
from zope.i18nmessageid import MessageFactory

patch  # flake8
_ = MessageFactory("cpskin.caching")
