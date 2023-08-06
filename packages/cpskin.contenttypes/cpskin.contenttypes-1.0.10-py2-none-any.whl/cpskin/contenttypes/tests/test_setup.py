# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from cpskin.contenttypes.testing import CPSKIN_CONTENTTYPES_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that cpskin.contenttypes is properly installed."""

    layer = CPSKIN_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cpskin.contenttypes is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cpskin.contenttypes'))

    def test_browserlayer(self):
        """Test that ICpskinContenttypesLayer is registered."""
        from cpskin.contenttypes.interfaces import (
            ICpskinContenttypesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICpskinContenttypesLayer,
            utils.registered_layers())
