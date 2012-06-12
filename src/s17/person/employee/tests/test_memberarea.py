# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login

from s17.person.employee.testing import INTEGRATION_TESTING


class MemberAreaTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.membership = self.portal.portal_membership
        applyProfile(self.portal, 's17.person.employee:use_memberarea')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_creation(self):
        self.assertEqual(self.membership.getHomeFolder(), None)
        self.portal.logged_in()
        self.failIfEqual(self.membership.getHomeFolder(), None)
        home = self.membership.getHomeFolder()
        self.assertEqual(home.portal_type, 's17.employee')

    def test_areatitle(self):
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        self.assertEqual(home.given_name, 'test_user_1_')
        self.assertEqual(home.surname, '')
        self.assertEqual(home.fullname, 'test_user_1_ ')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
