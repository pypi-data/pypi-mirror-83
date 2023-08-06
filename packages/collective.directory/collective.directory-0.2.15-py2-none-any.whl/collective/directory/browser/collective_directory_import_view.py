from collective.directory import _
from collective.geo.behaviour.interfaces import ICoordinates

from geopy.geocoders.osm import Nominatim
from geopy.geocoders.googlev3 import GoogleV3
from geopy.geocoders.openmapquest import OpenMapQuest
from geopy.exc import GeocoderTimedOut

from plone import api
from plone.app.textfield.value import RichTextValue
from plone.directives import form
from plone.namedfile.field import NamedFile

from z3c.form import button

import StringIO
import copy
import csv
import logging
import unicodedata

logger = logging.getLogger('collective.directory import csv')


fields = (
    u'title',
    u'description',
    u'category',
    u'subtitle',
    u'address',
    u'zip_code',
    u'city',
    u'phone',
    u'mobile_phone',
    u'fax',
    u'email',
    u'website',
)

help_text = u"""
<p>
You can import card from a csv file. This csv file should contains header :
    <ul>
        <li>title</li>
        <li>description</li>
        <li>category</li>
        <li>subtitle</li>
        <li>address</li>
        <li>zip_code</li>
        <li>city</li>
        <li>phone</li>
        <li>mobile_phone</li>
        <li>fax</li>
        <li>email</li>
        <li>website</li>
    </ul>
Other column will be added into content.
For importing card, add your csv in the form below
</p>
"""


class ICollectiveDirectoryImportForm(form.Schema):
    """ Define form fields """

    csv_file = NamedFile(
        title=_(u"CSV file"),
        description=_(u'Import csv file for card creation')
    )


class CollectiveDirectoryImportForm(form.SchemaForm):
    """ Define Form handling """
    name = _(u"Import directory")
    schema = ICollectiveDirectoryImportForm
    ignoreContext = True

    label = u"Import directory from CSV file"

    description = help_text

    def process_csv(self, data):
        """
        """
        io = StringIO.StringIO(data)

        reader = csv.reader(io, delimiter=';', dialect="excel", quotechar='"')
        header = reader.next()

        def get_cell(row, name):
            """ Read one cell on a
            @param row: CSV row as list
            @param name: Column name: 1st row cell content value, header
            """
            assert type(name) == unicode, "Column names must be unicode"
            index = None
            for i in range(0, len(header)):
                if header[i].decode("utf-8") == name:
                    index = i
            if index is None:
                #return ""
                raise RuntimeError("CSV data does not have column:" + name)
            if index >= len(row):
                return ""
            else:
                return row[index].decode("utf-8")

        updated = 0
        for row in reader:
            headers = copy.deepcopy(header)
            category_name = get_cell(row, u'category')
            category = self.create_category(category_name)

            card_title = get_cell(row, u'title')
            card = api.content.create(
                type='collective.directory.card',
                title=card_title,
                container=category
            )
            headers.remove('title')
            zip_code = get_cell(row, u'zip_code')
            if zip_code:
                card.zip_code = zip_code
            headers.remove('zip_code')
            for field in fields:
                if field in headers:
                    value = get_cell(row, field)
                    setattr(card, field, value)
                    try:
                        headers.remove(field)
                    except ValueError:
                        logger.error("{} not in {}".format(field, headers))

            contents = ['<p>']
            for head in headers:
                value = get_cell(row, unicode(head))
                try:
                    contents.append("{} : {} <br />".format(head, value))
                except UnicodeEncodeError:
                    contents.append("{} : {} <br />".format(head, value.encode('utf8')))
            contents.append('</p>')
            card.content = RichTextValue(unicode("".join(contents), 'utf8'))

            latlon = self.get_xy_from_address(card)
            if latlon:
                coord = u"POINT({0} {1})".format(latlon['lon'], latlon['lat'])
                ICoordinates(card).coordinates = coord
            self.publish(card)
            updated += 1
            logger.info("{}: {} added".format(updated, card.title.encode('utf8')))
        return updated

    @button.buttonAndHandler(_(u'Import'), name='import')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        csv_file = data["csv_file"].data
        number = self.process_csv(csv_file)
        self.status = "File uploaded with {} new objects.".format(number)

    def create_category(self, category_name):
        context = self.context
        category_id = clean_special_chars(category_name)
        if category_id in context.keys():
            return context.get(category_id)
        else:
            category = api.content.create(
                type='collective.directory.category',
                id=category_id,
                title=category_name,
                container=context
            )
            self.publish(category)
            return category

    def publish(self, obj):
        workflow = api.portal.get_tool('portal_workflow')
        transitions = [
            action['id'] for action in workflow.listActions(object=obj)
        ]
        publish_and_hide = 'publish_and_hide'
        if publish_and_hide in transitions:
            api.content.transition(obj=obj, transition=publish_and_hide)
        else:
            api.content.transition(obj=obj, transition='publish')

    def get_xy_from_address(self, card):
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


def clean_special_chars(str):
    return_string = str
    if type(str) is unicode:
        nkfd_form = unicodedata.normalize('NFKD', str)
        return_string = nkfd_form.encode('ASCII', 'ignore')
    if "&" in return_string:
        return_string = return_string.replace("&", _(u"and"))
    chars_to_remove = (":]+<['>|\\/$?")
    for char in chars_to_remove:
        return_string = return_string.replace(char, "")
    return return_string
