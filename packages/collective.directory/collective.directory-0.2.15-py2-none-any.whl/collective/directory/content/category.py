# -*- coding: utf-8 -*-

from collective.directory import _
from five import grok
from plone.supermodel import model
from zope import schema
from collective.directory.content.card import ListingCardsMixin


grok.templatedir('templates')


class ICategory(model.Schema):
    """
    A "Category", categories can contain "Card"s
    """

    title = schema.TextLine(
        title=_(u"Category name"),
    )

    description = schema.Text(
        title=_(u"Category summary"),
        required=False,
    )


class ListingCards(ListingCardsMixin, grok.View):
    grok.context(ICategory)
    grok.require('zope2.View')
