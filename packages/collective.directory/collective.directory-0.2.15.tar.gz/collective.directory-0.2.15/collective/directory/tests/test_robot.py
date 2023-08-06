# -*- coding: utf-8 -*-
from plone.testing import layered
from collective.directory.testing import COLLECTIVE_DIRECTORY_ROBOT_TESTING

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot'),
                layer=COLLECTIVE_DIRECTORY_ROBOT_TESTING),
    ])
    return suite
