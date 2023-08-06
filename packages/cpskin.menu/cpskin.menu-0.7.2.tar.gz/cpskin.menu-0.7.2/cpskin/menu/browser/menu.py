# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from affinitic.caching.memcached import invalidate_dependencies

from Acquisition import aq_inner, aq_parent

from plone import api
from plone.uuid.interfaces import IUUID
from plone.app.layout.viewlets import common
from plone.app.layout.navigation.navtree import buildFolderTree

from affinitic.caching import cache
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.memoize import view
from plone.memoize.volatile import DontCache
from cpskin.menu.interfaces import IDirectAccess

from zope.i18n import translate

from collective.superfish.browser.sections import (VirtualCatalogBrain,
                                                   SuperFishQueryBuilder,
                                                   SuperFishViewlet)


DESKTOP_ID = 'menu-desktop'
MOBILE_ID = 'menu-mobile'


def cache_key(menu_key, obj_id, request):
    if obj_id is None:
        raise DontCache()
    server_url = request.other['SERVER_URL']
    language = request.other.get('LANGUAGE', 'default')
    domain = request.environ.get('HTTP_X_FORWARDED_HOST', server_url)
    key = "{0}.{1}.{2}.{3}".format(menu_key, domain, language, obj_id)
    return key


def cache_key_desktop(meth, viewlet):
    obj_id = IUUID(viewlet._get_root_menu(mobile=False), None)
    return cache_key(DESKTOP_ID, obj_id, viewlet.request)


def cache_key_mobile(meth, viewlet):
    obj_id = IUUID(viewlet._get_root_menu(mobile=True), None)
    return cache_key(MOBILE_ID, obj_id, viewlet.request)


def get_menu_dependencies_desktop(meth, viewlet):
    """
    Store the root_menu id for dependencies, so by invalidating this dependencies
    with invalidate_dependencies, all related submenu will be invalidated
    """
    obj_id = IUUID(viewlet._get_root_menu(mobile=False), None)
    key = "{0}.{1}".format(DESKTOP_ID, obj_id)
    return [key]


def get_menu_dependencies_mobile(meth, viewlet):
    obj_id = IUUID(viewlet._get_root_menu(mobile=True), None)
    key = "{0}.{1}".format(MOBILE_ID, obj_id)
    return [key]

cached_method_id = 'cpskin.menu.browser.menu.superfish_portal_tabs'


def invalidate_menu(context):
    request = getRequest()
    if request is None:  # when plone site is created
        request = getattr(context, 'REQUEST', None)
        if request is None:  # when zope is starting
            return
    viewlet = CpskinMenuViewlet(context, request, None, None)
    try:
        dependencies = get_menu_dependencies_desktop(viewlet.superfish_portal_tabs, viewlet)
        invalidate_dependencies(dependencies)
    except DontCache:
        pass
    try:
        dependencies = get_menu_dependencies_mobile(viewlet.superfish_portal_tabs, viewlet)
        invalidate_dependencies(dependencies)
    except DontCache:
        pass


class UtilsView(BrowserView):

    def show_description(self):
        return api.portal.get_registry_record(
            'cpskin.core.interfaces.ICPSkinSettings.show_description_on_themes')  # noqa


class CpskinMenuViewlet(common.GlobalSectionsViewlet, SuperFishViewlet):

    index = ViewPageTemplateFile('menu.pt')

    # monkey patch this if you want to use collective.superfish together with
    # global_sections, need another start level or menu depth.
    menu_id = 'portal-globalnav-cpskinmenu'
    menu_depth = 4

    ADD_PORTAL_TABS = True

    # this template is used to generate a single menu item.
    _menu_item = (
        u"""<li id="%(menu_id)s-%(id)s"%(classnames)s aria-expanded="false"><span>"""
        u"""<a href="%(url)s" target="%(target)s" title="%(description)s" """
        u"""id="%(id)s" tabindex="%(tabindex)s">%(title)s</a></span>%(submenu)s</li>"""
    )

    # this template is used to generate a menu container
    _submenu_item = u"""<ul%(id)s class="%(classname)s">%(close)s%(menuitems)s</ul>"""

    @view.memoize
    def _get_real_context(self):
        context = self.context
        plone_view = getMultiAdapter((context, self.request), name="plone")
        if plone_view.isDefaultPageInFolder():
            context = aq_parent(context)
        context = aq_inner(context)
        return context

    @view.memoize
    def _get_root_menu(self, mobile):
        context = self._get_real_context()

        if mobile or not self._is_load_page_menu():
            return api.portal.get_navigation_root(context)
        else:
            # Plone site root?
            if '/'.join(context.getPhysicalPath()) == self.navigation_root_path:
                return context

            # Top level of actual submenu
            while 1:
                if '/'.join(context.aq_parent.getPhysicalPath()) == self.navigation_root_path:
                    break
                context = context.aq_parent
            return context

    @property
    def is_homepage(self):
        return IPloneSiteRoot.providedBy(self._get_real_context())

    def __init__(self, *args):
        super(CpskinMenuViewlet, self).__init__(*args)

        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')

        self.current_url = context_state.current_page_url()
        self.site_url = portal_state.portal_url()
        context = self._get_real_context()

        self.root_path = api.portal.get_navigation_root(context).getPhysicalPath()
        self.nav_start_level = len(self.root_path)
        self.physical_path = context.getPhysicalPath()
        self.navigation_root_path = '/'.join(self.physical_path[:self.nav_start_level])

    def _build_navtree(self, navigation_root, depth):
        # we generate our navigation out of the sitemap. so we can use the
        # highspeed navtree generation, and use it's caching features too.
        query = SuperFishQueryBuilder(self.context)()
        query['path']['depth'] = depth
        query['path']['query'] = navigation_root

        # no special strategy needed, so i kicked the INavtreeStrategy lookup.
        context = self._get_real_context()
        return buildFolderTree(self.context, obj=context, query=query)

    def update(self):
        super(CpskinMenuViewlet, self).update()
        # Why different depth in desktop and mobile?
        self.data = self._build_navtree(self.navigation_root_path,
                                        depth=self.menu_depth)

    @cache(cache_key_desktop, get_dependencies=get_menu_dependencies_desktop)
    def superfish_portal_tabs(self):
        """We do not want to use the template-code any more.
           Python code should speedup rendering."""
        child_id = None

        # Need to get only child menu if we are not in root
        if self.physical_path != self.root_path:
            child_id = self.physical_path[self.nav_start_level]

        return self.superfish_portal_tabs_child_desktop(child_id)

    @cache(cache_key_mobile, get_dependencies=get_menu_dependencies_mobile)
    def superfish_portal_tabs_mobile(self):
        """We do not want to use the template-code any more.
           Python code should speedup rendering."""
        child_id = None

        # Need to get only child menu if we are not in root
        if self.physical_path != self.root_path:
            child_id = self.physical_path[self.nav_start_level]

        return self.superfish_portal_tabs_child_mobile(child_id)

    def superfish_portal_tabs_child_desktop(self, child_id):
        menu = u""

        self.mobile = False

        tabindex = self._calculate_tabindex()

        # We do not need to calculate menu if not in a theme view
        if self.data:  # and self._is_in_theme:
            menu = u""

            # Do not render menu at root page in load_page_menu mode
            if not (self._is_load_page_menu()
                    and '/'.join(self._get_real_context().getPhysicalPath()) == self.navigation_root_path):

                for item in self.data['children']:
                    item_id = item['item'].id
                    self.menu_id = 'portal-globalnav-cpskinmenu-' + item_id

                    if self._is_load_page_menu():
                        menu_classnames = u"sf-menu cpskinmenu-load-page"
                    else:
                        menu_classnames = u"sf-menu"

                    menu += self._submenu(
                        item['children'],
                        tabindex,
                        menu_classnames=menu_classnames,
                        close_button=True,
                    )
        return menu

    def superfish_portal_tabs_child_mobile(self, child_id):
        menu = u""

        tabindex = self._calculate_tabindex()
        self.mobile = True
        self.menu_id = 'portal-globalnav-cpskinmenu-mobile'
        if self.data:
            menu = self._submenu(
                self.data['children'],
                tabindex,
                menu_classnames=u"sf-menu-mobile",
                close_button=False,
            )
        return menu

    def _submenu(self, items, tabindex, menu_level=0, menu_classnames='', close_button=False, direct_access=False):
        i = 0
        s = []

        # exclude nav items for non direct access
        if not direct_access:
            items = [item for item in items if not item['item'].exclude_from_nav]

        if not items:
            return ''

        for item in items:
            first = (i == 0)
            i += 1
            last = (i == len(items))

            s.append(self._menuitem(item, tabindex, first, last, menu_level))

        menu_id = u""
        if self.menu_id:
            if not menu_level:
                menu_id = self.menu_id and u" id=\"%s\"" % (self.menu_id) or u""

        submenu = u""
        close = u""
        if not self.mobile and close_button and menu_level == 1:
            close = """<span class="icon-cancel-circled2 navTreeClose" />"""
        submenu = self._submenu_item % dict(
            id=menu_id,
            menuitems=u"".join(s),
            classname=u"portal-globalnav-cpskinmenu navTreeLevel%d %s" % (
                menu_level, menu_classnames),
            close=close,
        )
        return submenu

    def _menuitem(self, item, tabindex, first=False, last=False, menu_level=0):
        classes = []

        if first:
            classes.append('firstItem')
        if last:
            classes.append('lastItem')

        brain = item.get('item')
        target = '_self'
        if type(brain) == VirtualCatalogBrain:
            # translate our portal_actions and use their id instead of the
            # url
            title = translate(brain.Title, context=self.request)
            desc = translate(brain.Description, context=self.request)
            url = brain.url.strip(self.context.portal_url())
            item_id = brain.id
        else:
            title = safe_unicode(brain.Title)
            desc = safe_unicode(brain.Description)
            url = brain.getPath()
            item_id = brain.getURL()[len(self.site_url):]
            if brain.Type == 'Link':
                obj = brain.getObject()
                current_user = api.user.get_current()
                can_edit = current_user.has_permission('Edit', brain)
                if not can_edit:
                    obj = brain.getObject()
                    if hasattr(obj, 'target_blank'):
                        target = '_blank' if obj.target_blank is True else '_self'


        item_id = item_id.strip('/').replace('/', '-')

        children = item['children']

        """
            plone (portal root)
            |
            `-- 1: Commune (*) (Not generated by this script)
                `-- 2: Services communaux (0) (Parent of the Direct Access)
                    `-- 3: Finances (1) (Direct access, Parent of the fourth level)
                        `-- 4: Tata (2) (Fourth level)

        """
        if self.mobile:
            direct_access_level = 1
            fourth_menu_level = 2
        else:
            # Level of PARENT of the level showing the Direct access
            direct_access_level = 0
            # Level of PARENT of the fourth level
            fourth_menu_level = 1

        if menu_level == direct_access_level:
            queryDict = {}
            queryDict['path'] = {'query': url, 'depth': 10}
            queryDict['sort_on'] = 'sortable_title'
            queryDict['object_provides'] = 'cpskin.menu.interfaces.IDirectAccess'
            catalog = getToolByName(self.context, 'portal_catalog')

            direct_access_catalog = catalog(queryDict)
            direct_access = []
            normal_children = []
            for child in children:
                normal_children.append(child)
            for element in direct_access_catalog:
                direct_access.append({'item': element,
                                      'depth': 1,
                                      'children': [],
                                      'currentParent': False,
                                      'currentItem': False})
            if direct_access:
                submenu_render = self._submenu(
                    normal_children,
                    tabindex,
                    menu_level=menu_level + 1,
                    menu_classnames='has_direct_access',
                    close_button=False) or u""
                submenu_render += self._submenu(
                    direct_access,
                    tabindex,
                    menu_level=menu_level + 1,
                    menu_classnames='direct_access',
                    close_button=True,
                    direct_access=True) or u""
            else:
                submenu_render = self._submenu(
                    children,
                    tabindex,
                    menu_level=menu_level + 1,
                    menu_classnames='no_direct_access',
                    close_button=True) or u""
        elif menu_level == fourth_menu_level:
            if IDirectAccess.providedBy(item['item'].getObject()):
                submenu_render = u""
            else:
                helper_view = getMultiAdapter((item['item'].getObject(), self.request), name=u'multilevel-navigation')
                if helper_view.is_enabled:
                    submenu_render = self._submenu(
                        children,
                        tabindex,
                        menu_level=menu_level + 1,
                        close_button=True) or u""
                else:
                    submenu_render = u""
        else:
            submenu_render = self._submenu(
                children,
                tabindex,
                menu_level=menu_level + 1,
                close_button=True) or u""

        return self._menu_item % dict(
            menu_id=self.menu_id,
            id=item_id,
            tabindex=tabindex,
            level=menu_level,
            title=self.html_escape(title),
            description=self.html_escape(desc),
            target=target,
            url=item['item'].getURL(),
            classnames=len(classes) and u' class="%s"' % (" ".join(classes)) or u"",
            selected=item['currentItem'] and u' class="selected"' or u"",
            submenu=submenu_render)

    def _calculate_tabindex(self):
        """
        Calculate tabindex of actual context
        """
        # For accessibility tabindex must always be 0
        return 0

    def _is_in_theme(self):
        """
        Returns True if we are currently in a theme (non root, navigation view)
        """
        context = self.context
        # Get the right object if we are on a default page
        portal = getToolByName(context, 'portal_url').getPortalObject()
        plone_view = portal.restrictedTraverse('@@plone')
        if plone_view.isDefaultPageInFolder():
            # if the context is a default page, get the parent!
            obj = context.aq_inner.aq_parent
            context = obj
        # Take the path, traverse to the first level and see if it is a
        # element respecting the navigation strategy
        portal_url = getToolByName(context, 'portal_url')
        contentPath = portal_url.getRelativeContentPath(context)
        if not len(contentPath):
            # we are on the home page
            return False
        # Use the portal_catalog the get the first level element
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal = getToolByName(context, 'portal_url').getPortalObject()
        queryDict = {}
        queryDict['path'] = {'query': '/'.join(portal.getPhysicalPath()) + '/' + contentPath[0], 'depth': 0}
        queryDict['portal_type'] = 'Folder'
        brains = portal_catalog(queryDict)
        if not brains:
            return False
        brain = brains[0]
        navtreeProps = getToolByName(context, 'portal_properties').navtree_properties
        if brain.meta_type not in navtreeProps.metaTypesNotToList and \
           (brain.review_state in navtreeProps.wf_states_to_show or
            not navtreeProps.enable_wf_state_filtering) and \
           brain.id not in navtreeProps.idsNotToList:
            return True
        return False

    def _is_load_page_menu(self):
        portal_registry = getToolByName(self.context, 'portal_registry')
        record = 'cpskin.core.interfaces.ICPSkinSettings.load_page_menu'
        # if record in portal_registry.records:
        #     return portal_registry[record]
        # else:
        #     return False
        try:
            return portal_registry[record]
        except:
            return False


def getNavigationRoot(context):
    """
    Return brains of the navigation root menu
    """
    # Get 1st level folders appearing in navigation
    portal_catalog = api.portal.get_tool('portal_catalog')
    navtreeProps = api.portal.get_tool('portal_properties').navtree_properties
    portal = api.portal.get()
    queryDict = {}
    # LATER : queryPath = getNavigationRoot(context) ?
    queryDict['path'] = {'query': '/'.join(portal.getPhysicalPath()), 'depth': 1}
    if navtreeProps.enable_wf_state_filtering:
        queryDict['review_state'] = navtreeProps.wf_states_to_show
    queryDict['sort_on'] = 'getObjPositionInParent'
    queryDict['portal_type'] = 'Folder'
    queryDict['is_default_page'] = False
    brains = portal_catalog(queryDict)
    res = [b for b in brains if b.id not in navtreeProps.idsNotToList]
    return res
