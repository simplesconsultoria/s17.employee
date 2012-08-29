# -*- coding: utf-8 -*-

from five import grok

from z3c.form import field

from Products.CMFCore.utils import getToolByName

from plone.autoform.utils import processFieldMoves, processFields
from plone.behavior.interfaces import IBehaviorAssignable
from plone.directives import dexterity
from plone.z3cform.fieldsets.group import GroupFactory

from collective.person.behaviors.user import IPloneUser
from collective.person.content.person import IPerson
from collective.person.content.person import Person


fields = IPerson.names()
fields.reverse()


class IEmployee(IPerson):
    """ A representation of a Employee
    """


class Employee(Person):
    """ Implementation of IEmployee
    """
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


class EmployeeEditForm(dexterity.EditForm):
    grok.context(IEmployee)
    grok.name('employee_edit')

    autoGroups = True

    def is_from_person(self, schema):
        """ Check if the behavior belongs to the package collective.person.
        """
        assignable = IBehaviorAssignable(self.getContent())
        result = False
        for behavior in assignable.enumerateBehaviors():
            if (behavior.interface.getName() == schema.getName()) and \
               (behavior.factory.__module__.find('collective.person') == 0):
                result = behavior
        return result

    def updateFieldsFromSchemata(self):
        """ Override method especific for additional schematas based of
        collective.person behaviors.
        """

        # If the form is called from the ++widget++ traversal namespace,
        # we won't have a user yet. In this case, we can't perform permission
        # checks.

        have_user = bool(self.request.get('AUTHENTICATED_USER', False))

        # Turn fields into an instance variable, since we will be modifying it
        self.fields = field.Fields(self.fields)

        # Copy groups to an instance variable and ensure that we have
        # the more mutable factories, rather than 'Group' subclasses

        groups = []

        for g in self.groups:
            group_name = getattr(g, '__name__', g.label)
            fieldset_group = GroupFactory(group_name,
                                          field.Fields(g.fields),
                                          g.label,
                                          getattr(g, 'description', None))
            groups.append(fieldset_group)

        # Copy to instance variable only after we have potentially read from
        # the class
        self.groups = groups

        prefixes = {}

        # Set up all widgets, modes, omitted fields and fieldsets
        if self.schema is not None:
            processFields(self, self.schema, permissionChecks=have_user)
            for schema in self.additionalSchemata:

                # Find the prefix to use for this form and cache for next round
                prefix = self.getPrefix(schema)
                if prefix and prefix in prefixes:
                    prefix = schema.__identifier__
                prefixes[schema] = prefix

                # By default, there's no default group, i.e. fields go
                # straight into the default fieldset

                defaultGroup = None

                # Create groups from schemata if requested and set default
                # group
                behavior = self.is_from_person(schema)
                if self.autoGroups and behavior:
                    group_name = behavior.title

                    # Look for group - note that previous processFields
                    # may have changed the groups list, so we can't easily
                    # store this in a dict.
                    found = False
                    for g in self.groups:
                        if group_name == getattr(g, '__name__', g.label):
                            found = True
                            break

                    if not found:
                        fieldset_group = GroupFactory(group_name,
                                                      field.Fields(),
                                                      group_name)
                        self.groups.append(fieldset_group)

                    defaultGroup = group_name

                processFields(self, schema, prefix=prefix, \
                              defaultGroup=defaultGroup, \
                              permissionChecks=have_user)

        # Then process relative field movements. The base schema is processed
        # last to allow it to override any movements made in additional
        # schemata.
        if self.schema is not None:
            for schema in self.additionalSchemata:
                processFieldMoves(self, schema, prefix=prefixes[schema])
            processFieldMoves(self, self.schema)


class View(dexterity.DisplayForm):
    grok.context(IEmployee)
    grok.require('zope2.View')
    grok.name('view')

    def biography(self):
        context = self.context
        id = context.getId()
        pm = getToolByName(context, 'portal_membership')
        pt = getToolByName(context, 'portal_types')
        fti = pt['s17.employee']
        user = pm.getMemberById(id)
        if not user and \
           'collective.person.behaviors.user.IPloneUser' in fti.behaviors:
            item = IPloneUser(context)
            user = pm.getMemberById(item.user_name)
        if user:
            biography = user.getProperty('description')
            if biography:
                return biography
            else:
                return None
        else:
            return None
