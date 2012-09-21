# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from s17.employee.testing import INTEGRATION_TESTING


class DemoTest(unittest.TestCase):
    """ Test Case for Demo profile.
    """

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        self.portal = self.layer['portal']
        self.pm = getattr(self.portal, 'portal_membership')
        self.setUpUser()

    def test_employees_item(self):
        """ Check that all the items are created.
        """
        folder = self.portal['employees']
        self.assertEquals(len(folder.keys()), 5)
        self.assertEquals(len(self.pm.listMemberIds()) - 1, 5)
