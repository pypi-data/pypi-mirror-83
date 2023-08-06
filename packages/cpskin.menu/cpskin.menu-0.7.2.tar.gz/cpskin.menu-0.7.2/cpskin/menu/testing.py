# -*- coding: utf-8 -*-

from zope.component import queryUtility
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.testing import z2
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import applyProfile
from plone.app.testing import (login,
                               TEST_USER_NAME,
                               setRoles,
                               TEST_USER_ID)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.registry.interfaces import IRegistry
from plone.memoize.interfaces import ICacheChooser

from affinitic.caching.memcached import MemcacheAdapter
from affinitic.caching.testing import NO_MEMCACHED

from cpskin.menu.interfaces import IFourthLevelNavigation, IDirectAccess

import cpskin.menu


def memcached_launched():
    adapter = queryUtility(ICacheChooser)('cpskin.menu.browser.menu.superfish_portal_tabs')
    if isinstance(adapter, MemcacheAdapter):
        adapter['test_key'] = 'test_value'
        if adapter.get('test_key'):
            return True
    return False


class CPSkinMenuPloneWithPackageLayer(PloneWithPackageLayer):
    """
    plone (portal root)
    |
    |-- 1: Commune
    |   `-- 2: Services communaux
    |       `-- 3: Finances
    |
    `-- 1: Loisirs
        |-- 2: Tourisme
        |   `-- 3: Promenades [Direct access]
        |
        `-- 2: Art & Culture
            |-- 3: Bibliothèques
            `-- 3: Artistes [Fourth level navigation]
                |-- 4: Tata
                |-- 4: Yoyo
                |-- 4: Abba [Direct access]
                `-- 4: Rockers
                |   |-- 5: John Lennon [Direct access]
                |   `-- 5: Mick Jagger
                |       `-- test
                `-- 4: Cinema [Fourth level navigation] (wrong place)
                    `-- 5: Kinepolis
    """

    load_page_menu = False

    def setUpZope(self, app, configurationContext):
        super(CPSkinMenuPloneWithPackageLayer,
              self).setUpZope(app, configurationContext)
        z2.installProduct(app, 'Products.DateRecurringIndex')
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes)

    def setUpPloneSite(self, portal):
        if not memcached_launched():
            raise EnvironmentError('Memcached must be launched')
        applyProfile(portal, 'cpskin.menu:testing')

        applyProfile(portal, 'cpskin.workflow:testing')
        portal.portal_workflow.setDefaultChain('cpskin_workflow')
        # import pdb; pdb.set_trace()
        catalog = getToolByName(portal, 'portal_catalog')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # disable non folderish sections
        # to fake workflow filtered base navigation
        portal.portal_properties.site_properties.manage_changeProperties(disable_nonfolderish_sections=True)

        registry = queryUtility(IRegistry)
        registry.records['cpskin.core.interfaces.ICPSkinSettings.load_page_menu'].value = self.load_page_menu

        commune = api.content.create(
            type='Folder',
            title='COMMUNE',
            id='commune',
            container=portal)
        services_communaux = api.content.create(
            type='Folder',
            title='Services communaux',
            id='services_communaux',
            container=commune)
        api.content.create(
            type='Folder',
            title='Finances',
            id='finances',
            container=services_communaux)

        loisirs = api.content.create(
            type='Folder',
            title='LOISIRS',
            id='loisirs',
            container=portal)
        tourisme = api.content.create(
            type='Folder',
            title='Tourisme',
            id='tourisme',
            container=loisirs)
        promenades = api.content.create(
            type='Folder',
            title='Promenades',
            id='promenades',
            container=tourisme)

        art_et_culture = api.content.create(
            type='Folder',
            title='Art & Culture',
            id='art_et_culture',
            container=loisirs)
        api.content.create(
            type='Folder',
            title='Bibliothèques',
            id='bibliotheques',
            container=art_et_culture)

        artistes = api.content.create(
            type='Folder',
            title='Artistes',
            id='artistes',
            container=art_et_culture)
        api.content.create(
            type='Folder',
            title='Tata',
            id='tata',
            container=artistes)
        api.content.create(
            type='Folder',
            title='Yoyo',
            id='yoyo',
            container=artistes)
        abba = api.content.create(
            type='Folder',
            title='Abba',
            id='abba',
            container=artistes)
        rockers = api.content.create(
            type='Folder',
            title='Rockers',
            id='rockers',
            container=artistes)
        john_lennon = api.content.create(
            type='Folder',
            title='John Lennon',
            id='john_lennon',
            container=rockers)
        api.content.create(
            type='Folder',
            title='Mick Jagger',
            id='mick_jagger',
            container=rockers)

        cinema = api.content.create(
            type='Folder',
            title='Cinema',
            id='cinema',
            container=artistes)
        api.content.create(
            type='Folder',
            title='Kinepolis',
            id='kinepolis',
            container=cinema)

        alsoProvides(artistes, IFourthLevelNavigation)
        alsoProvides(cinema, IFourthLevelNavigation)
        alsoProvides(tourisme, IDirectAccess)
        catalog.reindexObject(tourisme)
        alsoProvides(promenades, IDirectAccess)
        catalog.reindexObject(promenades)
        alsoProvides(abba, IDirectAccess)
        catalog.reindexObject(abba)
        alsoProvides(john_lennon, IDirectAccess)
        catalog.reindexObject(john_lennon)


class CPSkinMenuLoadPage(CPSkinMenuPloneWithPackageLayer):

    load_page_menu = True


CPSKIN_MENU_FIXTURE = CPSkinMenuPloneWithPackageLayer(
    name='CPSKIN_MENU_FIXTURE',
    zcml_filename='testing.zcml',
    zcml_package=cpskin.menu,
    gs_profile_id='cpskin.menu:testing')

CPSKIN_MENU_FIXTURE_LOAD_PAGE = CPSkinMenuLoadPage(
    name='CPSKIN_MENU_FIXTURE_LOAD_PAGE',
    zcml_filename='testing.zcml',
    zcml_package=cpskin.menu,
    gs_profile_id='cpskin.menu:testing')


CPSKIN_MENU_INTEGRATION_TESTING = IntegrationTesting(
    name='CPSKIN_MENU_INTEGRATION_TESTING',
    bases=(CPSKIN_MENU_FIXTURE,))


CPSKIN_MENU_LOAD_PAGE_INTEGRATION_TESTING = IntegrationTesting(
    name='CPSKIN_MENU_LOAD_PAGE_INTEGRATION_TESTING',
    bases=(CPSKIN_MENU_FIXTURE_LOAD_PAGE,))


CPSKIN_MENU_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_MENU_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='cpskin.menu:Robot')

CPSKIN_MENU_ROBOT_TESTING_LOAD_PAGE = FunctionalTesting(
    bases=(CPSKIN_MENU_FIXTURE_LOAD_PAGE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='cpskin.menu:Robot load page')


NO_MEMCACHED_CPSKIN_MENU_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_MENU_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE, NO_MEMCACHED),
    name='NO_MEMCACHED_CPSKIN_MENU_ROBOT_TESTING')
