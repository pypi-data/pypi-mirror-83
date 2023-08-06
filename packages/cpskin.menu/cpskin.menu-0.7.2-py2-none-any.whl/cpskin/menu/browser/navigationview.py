# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides

from cpskin.locales import CPSkinMessageFactory as _

from cpskin.menu.browser.menu import invalidate_menu
from cpskin.menu.interfaces import IFourthLevelNavigation
from cpskin.menu.interfaces import IMultiLevelNavigationView


class MultiLevelNavigationView(BrowserView):
    """ Multi level navitation helper view
    """
    implements(IMultiLevelNavigationView)

    def _redirect(self, msg=''):
        """ Redirect
        """
        if self.request:
            if msg:
                api.portal.show_message(message=msg,
                                        request=self.request,
                                        type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    def _get_real_context(self):
        context = self.context
        plone_view = getMultiAdapter((context, self.request), name="plone")
        if plone_view.isDefaultPageInFolder():
            context = aq_parent(context)
        context = aq_inner(context)
        return context

    @property
    def can_enable_fourth_level(self):
        """ Helper method used by the actions to know if they should
        be displayed or not
        """
        context = self._get_real_context()

        sm = getSecurityManager()
        if not sm.checkPermission("Portlets: Manage portlets", context):
            return False
        contextPhyPath = context.getPhysicalPath()
        portalPhyPath = api.portal.get().getPhysicalPath()
        path = [elem for elem in list(contextPhyPath) if elem not in list(portalPhyPath)]
        depth = len(path)
        if depth == 3 and not IFourthLevelNavigation.providedBy(context):
            return True
        else:
            return False

    @property
    def is_enabled(self):
        context = self._get_real_context()
        return IFourthLevelNavigation.providedBy(context)

    @property
    def can_disable_fourth_level(self):
        """ Return True if the fourth menu level is enable in this context
        """
        context = self._get_real_context()
        sm = getSecurityManager()
        return self.is_enabled and sm.checkPermission("Portlets: Manage portlets", context)

    def enable_fourth_level(self):
        """ Enable the 4th level navigation """
        context = self._get_real_context()
        alsoProvides(context, IFourthLevelNavigation)
        self._redirect(_(u'4th level navigation enabled on content'))
        invalidate_menu(context)

    def disable_fourth_level(self):
        """ Disable the 4th level navigation """
        context = self._get_real_context()
        noLongerProvides(context, IFourthLevelNavigation)
        self._redirect(_(u'4th level navigation disabled on content'))
        invalidate_menu(context)
