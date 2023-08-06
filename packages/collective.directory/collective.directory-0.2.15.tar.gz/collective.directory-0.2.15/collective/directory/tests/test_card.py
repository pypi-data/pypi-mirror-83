# -*- coding: utf-8 -*-

import unittest

from zope.component import createObject
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from collective.directory.content.card import ICard
from collective.directory.testing import COLLECTIVE_DIRECTORY_INTEGRATION_TESTING


class TestCardIntegration(unittest.TestCase):
    """Integration test for the Card type
    """

    layer = COLLECTIVE_DIRECTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = getToolByName(self.portal, 'portal_workflow')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('collective.directory.directory', 'directory1')
        self.directory = self.folder['directory1']
        self.directory.invokeFactory('collective.directory.category', 'category1')
        self.category = self.directory['category1']

    def test_adding(self):
        self.category.invokeFactory('collective.directory.card', 'card1')
        c1 = self.category['card1']
        self.assertTrue(ICard.providedBy(c1))

        c1.invokeFactory('collective.directory.card', 'card2')
        c2 = c1['card2']
        self.assertTrue(ICard.providedBy(c2))

    def test_disallowed_adding(self):
        # XXX I have to find the way to disallow adding 'card' into something
        # else that category childrens and subchildrens
        self.assertRaises(ValueError, self.folder.invokeFactory, 'collective.directory.card', 'card1')
        self.assertRaises(ValueError, self.directory.invokeFactory, 'collective.directory.card', 'card2')

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.card')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.card')
        schema = fti.lookupSchema()
        self.assertEqual(ICard, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.directory.card')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ICard.providedBy(new_object))

    def test_view(self):
        self.category.invokeFactory('collective.directory.card', 'card1')
        c1 = self.category['card1']
        listingview = c1.restrictedTraverse('@@listingcards')
        self.assertNotEquals(None, listingview)

        detailview = c1.restrictedTraverse('@@detailcard')
        self.assertNotEquals(None, detailview)

    def test_getSubCards(self):
        self.category.invokeFactory('collective.directory.card', 'card1')
        self.category.invokeFactory('collective.directory.card', 'card2')
        c1 = self.category['card1']
        c2 = self.category['card2']

        self.portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        workflowTool = getToolByName(self.portal, 'portal_workflow')
        workflowTool.doActionFor(c1, 'publish')
        workflowTool.doActionFor(c2, 'publish')

        listingview = self.category.restrictedTraverse('@@listingcards')
        cards = listingview.getSubCards()
        self.assertEqual(len(cards), 2)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
