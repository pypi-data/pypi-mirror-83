# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cpskin.cirkwi.testing import CPSKIN_CIRKWI_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that cpskin.cirkwi is properly installed."""

    layer = CPSKIN_CIRKWI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cpskin.cirkwi is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cpskin.cirkwi'))

    def test_browserlayer(self):
        """Test that ICpskinCirkwiLayer is registered."""
        from cpskin.cirkwi.interfaces import (
            ICpskinCirkwiLayer)
        from plone.browserlayer import utils
        self.assertIn(ICpskinCirkwiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CPSKIN_CIRKWI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cpskin.cirkwi'])

    def test_product_uninstalled(self):
        """Test if cpskin.cirkwi is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cpskin.cirkwi'))
