import unittest

import robotsuite

from plone.testing import layered

from s17.employee.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_employees.txt"),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
