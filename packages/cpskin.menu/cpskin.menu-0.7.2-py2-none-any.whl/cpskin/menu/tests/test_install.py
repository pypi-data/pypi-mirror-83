# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.uuid.interfaces import IUUID
from cpskin.menu.testing import CPSKIN_MENU_INTEGRATION_TESTING


class TestInstall(unittest.TestCase):

    layer = CPSKIN_MENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_plonesite_uuid(self):
        self.assertTrue(IUUID(self.portal) is not None)
