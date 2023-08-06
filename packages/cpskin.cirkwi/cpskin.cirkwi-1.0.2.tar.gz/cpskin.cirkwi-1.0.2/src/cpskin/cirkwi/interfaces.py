# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.supermodel import model
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from cpskin.cirkwi import _


class ICpskinCirkwiLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICirkwi(model.Schema):
    """Marker interface that defines cirkwi."""

    cdf_host = schema.TextLine(
        title=_(u"cdf_host"),
        required=True,
    )

    cdf_outils = schema.TextLine(
        title=_(u"cdf_outils"),
        required=True,
    )

    cdf_lang = schema.TextLine(
        title=_(u"cdf_lang"),
        required=False,
    )
