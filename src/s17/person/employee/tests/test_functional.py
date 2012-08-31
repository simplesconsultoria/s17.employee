#-*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from s17.person.employee.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/test_birthdays.txt',
                                     package='s17.person.employee'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite