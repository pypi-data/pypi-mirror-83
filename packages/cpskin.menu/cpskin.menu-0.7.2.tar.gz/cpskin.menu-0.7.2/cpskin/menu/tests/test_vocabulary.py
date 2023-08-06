# -*- coding: utf-8 -*-

from cpskin.menu import testing
from cpskin.menu.interfaces import IFourthLevelNavigation
from mock import Mock
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory

import unittest


class FakeBrain(object):

    def __init__(self, path, id, title):
        self.path = path
        self.id = id
        self.title = title

    def getPath(self):
        return self.path

    def getObject(self):
        obj_values = {'title': self.title,
                      'aq_parent': type('parent', (object, ), {})()}
        alsoProvides(obj_values['aq_parent'], IFourthLevelNavigation)
        return type('obj', (object, ), obj_values)()


class TestVocabulary(unittest.TestCase):
    layer = testing.CPSKIN_MENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self._getPhysicalPath = self.portal.getPhysicalPath
        self._get_brains = self.vocabulary_factory.get_brains
        self._is_multilingual = self.vocabulary_factory._is_multilingual_site

    def tearDown(self):
        self.vocabulary_factory.get_brains = self._get_brains
        self.vocabulary_factory._is_multilingual_site = self._is_multilingual
        self.portal.getPhysicalPath = self._getPhysicalPath

    @property
    def vocabulary_factory(self):
        return getUtility(IVocabularyFactory,
                          'cpskin.menu.vocabularies.lastlevelnavigation')

    def test_vocabulary(self):
        voc = self.vocabulary_factory(self.portal)
        expected_values = [u'Promenades', u'Bibliothèques', u'Yoyo', u'Tata',
                           u'Rockers', u'Cinema', u'Abba', u'Finances']
        self.assertListEqual(sorted(expected_values), [t.title for t in voc])

    def test_duplicate_title(self):
        brains = [FakeBrain('/plone/1/2/apple-1', 'apple-1', u'Apple'),
                  FakeBrain('/plone/1/2/apple-2', 'apple-2', u'Apple')]
        self.vocabulary_factory.get_brains = Mock(return_value=brains)
        voc = self.vocabulary_factory(self.portal)
        expected_values = [u'Apple', u'Apple']
        self.assertItemsEqual(expected_values, [t.title for t in voc])

    def test_with_mountpoint(self):
        brains = [FakeBrain('/mount/plone/1/2/third', 'third', u'Third'),
                  FakeBrain('/mount/plone/1/2/3/fourth', 'fourth', u'Fourth')]
        self.portal.getPhysicalPath = Mock(return_value=('', 'mount', 'plone'))
        self.vocabulary_factory.get_brains = Mock(return_value=brains)
        voc = self.vocabulary_factory(self.portal)
        expected_values = [u'Third', u'Fourth']
        self.assertItemsEqual(expected_values, [t.title for t in voc])

    def test_with_multilingual(self):
        brains = [
            FakeBrain('/plone/fr/1/2/third', 'third', u'Third'),
            FakeBrain('/plone/fr/1/2/3/fourth', 'fourth', u'Fourth'),
        ]
        self.portal.getPhysicalPath = Mock(return_value=('', 'plone'))
        self.vocabulary_factory.get_brains = Mock(return_value=brains)
        self.vocabulary_factory._is_multilingual_site = Mock(return_value=True)
        voc = self.vocabulary_factory(self.portal)
        expected_values = [u'Third', u'Fourth']
        self.assertItemsEqual(expected_values, [t.title for t in voc])

    def test_with_multilingual_mountpoint(self):
        brains = [
            FakeBrain('/mount/plone/fr/1/2/third', 'third', u'Third'),
            FakeBrain('/mount/plone/fr/1/2/3/fourth', 'fourth', u'Fourth'),
        ]
        self.portal.getPhysicalPath = Mock(return_value=('', 'mount', 'plone'))
        self.vocabulary_factory.get_brains = Mock(return_value=brains)
        self.vocabulary_factory._is_multilingual_site = Mock(return_value=True)
        voc = self.vocabulary_factory(self.portal)
        expected_values = [u'Third', u'Fourth']
        self.assertItemsEqual(expected_values, [t.title for t in voc])
