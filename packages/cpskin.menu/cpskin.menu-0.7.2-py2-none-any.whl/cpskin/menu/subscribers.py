# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from cpskin.menu.browser.menu import invalidate_menu
from plone import api
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite


def content_has_id(content):
    try:
        content.getId()
    except AttributeError:
        return False
    else:
        return True


def object_is_wrapped(content):
    return len(aq_chain(content)) > 1


def content_modified(content, event):
    if not content_has_id(content):
        return
    if not object_is_wrapped(content):
        return
    try:
        current_state = api.content.get_state(content)
    except:
        return
    new_state = None
    old_state = None
    if getattr(event, 'new_state', None):
        new_state = event.new_state.id
    if getattr(event, 'old_state', None):
        old_state = event.old_state.id
    # published_and_hidden added to invalidate menu no more show
    # if state not in ['published_and_shown', 'published_and_hidden']:
    if'published_and_shown' not in [new_state, old_state, current_state]:
        return
    portal_properties = api.portal.get_tool('portal_properties')
    navtree_properties = portal_properties.get('navtree_properties', None)
    if navtree_properties:
        metaTypesNotToList = list(navtree_properties.metaTypesNotToList)
        if getattr(content, 'portal_type', None) in metaTypesNotToList:
            return
    if IUUID(getSite(), None) is not None:
        invalidate_menu(content)
