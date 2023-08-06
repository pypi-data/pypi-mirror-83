# -*- coding: utf-8 -*-
from cpskin.menu.browser.menu import cache_key_desktop
from cpskin.menu.browser.menu import CpskinMenuViewlet
from cpskin.menu.browser.menu import invalidate_menu
from cpskin.menu.testing import CPSKIN_MENU_INTEGRATION_TESTING
from plone import api
from plone.app.testing import applyProfile
from plone.memoize.interfaces import ICacheChooser
from plone.uuid.interfaces import IUUID
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


def cache_exist(viewlet):
    # Si j utilise cache exist ici c'est bon
    adapter = queryUtility(ICacheChooser)('cpskin.menu.browser.menu.superfish_portal_tabs')
    key = cache_key_desktop(None, viewlet)
    return adapter.get(key) and True or False


def empty_cache():
    adapter = queryUtility(ICacheChooser)('cpskin.menu.browser.menu.superfish_portal_tabs')
    adapter.client.invalidateAll()


class TestMenu(unittest.TestCase):

    layer = CPSKIN_MENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        applyProfile(self.portal, 'cpskin.workflow:testing')
        self.portal_workflow = self.portal.portal_workflow
        self.portal_workflow.setDefaultChain('cpskin_workflow')
        self.portal_workflow.setChainForPortalTypes(
            ('Folder',), ('cpskin_workflow',)
        )
        item = self.portal.restrictedTraverse('commune/services_communaux')
        api.content.transition(obj=item, transition='publish_and_show')
        empty_cache()

    def tearDown(self):
        empty_cache()

    def test_menu_portal_tabs(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.is_homepage)
        menus = viewlet.superfish_portal_tabs()
        self.assertEqual(len(menus), 4994)

    def test_menu_cache_key_on_root(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        key = cache_key_desktop(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu-'))
        self.assertTrue(key.endswith(IUUID(viewlet._get_real_context())))

    def test_menu_cache_usage_test_fail(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_menu_cache_usage_different_context(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet1 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet1.update()
        self.assertEqual(cache_exist(viewlet1), False)
        viewlet1.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet1), True)

        item = self.portal.restrictedTraverse('commune')
        viewlet2 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet2.update()
        self.assertEqual(cache_exist(viewlet2), True)
        viewlet2.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet2), True)

        item = self.portal.restrictedTraverse('loisirs')
        viewlet3 = CpskinMenuViewlet(item, self.request, None, None)
        viewlet3.update()
        self.assertEqual(cache_exist(viewlet3), True)
        viewlet3.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet3), True)

    def test_menu_cache_invalidation(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        invalidate_menu(item)
        self.assertEqual(cache_exist(viewlet), False)

    def test_menu_cache_invalidate_another_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()

        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

        loisirs = self.portal.restrictedTraverse('loisirs')
        invalidate_menu(loisirs)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

        viewlet.superfish_portal_tabs()
        invalidate_menu(commune)
        self.assertEqual(cache_exist(viewlet), False)

    def test_objet_modification_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        item.setTitle('Test Cache Invalidation')
        notify(ObjectModifiedEvent(item))
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_object_creation_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.create(item, 'Folder', 'foo')
        self.assertEqual(cache_exist(viewlet), False)

    def test_object_publication_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        api.content.transition(item, 'back_to_created')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.transition(item, 'publish_and_show')
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_object_removed_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.delete(item)
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)

    def test_object_moved_invalidates_menus(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        loisirs = self.portal.restrictedTraverse('loisirs')
        api.content.transition(obj=commune, transition='publish_and_show')
        api.content.transition(obj=loisirs, transition='publish_and_show')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        viewlet_loisirs = CpskinMenuViewlet(loisirs, self.request, None, None)
        viewlet_loisirs.update()
        self.assertEqual(cache_exist(viewlet), True)
        self.assertEqual(cache_exist(viewlet_loisirs), True)
        api.content.move(item, loisirs)
        self.assertEqual(cache_exist(viewlet), False)
        self.assertEqual(cache_exist(viewlet_loisirs), False)
        viewlet.update()
        viewlet_loisirs.update()
        self.assertEqual(cache_exist(viewlet), False)
        self.assertEqual(cache_exist(viewlet_loisirs), False)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        self.assertEqual(cache_exist(viewlet_loisirs), True)

    def test_object_rename_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
        api.content.rename(item, new_id='sc')
        notify(ObjectModifiedEvent(item))
        viewlet.update()
        self.assertEqual(cache_exist(viewlet), False)
        viewlet.superfish_portal_tabs()
        self.assertEqual(cache_exist(viewlet), True)
