# -*- coding: utf-8 -*-

import unittest

from zope.component import createObject
from zope.component import queryUtility
from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from collective.directory.content.directory import IDirectory
from collective.directory.testing import COLLECTIVE_DIRECTORY_INTEGRATION_TESTING

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IWriteGeoreferenced


class TestDirectoryIntegration(unittest.TestCase):
    """Integration test for the Directory type
    """

    layer = COLLECTIVE_DIRECTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('collective.directory.directory', 'directory1')
        d1 = self.folder['directory1']
        self.assertTrue(IDirectory.providedBy(d1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.directory')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.directory')
        schema = fti.lookupSchema()
        self.assertEqual(IDirectory, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.directory')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IDirectory.providedBy(new_object))

    def test_view(self):
        self.folder.invokeFactory('collective.directory.directory', 'directory1')
        d1 = self.folder['directory1']
        view = d1.restrictedTraverse('@@directory')
        self.assertNotEquals(None, view)

    def test_jsonview(self):
        self.folder.invokeFactory('collective.directory.directory', 'directory1')
        directory1 = self.folder.get('directory1')
        directory1.invokeFactory('collective.directory.category', 'category1')
        category1 = directory1.get('category1')
        category1.invokeFactory('collective.directory.card', 'card1')
        category1.invokeFactory('collective.directory.card', 'card2')
        card1 = category1.get('card1')
        card2 = category1.get('card2')

        alsoProvides(card1, IGeoreferenceable)
        alsoProvides(card2, IGeoreferenceable)
        geo1 = IWriteGeoreferenced(card1)
        geo2 = IWriteGeoreferenced(card2)

        geo1.setGeoInterface('Point', (5.583, 50.633))
        geo2.setGeoInterface('Point', (5.593, 50.643))
        card1.reindexObject(idxs=['zgeo_geometry', 'collective_geo_styles'])
        card2.reindexObject(idxs=['zgeo_geometry', 'collective_geo_styles'])

        d1 = self.folder['directory1']
        view = d1.restrictedTraverse('@@json.js')
        js = view.get_categories()
        self.assertIn('"coordinates": [5.583, 50.633]', js)

    def test_jsonview_card_in_card(self):
        self.folder.invokeFactory('collective.directory.directory', 'directory1')
        directory1 = self.folder.get('directory1')
        directory1.invokeFactory('collective.directory.category', 'category1')
        category1 = directory1.get('category1')
        category1.invokeFactory('collective.directory.card', 'card1')
        card1 = category1.get('card1')
        card1.invokeFactory('collective.directory.card', 'card2')
        card2 = card1.get('card2')

        alsoProvides(card1, IGeoreferenceable)
        alsoProvides(card2, IGeoreferenceable)
        geo1 = IWriteGeoreferenced(card1)
        geo2 = IWriteGeoreferenced(card2)

        geo1.setGeoInterface('Point', (5.583, 50.633))
        geo2.setGeoInterface('Point', (5.593, 50.643))
        card1.reindexObject(idxs=['zgeo_geometry', 'collective_geo_styles'])
        card2.reindexObject(idxs=['zgeo_geometry', 'collective_geo_styles'])

        d1 = self.folder['directory1']
        view = d1.restrictedTraverse('@@json.js')
        js = view.get_categories()
        self.assertIn('"coordinates": [5.593, 50.643]', js)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
