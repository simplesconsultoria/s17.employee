# -*- coding: utf-8 -*-

from five import grok

from zope import schema
from zope.interface import Invalid, invariant
from zope.app.container.interfaces import IObjectAddedEvent
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName

from plone.directives import dexterity
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.formwidget.contenttree import ObjPathSourceBinder

from z3c.relationfield.schema import RelationList, RelationChoice

from collective.person.behaviors.user import IPloneUser
from collective.person.behaviors.contact import IContactInfo
from collective.person.content.person import IPerson
from collective.person.content.person import Person

from s17.person.employee import MessageFactory as _


fields = IPerson.names()
fields.reverse()


class IEmployee(IPerson):
    """ A representation of a Employee
    """

    employee_id = schema.Int(
        title=_(u"Registration number"),
        required=True,
        )

    charge = schema.TextLine(
        title=_(u"Charge"),
        description=_(u"Position in the company."),
        required=False,
        )

    ou = schema.TextLine(
        title=_(u"Organizational Unit"),
        description=_(u"To what unit this employee belong."),
        required=False,
        )

    location = schema.TextLine(
        title=_(u"Location"),
        description=_(u"Information of room/desk."),
        required=False,
        )

    extension = schema.Int(
        title=_(u"Extension line"),
        description=_(u"Internal extension line to contact this employee."),
        required=False,
        )

    reports_to = RelationList(
        title=_(u'Boss', default=u'Boss'),
        default=[],
        value_type=RelationChoice(title=u"Boss",
                      source=ObjPathSourceBinder(portal_type='s17.employee')),
        required=False,
        )

    @invariant
    def restrict_year(data):
        ''' Check year of birthday. '''
        birthday = data.birthday
        if birthday and birthday.year < 1901:
            raise Invalid(_(u"Years of birthdays have to be greater" + \
                                " than 1900."))


class Employee(Person):
    """ Implementation of IEmployee
    """
    grok.implements(IEmployee)

    def setTitle(self, value):
        ''' Membership tool expects a setTitle '''
        title = value.split(' ')
        given_name = surname = ''
        if len(title) == 2:
            given_name = title[0]
            surname = title[1]
        elif len(title) == 1:
            given_name = title[0]
            surname = ''
        elif len(title) > 2:
            given_name = title[0]
            surname = ' '.join(title[1:])
        else:
            # Overide here
            given_name = ''
            surname = ''
        self.given_name = given_name
        self.surname = surname

    def get_bosses(self):
        """ Return the employee objects with this employee reports to.
        """
        results = []
        if self.reports_to == []:
            return results
        for value in self.reports_to:
            results.append(value.to_object)
        return results


class EmployeeEditForm(dexterity.EditForm):
    grok.context(IEmployee)


class View(dexterity.DisplayForm):
    grok.context(IEmployee)
    grok.require('zope2.View')
    grok.name('view')

    def biography(self):
        user = self.check_member()
        if user:
            biography = user.getProperty('description')
            if biography:
                return biography
            else:
                return None
        else:
            return None

    def check_member(self):
        """ Check if the employee is attached to a plone user.
        """
        context = self.context
        id = context.getId()
        pm = getToolByName(context, 'portal_membership')
        pt = getToolByName(context, 'portal_types')
        fti = pt['s17.employee']
        user = pm.getMemberById(id)
        if user:
            return user
        if 'collective.person.behaviors.user.IPloneUser' in fti.behaviors:
            item = IPloneUser(context)
            user = pm.getMemberById(item.user_name)
        if user:
            return user

        return None

    def base_sorted_keys(self):
        employee = self.context
        result = []
        if employee.employee_id:
            result.append({'employee_id': employee.employee_id})
        if employee.birthday:
            result.append({'birthday': employee.birthday})
        return result

    def contact_sorted_keys(self):
        employee = self.context
        employee = IContactInfo(employee)
        result = []
        if employee.emails:
            result.append({'IContactInfo.emails': \
                            employee.emails})
        if employee.instant_messengers:
            result.append({'IContactInfo.instant_messengers': \
                            employee.instant_messengers})
        if employee.telephones:
            result.append({'IContactInfo.telephones': \
                            employee.telephones})
        return result

    def companyinfo_sorted_keys(self):
        employee = self.context
        result = []
        if employee.charge:
            result.append({'charge': employee.charge})
        if employee.reports_to:
            result.append({'reports_to': employee.reports_to})
        if employee.ou:
            result.append({'ou': employee.ou})
        if employee.location:
            result.append({'location': employee.location})

        return result


@grok.subscribe(IEmployee, IObjectAddedEvent)
def notifyUser(employee, event):
    pm = getToolByName(employee, 'portal_membership')
    if pm.getMemberById(employee.getId()) is not None:
        return None
    pr = getToolByName(employee, 'portal_registration')
    pt = getToolByName(employee, 'portal_types')
    fti = pt['s17.employee']
    e_id = employee.getId()
    passwd = 'changeme123'
    fullname = employee.fullname
    email = u'changeme@changeme.com'
    if 'collective.person.behaviors.contact.IContactInfo' in fti.behaviors:
        adapt_employee = IContactInfo(employee)
        emails = adapt_employee.emails
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
