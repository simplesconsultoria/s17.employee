# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility, getUtility
from zope.app.intid.interfaces import IIntIds

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.content.interfaces import INameFromTitle
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

from z3c.relationfield.relation import RelationValue

from s17.person.behaviors.contact import IContactInfo

from s17.employee.content.employee import IEmployee

from s17.employee.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Member'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        login(self.portal, TEST_USER_NAME)

    def test_create_member(self):
        # We check when the behavior is enabled
        pm = getToolByName(self.portal, 'portal_membership')
        self.folder.invokeFactory('s17.employee', 'somebody-someone',
                                   given_name='Somebody', surname='Someone')
        e1 = self.folder['somebody-someone']
        e1.reindexObject()
        user = pm.getMemberById('somebody-someone')
        self.assertEqual(user.getId(), e1.getId())

    def test_not_create_member(self):
        # We check when the behavior is disabled
        pm = getToolByName(self.portal, 'portal_membership')
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        behaviors = []
        behaviors.append(IReferenceable.__identifier__)
        behaviors.append(INameFromTitle.__identifier__)
        fti.behaviors = tuple(behaviors)
        self.folder.invokeFactory('s17.employee', 'somebody-someone',
                                   given_name='Somebody', surname='Someone')
        e1 = self.folder['somebody-someone']
        e1.reindexObject()
        user = pm.getMemberById('somebody-someone')
        self.assertEqual(None, user)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
