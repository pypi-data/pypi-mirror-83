# -*- coding: utf-8 -*-
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite


def getPloneSiteMemcachedDefaultNameSpace():
    site = getSite()
    if site is not None:
        return IUUID(site, None)
