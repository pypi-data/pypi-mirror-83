# -*- coding: utf-8 -*-
from plone import api
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class BasePortalTypeVocabulary(object):
    """Vocabulary factory depending on portal_type"""
    implements(IVocabularyFactory)
    portal_type = ''

    def __call__(self, context, query=None):
        catalog = api.portal.get_tool('portal_catalog')
        if catalog is None:
            return SimpleVocabulary([])

        brains = catalog.searchResults(portal_type=self.portal_type)
        items = []
        for brain in brains:
            obj = brain.getObject()
            items.append(SimpleTerm(obj.id, obj.id, obj.title))
        return SimpleVocabulary(items)


class DirectoryVocabulary(BasePortalTypeVocabulary):
    """Vocabulary factory listing all directory"""
    portal_type = 'collective.directory.directory'


class CategoryVocabulary(BasePortalTypeVocabulary):
    """Vocabulary factory listing all category"""
    portal_type = 'collective.directory.category'


DirectoryVocabularyFactory = DirectoryVocabulary()
CategoryVocabularyFactory = CategoryVocabulary()
