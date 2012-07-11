# -*- coding:utf-8 -*-

from five import grok

from plone.directives import dexterity

from Acquisition import aq_inner
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from s17.person.employee.content.employee import IEmployee

from s17.person.employee import MessageFactory as _

class View(dexterity.DisplayForm):
    grok.context(IEmployee)
    grok.require('zope2.View')
    grok.name('view')

    def biography(self):
        context = self.context
        id = context.getId()
        pm = getToolByName(context, 'portal_membership')
        user = pm.getMemberById(id)
        biography = user.getProperty('description')
        if biography:
            return biography
        else:
            return None
            