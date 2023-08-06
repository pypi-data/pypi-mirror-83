# -*- coding: utf-8 -*-
import logging
from collective.geo.behaviour.interfaces import ICoordinates
from plone import api
from plone.app.textfield.value import RichTextValue
logger = logging.getLogger('collective.directory.migrate')
MIGRATE_CONTAINER = 'directory'


def migrate_from_products_directory(context):
    if context.readDataFile('collective.directory-migration.txt') is None:
        return

    portal = context.getSite()

    qi_tool = api.portal.get_tool(name='portal_quickinstaller')
    pid = 'collective.directory'
    installed = [p['id'] for p in qi_tool.listInstalledProducts()]
    if pid not in installed:
        setup = api.portal.get_tool(name='portal_setup')
        setup.runAllImportStepsFromProfile('profile-collective.directory:default')

    if MIGRATE_CONTAINER not in portal.keys():
        migrate_container = api.content.create(
            type='Folder',
            title=MIGRATE_CONTAINER,
            container=portal
        )
    catalog = api.portal.get_tool(name="portal_catalog")
    query = {}

    portal_directory = portal.get('portal_directory')
    if not portal_directory:
        return
    directories = portal_directory.keys()
    categories = get_categories(portal_directory)

    query['portal_type'] = directories
    brains = catalog(query)
    for brain in brains:
        card = brain.getObject()
        directory = create_directory(migrate_container, card.portal_type)
        category = create_category(directory, categories, card)
        create_card(category, card)


def create_card(category, card):
    new_card = api.content.create(
        type='collective.directory.card',
        title=card.title,
        container=category
    )

    # key is old field, value is new field
    mapping = {
        'description': 'description',
        'street': 'address',
        'commune': 'city',
        'phone': 'phone',
        'mobile': 'mobile_phone',
        'fax': 'fax',
        'email': 'email',
        'websiteurl': 'website',
    }
    for field in mapping.keys():
        new_field = mapping[field]
        setattr(new_card, new_field, getattr(card, field))

    if card.zip:
        new_card.zip_code = int(card.zip)
    else:
        logger.warn("{} has no zip code.".format(new_card.id))

    opening_hours = ""
    if card.opening_hours:
        opening_hours = card.opening_hours.getRaw()

    content = "{0}<br />{1}".format(card.presentation(), opening_hours)
    content = RichTextValue(unicode(content, 'utf8'))
    new_card.content = content
    logo = card.getLogo()
    if logo:
        pass
        # XXX TODO
        # imageField.getRaw(news) == logo
#         from collective.directory.content.card import ICard
#         filename = logo.filename
#         content_type = logo.getContentType()
#         import pdb;pdb.set_trace()
#         new_card.photo = ICard.photo._type(
#             str(logo),
#             contentType=content_type, filename=filename)

#         new_card.photo = logo

    if card.Coordinates:
        lat, lon = card.Coordinates.split('|')
        coord = u"POINT({0} {1})".format(lon, lat)
    else:
        logger.warn("{} has no coordinates.".format(new_card.id))
    ICoordinates(new_card).coordinates = coord
    api.content.transition(obj=new_card, transition='publish_and_hide')
    logger.info("{} is migrated.".format(new_card.id))


def create_directory(container, folder_name):
    if folder_name in container.keys():
        return container.get(folder_name)
    else:
        return api.content.create(
            type='collective.directory.directory',
            title=folder_name,
            container=container
        )


def create_category(directory, categories_list, card):
    if len(card.category) != 1:
        logger.error('Multi category: {} for {}'.format(card.category, card.id))
    category_name = card.category[0]
    category_title = categories_list.get(category_name)

    if category_name in directory.keys():
        return directory.get(category_name)
    else:
        category = api.content.create(
            type='collective.directory.category',
            id=category_name,
            title=category_title,
            container=directory
        )
        api.content.transition(obj=category, transition='publish_and_hide')
        return category


def get_categories(portal_directory):
    '''Return dict of all categories
    '''
    categories = {}
    for key in portal_directory.keys():
        directory = portal_directory.get(key)
        for category in directory.categories().split('\r\n'):
            dictkey, dictvalue = category.split('|')
            categories[dictkey] = dictvalue
    return categories
