# -*- coding: utf-8 -*-
from collective.sticky.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers
from collective.sticky.interfaces import IBrowserLayer
import unittest

PROJECTNAME = 'collective.sticky'


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_catalog_is_sticky(self):
        pass

    def test_querystring(self):
        pass

    def test_reinstall_with_changed_registry(self):
        ps = getattr(self.portal, 'portal_setup')
        try:
            ps.runAllImportStepsFromProfile('profile-collective.sticky:default')
        except AttributeError:
            self.fail('Reinstall fails when the record was changed')


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    def test_jcatalog_removed(self):
        pass

    def test_querystring_removed(self):
        pass
