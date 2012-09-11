# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

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

    def test_check_plone_user(self):
        pm = getToolByName(self.portal, 'portal_membership')
        self.folder.invokeFactory('s17.employee', 'someone',
                                   given_name='Someone', surname='Somebody')
        e1 = self.folder['someone']
        e1.reindexObject()
        user = pm.getMemberById('someone')
        self.assertEqual(user.getId(),e1.getId())


class FieldsetTest(unittest.TestCase):

    name = 'collective.person.behaviors.contact.IContactInfo'
    fake_name = 'plone.app.dexterity.behaviors.metadata.IDublinCore'

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = getToolByName(self.portal, 'portal_types')
        self.pc = self.portal['portal_personcatalog']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('s17.employee', 'e1')
        behaviors = []
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI,
                           name='s17.employee')
        fti.behaviors = tuple(behaviors)

    def test_fieldsets(self):
        behaviors = []
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        fti.behaviors = tuple(behaviors)
        e1 = self.folder['e1']
        request = self.layer['request']
        request.set('URL', e1.absolute_url() + '/employee_edit')
        request.set('ACTUAL_URL', e1.absolute_url() + '/employee_edit')
        edit = e1.restrictedTraverse('employee_edit')
        setattr(edit, 'portal_type', 's17.employee')
        edit.updateFieldsFromSchemata()
        self.assertEqual(edit.groups[0].label, 'Contact Info')

    def test_fake_fieldsets(self):
        behaviors = []
        behaviors.append(self.fake_name)
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        fti.behaviors = tuple(behaviors)
        e1 = self.folder['e1']
        request = self.layer['request']
        request.set('URL', e1.absolute_url() + '/employee_edit')
        request.set('ACTUAL_URL', e1.absolute_url() + '/employee_edit')
        edit = e1.restrictedTraverse('employee_edit')
        setattr(edit, 'portal_type', 's17.employee')
        edit.updateFieldsFromSchemata()

        # We check that our custom edit view is not taking effect
        # with external packages behaviors.
        self.assertEqual(edit.groups[0].label, 'Categorization')
        self.assertEqual(edit.groups[1].label, 'Dates')
        self.assertEqual(edit.groups[2].label, 'Ownership')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
