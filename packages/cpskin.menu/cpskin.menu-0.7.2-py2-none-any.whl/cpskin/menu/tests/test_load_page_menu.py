# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import getUtility
from zope.ramcache.interfaces.ram import IRAMCache
from cpskin.menu.testing import CPSKIN_MENU_LOAD_PAGE_INTEGRATION_TESTING
from cpskin.menu.browser.menu import CpskinMenuViewlet


def get_cache_miss():
    storage = getUtility(IRAMCache)._getStorage()
    return storage._misses.get('cpskin.menu.browser.menu.superfish_portal_tabs', 0)


class TestLoadPageMenu(unittest.TestCase):

    layer = CPSKIN_MENU_LOAD_PAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_menu_lp_portal_tabs(self):
        """Root page + load page menu actived should not return menus"""
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()

        self.assertTrue(viewlet.is_homepage)
        menus = viewlet.superfish_portal_tabs()

        self.assertEqual(len(menus), 0)
