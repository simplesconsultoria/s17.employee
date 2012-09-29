# -*- coding: utf-8 -*-

from five import grok

from zope import schema
from zope.interface import Invalid, invariant

from Products.CMFCore.utils import getToolByName

from plone.directives import dexterity
from plone.formwidget.contenttree import ObjPathSourceBinder

from z3c.relationfield.schema import RelationList, RelationChoice

from s17.person.behaviors.user import IPloneUser
from s17.person.behaviors.contact import IContactInfo
from s17.person.content.person import IPerson
from s17.person.content.person import Person

from s17.employee import MessageFactory as _


fields = IPerson.names()
fields.reverse()


class IEmployee(IPerson):
    """ A representation of a Employee
    """

    employee_id = schema.Int(
        title=_(u"Registration number"),
        required=True,
    )

    position = schema.TextLine(
        title=_(u"Position"),
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
                                  source=ObjPathSourceBinder(
                                      portal_type='Employee')),
        required=False,
    )

    @invariant
    def restrict_year(data):
        """ Check year of birthday
        """
        birthday = data.birthday
        if birthday and birthday.year < 1901:
            raise Invalid(_(u"Years of birthdays have to be greater" +
                            " than 1900."))


class Employee(Person):
    """ Implementation of IEmployee
    """
    grok.implements(IEmployee)

    def setTitle(self, value):
        """ Membership tool expects a setTitle
        """
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
        """ Check if this employee has a corresponding Plone user.
        """
        context = self.context
        id = context.getId()
        pm = getToolByName(context, 'portal_membership')
        pt = getToolByName(context, 'portal_types')
        fti = pt['Employee']
        user = pm.getMemberById(id)
        if user:
            return user
        if 's17.person.behaviors.user.IPloneUser' in fti.behaviors:
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
            result.append({'IContactInfo.emails':
                           employee.emails})
        if employee.instant_messengers:
            result.append({'IContactInfo.instant_messengers':
                           employee.instant_messengers})
        if employee.telephones:
            result.append({'IContactInfo.telephones':
                           employee.telephones})
        return result

    def companyinfo_sorted_keys(self):
        employee = self.context
        result = []
        if employee.position:
            result.append({'position': employee.position})
        if employee.reports_to:
            result.append({'reports_to': employee.reports_to})
        if employee.ou:
            result.append({'ou': employee.ou})
        if employee.location:
            result.append({'location': employee.location})

        return result

    def portal_url(self):
        """ Return the portal url
        """
        portal_url = getToolByName(self.context, 'portal_url')
        return portal_url()
