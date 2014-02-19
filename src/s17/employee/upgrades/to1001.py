# -*- coding: utf-8 -*-

from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from z3c.relationfield.event import updateRelations
from z3c.relationfield.interfaces import IHasRelations

from Products.CMFCore.utils import getToolByName


PROJECT = 's17.employee'


def reindex_zc_relations(context):
    ''' Upgrade to version 1001
        reindex zc.relations catalog
    '''
    rcatalog = getUtility(ICatalog)
    # Clear the relation catalog to fix issues with interfaces that don't exist anymore.
    # This actually fixes the bug editing employees than reports a:
    #   KeyError: <class 'plone.directives.form.schema.Schema'>
    rcatalog.clear()

    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.searchResults(object_provides=IHasRelations.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        updateRelations(obj, None)
