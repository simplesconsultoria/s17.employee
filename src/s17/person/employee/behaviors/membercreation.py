# -*- coding: utf-8 -*-

from five import grok

from zope.container.interfaces import IObjectAddedEvent
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName

from plone.directives import form
from plone.i18n.normalizer.interfaces import IIDNormalizer

from collective.person.behaviors.contact import IContactInfo

from s17.person.employee.content.employee import IEmployee


class IMemberCreation(form.Schema):
    """ Behavior to enable creation of plone member user
        when a employee is created.
    """


@grok.subscribe(IEmployee, IObjectAddedEvent)
def notifyUser(employee, event):
    pm = getToolByName(employee, 'portal_membership')
    pr = getToolByName(employee, 'portal_registration')
    pt = getToolByName(employee, 'portal_types')
    fti = pt['s17.employee']
    if (pm.getMemberById(employee.getId()) is not None) or \
        IMemberCreation.__identifier__ not in fti.behaviors:
        return None
    e_id = employee.getId()
    passwd = 'changeme123'
    fullname = employee.fullname
    email = u'changeme@changeme.com'
    if 'collective.person.behaviors.contact.IContactInfo' in fti.behaviors:
        contact_adapt_employee = IContactInfo(employee)
        emails = contact_adapt_employee.emails
        if emails != []:
            email = emails[0]['data']
    norm = queryUtility(IIDNormalizer)
    norm_name = norm.normalize(fullname)
    properties = {
        'username': norm_name,
        # Full name must be always as utf-8 encoded
        'fullname': fullname,
        # Email adress is obligated. If contact info behavior is not
        # activated we set a nonexistent email.
        'email': email,
    }
    try:
        member = pr.addMember(e_id, passwd, properties=properties)
    except ValueError, e:
        return None
