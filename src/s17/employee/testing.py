# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing.z2 import ZSERVER_FIXTURE


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import s17.employee
        self.loadZCML(package=s17.employee)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        pw = getToolByName(portal, 'portal_workflow')
        pw.setDefaultChain('intranet_workflow')
        self.applyProfile(portal, 's17.employee:default')
        self.applyProfile(portal, 's17.employee:demo')
        self.applyProfile(portal, 's17.employee:test')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='s17.employee:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, ZSERVER_FIXTURE,),
    name='s17.employee:Functional',
)
