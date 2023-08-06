# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class StickyCollectionView(BrowserView):

    def results(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        brains = self.context.queryCatalog()
        results = {'sticky_results': [],
                   'standard_results': []}
        for brain in brains:
            if portal_catalog.getIndexDataForRID(brain.getRID())['is_sticky']:
                results['sticky_results'].append(brain)
            else:
                results['standard_results'].append(brain)
        return results
