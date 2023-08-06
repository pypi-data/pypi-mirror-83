# -*- coding: utf-8 -*-

from plone.testing import z2
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import collective.directory

from plone.app.testing import applyProfile


class CollectiveDirectoryPloneWithPackageLayer(PloneWithPackageLayer):
    """
    """

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(portal, 'collective.directory:testing')


COLLECTIVE_DIRECTORY_FIXTURE = CollectiveDirectoryPloneWithPackageLayer(
    name="COLLECTIVE_DIRECTORY_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=collective.directory,
    gs_profile_id="collective.directory:testing")

COLLECTIVE_DIRECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DIRECTORY_FIXTURE,),
    name="collective.directory:Integration")

COLLECTIVE_DIRECTORY_ROBOT_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DIRECTORY_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="collective.directory:Robot")
