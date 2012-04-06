# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

from s17.person.employee.content.employee import IEmployee

from s17.person.employee.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

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
        self.assertEquals(IEmployee, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='s17.employee')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IEmployee.providedBy(new_object))

    def test_is_referenceable(self):
        self.folder.invokeFactory('s17.employee', 'e1')
        e1 = self.folder['e1']
        self.assertTrue(IReferenceable.providedBy(e1))
        self.assertTrue(IAttributeUUID.providedBy(e1))


class FieldsetTest(unittest.TestCase):

    name = 'collective.person.behaviors.contact.IContactInfo'
    fake_name = 'plone.app.dexterity.behaviors.metadata.IDublinCore'

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
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
        self.assertEquals(edit.groups[0].label, 'Contact Info')

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

        """We check that our custom edit view is not taking effect
        with external packages behaviors"""
        self.assertEquals(edit.groups[0].label, 'Categorization')
        self.assertEquals(edit.groups[1].label, 'Dates')
        self.assertEquals(edit.groups[2].label, 'Ownership')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
