# -*- coding: utf-8 -*-
from collections import OrderedDict
from collective.directory import _
from collective.geo.geographer.interfaces import IGeoreferenced
from cStringIO import StringIO
from plone import api
from plone.directives import form

import csv
import logging
import time
import types

logger = logging.getLogger('collective.directory export into csv')

help_text = u"""
<p>
You can export card to a csv file.
</p>
"""


class ICollectiveDirectoryExportForm(form.Schema):
    """ Define form fields """


class CollectiveDirectoryExportForm(form.SchemaForm):
    """ Define Form handling """
    name = _(u"Export directory")
    schema = ICollectiveDirectoryExportForm
    ignoreContext = True

    label = u"Export directory to CSV file"

    description = help_text

    def __init__(self, context, request):
        """ To get the workflow_state in csv, add ?workflow_state=true in url.
            You can add others card's properties in url.
        """
        super(CollectiveDirectoryExportForm, self).__init__(context, request)
        self.nb_csv_row = 0
        self.csv_page_header = OrderedDict([
            ('title', 'title'),
            ('subtitle', 'subtitle'),
            ('address', 'address'),
            ('zip_code', 'zip_code'),
            ('city', 'city'),
            ('phone', 'phone'),
            ('mobile_phone', 'mobile_phone'),
            ('fax', 'fax'),
            ('email', 'email'),
            ('website', 'website'),
            ('description', 'description'),
            ('latitude', 'lat'),
            ('longitude', 'lon'),
            ('category', 'collective_directory_category')
        ])
        self._clean_csv_page_header()

    def __call__(self):
        name = self.context.id
        value = self.get_formated_csv_data()
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment;filename=%s-%s.csv' % (name, time.strftime("%Y%m%d-%H%M")))
        return value

    def _clean_csv_page_header(self):
        """ __init__ : delete or add dictionnary entries thanks to httprequest value """
        for key, value in self.request.form.items():
            if value.upper() == 'FALSE':
                if key in self.csv_page_header.keys():
                    del self.csv_page_header[key]
            if value.upper() == 'TRUE':
                self.csv_page_header.update({key: key})

    def _build_brains(self):
        """ return all cards in brains """
        directory_path = self.context.getPhysicalPath()
        catalog = api.portal.get_tool(name="portal_catalog")
        brains = catalog.searchResults(path={"query": "/".join(directory_path)},
                                       portal_type='collective.directory.card',
                                       sort_on='sortable_title',
                                       sort_order='ascending')
        return brains

    def _get_card_workflow_state(self, card):
        """ Get current workflow state for a card. """
        return api.content.get_state(card)


    def get_formated_csv_data(self):
        """ Get a csv buffer value with all formated cards from directory. """
        buffer = StringIO()
        writer = csv.writer(buffer)
        brains = self._build_brains()
        writer.writerow(self.csv_page_header.keys())
        for brain in brains:
            card = brain.getObject()
            row = []
            for key, value in self.csv_page_header.iteritems():
                if key == 'workflow_state':
                    attr_value = self._get_card_workflow_state(card)
                elif key == 'latitude' or key == 'longitude':
                    geo = IGeoreferenced(card)
                    if geo.coordinates:
                        coord = {'lat': geo.coordinates[1], 'lon': geo.coordinates[0]}
                    else:
                        coord = {'lat': '', 'lon': ''}
                    attr_value = unicode(coord[value])
                else:
                    attr_value = getattr(card, value, '')
                if isinstance(attr_value, types.MethodType):
                    attr_value = getattr(card, value)()
                attr_value = self._encoding(attr_value)
                row.append(attr_value)
            writer.writerow(row)
            self.nb_csv_row = self.nb_csv_row + 1
        value = buffer.getvalue()
        value = unicode(value, "utf-8")
        return value

    def _encoding(self, value):
        val = unicode(value)
        if val == 'None':
            val = u""
        val = val.encode('utf8')
        return val

