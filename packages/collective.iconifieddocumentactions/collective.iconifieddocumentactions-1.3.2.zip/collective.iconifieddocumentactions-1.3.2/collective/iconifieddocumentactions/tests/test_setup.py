# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.iconifieddocumentactions.testing import INTEGRATION
from plone import api

import unittest2 as unittest


class TestInstall(unittest.TestCase):
    """Test installation of collective.iconifieddocumentactions into Plone."""
    layer = INTEGRATION

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.iconifieddocumentactions is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.iconifieddocumentactions'))

    def test_uninstall(self):
        """Test if collective.iconifieddocumentactions is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.iconifieddocumentactions'])
        self.assertFalse(self.installer.isProductInstalled('collective.iconifieddocumentactions'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveGeoLeafletLayer is registered."""
        from collective.iconifieddocumentactions.interfaces import ICollectiveGeoLeafletLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveGeoLeafletLayer, utils.registered_layers())
