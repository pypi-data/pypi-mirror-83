# -*- coding: utf-8 -*-
from five import grok
from plone.dexterity.content import Container
from plone.app.textfield import RichText
from plone.directives import dexterity
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.app.dexterity.behaviors.metadata import IBasic
from zope import schema

from collective.directory import _
from collective.schedulefield.schedule import Schedule

from plone.autoform import directives as form


grok.templatedir('templates')


class ICard(model.Schema, IBasic):
    """
    A "Card", directories can contain "Category"s
    """

    subtitle = schema.TextLine(
        title=_(u"Subtitle"),
        required=False,
    )

    address = schema.TextLine(
        title=_(u"Address"),
        description=_(u"Street and number"),
        required=False,
    )

    zip_code = schema.TextLine(
        title=_(u"Zip code"),
        required=False,
    )

    city = schema.TextLine(
        title=_(u"City"),
        required=False,
    )

    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
    )

    mobile_phone = schema.TextLine(
        title=_(u"Mobile phone"),
        required=False,
    )

    fax = schema.TextLine(
        title=_(u"Fax"),
        required=False,
    )

    email = schema.TextLine(
        title=_(u"E-mail"),
        required=False,
    )

    website = schema.TextLine(
        title=_(u"Website"),
        required=False,
    )

    schedule = Schedule(
        title=_(u"Schedule"),
        required=False)

    photo = NamedBlobImage(
        title=_(u"Photo"),
        required=False,
    )

    form.order_before(description='content')

    content = RichText(
        title=_(u"Content"),
        required=False,
    )


def get_first_parent_by_type(obj, portal_type):
    parent = obj.__parent__
    if parent.portal_type == portal_type:
        return parent
    elif parent.portal_type == 'Plone Site':
        return None
    else:
        return get_first_parent_by_type(parent, portal_type)


class Card(Container):
    grok.implements(ICard)

    def collective_directory_category(self):
        parent = get_first_parent_by_type(self, 'collective.directory.category')
        if not parent:
            raise TypeError(_(u"Card must always be in a Category"))
        return parent.id


class DetailCard(dexterity.DisplayForm):
    grok.context(ICard)
    grok.require('zope2.View')


class ListingCardsMixin(object):

    def getSubCards(self):
        portal_type = "collective.directory.card"
        results = self.context.portal_catalog.searchResults(
            portal_type=portal_type,
            path={'query': '/'.join(self.context.getPhysicalPath())},
            sort_on='sortable_title')
        results = [result.getObject() for result in results]

        # remove actual card because path get the actual too, not only the
        # containing objects
        if self.context.portal_type == portal_type:
            if results.count(self.context) >= 1:
                results.remove(self.context)

        return results

    def schedule_render(self, card):
        card_display = dexterity.DisplayForm(card, self.request)
        card_display.update()
        return card_display.w.get('schedule').render()


class ListingCards(ListingCardsMixin, dexterity.DisplayForm):
    grok.context(ICard)
    grok.require('zope2.View')
