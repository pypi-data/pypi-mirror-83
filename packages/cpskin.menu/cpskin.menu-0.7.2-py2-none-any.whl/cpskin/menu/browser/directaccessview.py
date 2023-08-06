from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides

from cpskin.locales import CPSkinMessageFactory as _

from cpskin.menu.browser.menu import invalidate_menu
from cpskin.menu.interfaces import IDirectAccess
from cpskin.menu.interfaces import IDirectAccessView


class DirectAccessView(BrowserView):
    """ Direct access helper view
    """
    implements(IDirectAccessView)

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
    def can_enable_direct_access(self):
        """ Helper method used by the actions to know if they should
        be displayed or not
        """
        context = self._get_real_context()

        sm = getSecurityManager()
        if not sm.checkPermission("Portlets: Manage portlets", context):
            return False

        depth = len(context.getPhysicalPath()[2:])
        if depth >= 3 and not IDirectAccess.providedBy(context):
            return True
        else:
            return False

    @property
    def is_enabled(self):
        context = self._get_real_context()
        return IDirectAccess.providedBy(context)

    @property
    def can_disable_direct_access(self):
        """ Return True if the direct access is enable in this context
        """
        context = self._get_real_context()
        sm = getSecurityManager()
        return self.is_enabled and sm.checkPermission("Portlets: Manage portlets", context)

    def enable_direct_access(self):
        """ Enable the direct access """
        context = self._get_real_context()
        alsoProvides(context, IDirectAccess)
        catalog = getToolByName(context, 'portal_catalog')
        catalog.reindexObject(context)
        self._redirect(_(u'Content added to direct access menu'))
        invalidate_menu(context)

    def disable_direct_access(self):
        """ Disable the direct access """
        context = self._get_real_context()
        noLongerProvides(context, IDirectAccess)
        catalog = getToolByName(context, 'portal_catalog')
        catalog.reindexObject(context)
        self._redirect(_(u'Content removed from direct access menu'))
        invalidate_menu(context)
