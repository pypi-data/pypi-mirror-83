# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer

from collective.directory import _
from collective.directory.content.card import ICard


def get_first_parent_by_type(obj, portal_type):
    parent = obj.__parent__
    if parent.portal_type == portal_type:
        return parent
    elif parent.portal_type == 'Plone Site':
        return None
    else:
        return get_first_parent_by_type(parent, portal_type)


@indexer(ICard)
def directory(card):
    """
    Get first directory parent id
    """
    parent = get_first_parent_by_type(card, 'collective.directory.directory')
    if not parent:
        raise TypeError(_(u"Card must always be in a Directory"))
    return parent and parent.id or None


@indexer(ICard)
def category(card):
    """
    Get first category parent id
    """
    parent = get_first_parent_by_type(card, 'collective.directory.category')
    if not parent:
        raise TypeError(_(u"Card must always be in a Category"))
    return parent and parent.id or None
