# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
import logging
logger = logging.getLogger('collective.directory.upgrades')


def update_profile(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-collective.directory:default')


def upgrade_1_to_2(context):
    # setup = getToolByName(context, 'portal_setup')
    # setup.runAllImportStepsFromProfile('profile-collective.directory:default')
    rename_ids("collective.directory.directory", context)
    rename_ids("collective.directory.category", context)


def rename_ids(pt, context):
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.searchResults({'portal_type': pt})
    for brain in brains:
        logger.info(brain.getURL())
        if brain.getId.startswith(pt.replace('.', '-')):
            obj = brain.getObject()
            old_id = obj.id
            title = obj.Title()
            logger.info('old id : {}, title : {}'.format(old_id, title))
            api.content.rename(obj=obj, new_id=title, safe_id=True)
            obj.reindexObject()


def add_collective_directory_category_metadata(context):
    update_profile(context)
    catalog = getToolByName(context, 'portal_catalog')
    portal_type = "collective.directory.card"
    brains = catalog.searchResults(portal_type=portal_type)

    for brain in brains:
        obj = brain.getObject()
        from collective.directory.content.card import Card
        obj.__class__ = Card
        obj.reindexObject()
    logger.info("{} {} updated".format(len(brains), portal_type))


def update_3_to_4(context):
    update_profile(context)


def set_translatable(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-collective.directory:default')


def update_5_to_6(context):
    context.runImportStepFromProfile('profile-collective.directory:default', 'typeinfo')
