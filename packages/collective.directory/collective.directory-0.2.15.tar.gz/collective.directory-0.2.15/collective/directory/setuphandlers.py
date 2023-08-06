# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
from plone import api
from collective.geo.geographer.interfaces import IWriteGeoreferenced

logger = logging.getLogger('collective.directory')


def installCore(context):
    if context.readDataFile('collective.directory-default.txt') is None:
        return

    logger.info('Installing')
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    # Reindex new indexes
    catalog.manage_reindexIndex('directory')
    catalog.manage_reindexIndex('category')


def testSetup(context):
    if context.readDataFile('collective_directory_test.txt') is None:
        return
    portal = context.getSite()
    if 'directories' not in portal.objectIds():
        directories_folder = api.content.create(
            container=portal,
            type='Folder',
            id='directories',
            title='Directories'
        )
        api.content.transition(obj=directories_folder, transition='publish')
        make_contents(directories_folder)

    if 'map' not in portal.objectIds():
        map_collection = api.content.create(
            type="Collection",
            container=portal,
            title="Map",
            id="map"
        )
        api.content.transition(obj=map_collection, transition='publish')
        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': ['collective.directory.card']
        }]
        map_collection.setQuery(query)


def make_contents(container):
    directories = {
        'Sports': {
            'Football': {
                'FC Mornimont': {'lat': 4.7143225, 'lon': 50.45635089999998},
                'RFC Mornimont': {'lat': 4.7243225, 'lon': 50.45635089999998},
            },
            'Hockey': {
                'Mornimont HC': {'lat': 4.7343225, 'lon': 50.45635089999998},
            },
        },
        'Assosiations': {
            'Divers': {
                'Scouts': {'lat': 4.7443225, 'lon': 50.45635089999998},
                'Patro': {'lat': 4.7543225, 'lon': 50.45635089999998},
            }
        },
    }
    for directory_title in directories.keys():
        directory_folder = api.content.create(
            container=container,
            type="collective.directory.directory",
            title=directory_title,
        )
        api.content.transition(obj=directory_folder, transition='publish')
        categories = directories[directory_title]
        for category_title in categories.keys():
            category_folder = api.content.create(
                container=directory_folder,
                type="collective.directory.category",
                title=category_title,
            )
            api.content.transition(obj=category_folder, transition='publish')
            cards = categories[category_title]
            for card_title in cards.keys():
                card = cards[card_title]
                card_container = api.content.create(
                    container=category_folder,
                    type="collective.directory.card",
                    title=card_title,
                )
                api.content.transition(
                    obj=card_container,
                    transition='publish'
                )
                geo = IWriteGeoreferenced(card_container)
                geo.setGeoInterface('Point', (card['lat'], card['lon']))
                card_container.reindexObject(idxs=['zgeo_geometry', 'collective_geo_styles'])
