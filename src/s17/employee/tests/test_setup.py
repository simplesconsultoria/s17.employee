# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.site.hooks import setSite

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from s17.employee.testing import INTEGRATION_TESTING

PROJECTNAME = 's17.employee'


class InstallTestCase(unittest.TestCase):
    """ensure product is properly installed"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        "%s not installed" % PROJECTNAME)

    def test_dependencies_installed(self):
        self.assertTrue(self.qi.isProductInstalled('s17.person'),
                        "s17.person dependency not installed")

    def test_catalog_installed(self):
        self.assertTrue('portal_personcatalog' in self.portal.objectIds(),
                        "Catalog not installed")


class UninstallTestCase(unittest.TestCase):
    """ensure product is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))
