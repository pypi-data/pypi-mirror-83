# -*- coding: utf-8 -*-
from plone.testing import layered
import unittest
import robotsuite

from imio.ckeditortemplates.testing import IMIO_CKEDITORTEMPLATES_ROBOT_TESTING


def test_suite():
    suite = unittest.TestSuite()
    # robots_file = ['example.robot']
    robots_file = []

    for robot_file in robots_file:
        rts = robotsuite.RobotTestSuite(robot_file)
        suite.addTests([
            layered(rts,  layer=IMIO_CKEDITORTEMPLATES_ROBOT_TESTING)
        ])
    return suite
