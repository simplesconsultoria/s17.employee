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


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
