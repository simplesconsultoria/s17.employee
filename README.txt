************
s17.employee
************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A package containing a Dexterity content type and behaviors to represent an
Employe as a content in a Plone site.

This package depends on `s17.person`_.

Don't panic
-----------

Demo profile
^^^^^^^^^^^^

To give yourself an example you can use the demo profile within the product.
The steps to activate this profile you must do:

    1. Go to the zmi -> portal_setup.
    2. Click on ''Import'' tab.
    3. Select the profile ''s17.employee: Demo profile'' from the drop
       down.
    4. Check the step ''s17.employee: Demo steps'' and click the button
       ''import selected steps''.

Once you done the process you can see in you site a folder called
''Employees'' with five employee items in wich each one have a base of
information with a picture.

With this option you can have a quick view to see what this product offers.

User member area
^^^^^^^^^^^^^^^^

If you want to enable the member creation area, you need to just run the
profile: profile-s17.employee:use_memberarea.

The member area will be the type Employee that contains all the information
about the user (employee).

Behaviors
^^^^^^^^^

This package include a behavior called **Member creation** that enables
the functionality to create a plone user member for an employee when is
created.
The default id is the same of the employee object and the *default password*
of the plone user is *changeme123*.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/s17.employee.png
    :target: http://travis-ci.org/simplesconsultoria/s17.employee

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`s17.person`: https://github.com/simplesconsultoria/s17.person
.. _`opening a support ticket`: https://github.com/simplesconsultoria/s17.employee/issues

