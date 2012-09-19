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
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

from z3c.relationfield.relation import RelationValue

from collective.person.behaviors.user import IPloneUser

from s17.person.employee.content.employee import IEmployee

from s17.person.employee.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Member'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        login(self.portal, TEST_USER_NAME)

    def test_adding(self):
        self.folder.invokeFactory('s17.employee', 'e1')
        e1 = self.folder['e1']
        self.assertTrue(IEmployee.providedBy(e1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        schema = fti.lookupSchema()
        self.assertEqual(IEmployee, schema)

    def test_is_referenceable(self):
        self.folder.invokeFactory('s17.employee', 'e1')
        e1 = self.folder['e1']
        self.assertTrue(IAttributeUUID.providedBy(e1))
        self.assertTrue(IReferenceable.providedBy(e1))

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IEmployee.providedBy(new_object))

    def test_setTitle(self):
        self.folder.invokeFactory('s17.employee', 'e1')
        e1 = self.folder['e1']
        # Simple name and surname
        e1.setTitle('James Kirk')
        self.assertEqual(e1.given_name, 'James')
        self.assertEqual(e1.surname, 'Kirk')
        self.assertEqual(e1.fullname, 'James Kirk')
        # With two surnames
        e1.setTitle('James T. Kirk')
        self.assertEqual(e1.given_name, 'James')
        self.assertEqual(e1.surname, 'T. Kirk')
        self.assertEqual(e1.fullname, 'James T. Kirk')
        # Just a name
        e1.setTitle('Kirk')
        self.assertEqual(e1.given_name, 'Kirk')
        self.assertEqual(e1.surname, '')
        self.assertEqual(e1.fullname, 'Kirk ')
        # Nothing
        e1.setTitle('')
        self.assertEqual(e1.given_name, '')
        self.assertEqual(e1.surname, '')
        self.assertEqual(e1.fullname, ' ')

    def test_biography(self):
        # We config the plone user and attach a employee for it
        pm = getToolByName(self.portal, 'portal_membership')
        user = pm.getAuthenticatedMember()
        properties = {"email": "aaa@aaa.com",
                      "description": u"Just a user"}
        user.setMemberProperties(mapping=properties)

        self.folder.invokeFactory('s17.employee', TEST_USER_ID)
        e1 = self.folder[TEST_USER_ID]

        # We test the view method
        view = e1.unrestrictedTraverse('view')
        self.assertEqual(view.biography(), u"Just a user")

    def test_biography_with_behavior(self):
        pm = getToolByName(self.portal, 'portal_membership')
        user = pm.getAuthenticatedMember()
        properties = {"email": "aaa@aaa.com",
                      "description": u"Just a user"}
        user.setMemberProperties(mapping=properties)

        # We config the employee and attach a plone user for it
        self.folder.invokeFactory('s17.employee', 'e1')
        e1 = self.folder['e1']
        e1 = IPloneUser(e1)
        e1.user_name = TEST_USER_ID
        e1 = self.folder['e1']

        # We test the view method
        view = e1.unrestrictedTraverse('view')
        self.assertEqual(view.biography(), u"Just a user")

    def test_return_bosses(self):
        self.folder.invokeFactory('s17.employee', 'boss')
        boss = self.folder['boss']
        self.folder.invokeFactory('s17.employee', 'employee')
        employee = self.folder['employee']
        intids = getUtility(IIntIds)
        reports_to = []
        reports_to.append(RelationValue(intids.getId(boss)))
        employee.reports_to = reports_to
        self.assertEqual(employee.get_bosses()[0], boss)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
