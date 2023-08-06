# -*- coding: utf-8 -*-

import unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from collective.directory.content.category import ICategory
from collective.directory.testing import COLLECTIVE_DIRECTORY_INTEGRATION_TESTING


class TestCategoryIntegration(unittest.TestCase):
    """Integration test for the Category type
    """

    layer = COLLECTIVE_DIRECTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('collective.directory.directory', 'directory1')
        self.directory = self.folder['directory1']

    def test_adding(self):
        self.directory.invokeFactory('collective.directory.category', 'category1')
        c1 = self.directory['category1']
        self.assertTrue(ICategory.providedBy(c1))

    def test_disallowed_adding(self):
        self.assertRaises(ValueError, self.folder.invokeFactory, 'collective.directory.category', 'category1')

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.category')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.category')
        schema = fti.lookupSchema()
        self.assertEqual(ICategory, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.category')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ICategory.providedBy(new_object))

    def test_view(self):
        self.directory.invokeFactory('collective.directory.category', 'category1')
        c1 = self.directory['category1']
        view = c1.restrictedTraverse('@@listingcards')
        self.assertNotEquals(None, view)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
