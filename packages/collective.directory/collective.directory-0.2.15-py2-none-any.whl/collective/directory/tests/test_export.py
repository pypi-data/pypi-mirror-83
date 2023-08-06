# -*- coding: utf-8 -*-

import unittest

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.directory.testing import COLLECTIVE_DIRECTORY_INTEGRATION_TESTING


class TestExportIntegration(unittest.TestCase):
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
        self.category.invokeFactory('collective.directory.card', 'card1')
        self.category.invokeFactory('collective.directory.card', 'card2')
        self.card1 = self.category['card1']
        self.card2 = self.category['card2']

    def test_view(self):
        view = self.directory.restrictedTraverse('collective_directory_export_view')
        self.assertTrue(view())

    def test_nb_csv_row_is_equal_to_nb_cards(self):
        view = self.directory.restrictedTraverse('collective_directory_export_view')
        view.__call__()
        nb_cards = len(self.category.items())
        self.assertEqual(nb_cards, view.nb_csv_row)

    def test_view_is_request_update_not_in(self):
        view = self.directory.restrictedTraverse('collective_directory_export_view')
        view.request.form = {"address": "false"}
        view._clean_csv_page_header()
        self.assertNotIn("address", view.__call__())

    def test_view_is_request_update_in(self):
        view = self.directory.restrictedTraverse('collective_directory_export_view')
        view.request.form = {"workflow_state": "true"}
        view._clean_csv_page_header()
        self.assertIn("workflow_state", view.__call__())
