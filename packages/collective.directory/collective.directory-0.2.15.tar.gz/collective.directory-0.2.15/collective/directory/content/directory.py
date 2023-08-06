# -*- coding: utf-8 -*-

from collective.directory import _
from collective.geo.leaflet import geomap
from five import grok
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope import schema

import json


grok.templatedir('templates')


class IDirectory(model.Schema):
    """
    A "Directory", directories can contain "Category"s
    """

    title = schema.TextLine(
        title=_(u"Directory name"),
    )

    description = schema.Text(
        title=_(u"Directory summary"),
        required=False,
    )


class Directory(grok.View):
    grok.context(IDirectory)
    grok.require('zope2.View')

    def __init__(self, context, request):
        super(Directory, self).__init__(context, request)
        self.geomap = geomap.GeoMap(context)

    def get_directory_geojsons_url(self):
        return "{}/@@geo-json.json".format(self.context.absolute_url())

    def get_simple_directory_geojson_urls(self):
        results = []
        catalog = getToolByName(self.context, 'portal_catalog')
        query_dict = {}
        directory = {}
        # XXX should not wake up object
        directory['name'] = self.context.title
        directory['icon'] = ""
        query_dict = {}
        query_dict['portal_type'] = 'collective.directory.category'
        query_dict['path'] = {'query': "/".join(self.context.getPhysicalPath()), 'depth': 1}
        query_dict['sort_on'] = 'sortable_title'
        directory['contents'] = []
        for brain in catalog(query_dict):
            directory['contents'].append({
                'name': brain.getObject().title,
                'url': "{}/@@geo-json.json".format(brain.getURL()),
                'icon': ''
            })

        results.append(directory)
        return json.dumps(results)

    def get_all_directories_geojson_urls(self):
        results = []
        catalog = getToolByName(self.context, 'portal_catalog')
        query_dict = {}
        query_dict['portal_type'] = 'collective.directory.directory'
        brains = catalog(query_dict)
        for brain in brains:
            directory = {}
            # XXX should not wake up object
            directory['name'] = brain.getObject().title
            directory['icon'] = ""
            query_dict = {}
            query_dict['portal_type'] = 'collective.directory.category'
            query_dict['path'] = {'query': brain.getPath(), 'depth': 1}
            query_dict['sort_on'] = 'sortable_title'
            directory['contents'] = []
            for brain in catalog(query_dict):
                directory['contents'].append({
                    'name': brain.getObject().title,
                    'url': "{}/@@geo-json.json".format(brain.getURL()),
                    'icon': ''
                })

            results.append(directory)
        return json.dumps(results)
