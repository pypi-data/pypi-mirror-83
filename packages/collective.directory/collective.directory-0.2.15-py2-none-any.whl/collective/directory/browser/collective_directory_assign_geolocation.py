from collective.geo.behaviour.interfaces import ICoordinates
from geopy.geocoders.osm import Nominatim
from geopy.geocoders.googlev3 import GoogleV3
from geopy.exc import GeocoderTimedOut

from Products.CMFCore.utils import getToolByName

import logging
logger = logging.getLogger('collective.directory import csv')


class CollectiveDirectoryAssignGeolocation(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.catalog = getToolByName(context, 'portal_catalog', None)
        self.print_bad_location = ""

    def __call__(self):
        self.set_geolocalisation()
        return self.print_bad_location

    def set_geolocalisation(self):
        brains_card = self.catalog.searchResults({'portal_type': 'collective.directory.card'})
        for brain in brains_card:
            card = brain.getObject()
            if not ICoordinates(card).coordinates:
                latlon = self.get_xy_from_address(card)
                url = card.absolute_url()
                if latlon:
                    coord = u"POINT({0} {1})".format(latlon['lon'], latlon['lat'])
                    ICoordinates(card).coordinates = coord
                    self.print_bad_location += "GOOD => <a href=" + url + ">" + url + "</a><br>"
                else:
                    self.print_bad_location += "BAD => <a href=" + url + ">" + url + "</a><br>"
            card.reindexObject()

    def get_xy_from_address(self, card):
        location = None
        if card.address is not None and card.city is not None:
            address = "{} {} {}".format(card.address.encode('utf8'), card.zip_code, card.city.encode('utf8'))
            location = get_address(Nominatim(), address, 'OSM')
            if not location:
                location = get_address(GoogleV3(), address, 'Google')
            if not location:
                return
        return location


def get_address(geolocator, address, geolocator_name):
    try:
        location = geolocator.geocode(address)
    except GeocoderTimedOut:
        logger.error("{} timeout".format(geolocator_name))
        return False
    if not location:
        logger.error("{} didn't know this address '{}'".format(geolocator_name, address))
        return False
    return {'lat': location.latitude, 'lon': location.longitude}
