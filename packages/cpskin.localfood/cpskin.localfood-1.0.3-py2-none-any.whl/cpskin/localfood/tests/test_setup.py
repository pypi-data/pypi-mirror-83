# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from cpskin.localfood.testing import CPSKIN_LOCALFOOD_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that cpskin.localfood is properly installed."""

    layer = CPSKIN_LOCALFOOD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cpskin.localfood is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cpskin.localfood'))

    def test_browserlayer(self):
        """Test that ICpskinLocalfoodLayer is registered."""
        from cpskin.localfood.interfaces import (
            ICpskinLocalfoodLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICpskinLocalfoodLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CPSKIN_LOCALFOOD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cpskin.localfood'])

    def test_product_uninstalled(self):
        """Test if cpskin.localfood is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cpskin.localfood'))

    def test_browserlayer_removed(self):
        """Test that ICpskinLocalfoodLayer is removed."""
        from cpskin.localfood.interfaces import \
            ICpskinLocalfoodLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ICpskinLocalfoodLayer,
           utils.registered_layers())
