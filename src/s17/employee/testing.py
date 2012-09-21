# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import s17.person.employee
        self.loadZCML(package=s17.person.employee)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        pw = getToolByName(portal, 'portal_workflow')
        pw.setDefaultChain('intranet_workflow')
        self.applyProfile(portal, 's17.person.employee:default')
        self.applyProfile(portal, 's17.person.employee:demo')
        self.applyProfile(portal, 's17.person.employee:test')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='s17.person.employee:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='s17.person.employee:Functional',
    )
