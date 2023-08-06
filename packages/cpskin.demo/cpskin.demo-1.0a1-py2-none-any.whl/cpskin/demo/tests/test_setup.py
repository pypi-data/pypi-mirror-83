# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cpskin.demo.testing import CPSKIN_DEMO_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that cpskin.demo is properly installed."""

    layer = CPSKIN_DEMO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cpskin.demo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cpskin.demo'))

    def test_browserlayer(self):
        """Test that ICpskinDemoLayer is registered."""
        from cpskin.demo.interfaces import (
            ICpskinDemoLayer)
        from plone.browserlayer import utils
        self.assertIn(ICpskinDemoLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CPSKIN_DEMO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cpskin.demo'])

    def test_product_uninstalled(self):
        """Test if cpskin.demo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cpskin.demo'))
