# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


PROJECT = 's17.person.employee'


def fromZero(context):
    ''' Upgrade from Zero to version 1000
    '''
    qi = getToolByName(context, 'portal_quickinstaller')
    qi.installProduct('collective.person',
                      locked=0,
                      hidden=0,
                      profile='collective.person:default')