# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.interface import alsoProvides
from plone.uuid.interfaces import IAttributeUUID, IMutableUUID, IUUIDGenerator


def addUUIDOnPortal(portal):
    if not IAttributeUUID.providedBy(portal):
        alsoProvides(portal, IAttributeUUID)
    uuid_adapter = IMutableUUID(portal)
    if uuid_adapter.get() is None:
        generator = getUtility(IUUIDGenerator)
        uuid = generator()
        uuid_adapter.set(uuid)


def installMenu(context):
    if context.readDataFile('cpskin.menu-default.txt') is None:
        return

    portal = context.getSite()
    addUUIDOnPortal(portal)
