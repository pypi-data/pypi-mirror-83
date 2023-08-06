# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.printrss.testing import COLLECTIVE_PRINTRSS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.printrss is properly installed."""

    layer = COLLECTIVE_PRINTRSS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.printrss is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.printrss'))

    def test_browserlayer(self):
        """Test that ICollectivePrintrssLayer is registered."""
        from collective.printrss.interfaces import (
            ICollectivePrintrssLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectivePrintrssLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PRINTRSS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.printrss'])

    def test_product_uninstalled(self):
        """Test if collective.printrss is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.printrss'))
