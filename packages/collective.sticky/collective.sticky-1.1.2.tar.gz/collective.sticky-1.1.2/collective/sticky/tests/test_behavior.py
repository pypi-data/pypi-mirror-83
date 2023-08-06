# -*- coding: utf-8 -*-
import unittest
from collective.sticky.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter


class BehaviorTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_behavior(self):
        portal = self.layer['portal']

        stickynews = portal['stickynews']
        simplenews = portal['simplenews']
        self.assertTrue(stickynews.sticky)
        self.assertFalse(simplenews.sticky)

    def test_collection_results(self):
        portal = self.layer['portal']
        request = self.layer['request']
        view = getMultiAdapter(
            (portal.collection, request),
            name="sticky_summary_view"
        )
        results = view.results()
        self.assertEqual(len(results['sticky_results']), 1)
        self.assertEqual(len(results['standard_results']), 1)

        simplenews = portal['simplenews']
        simplenews.sticky = True
        simplenews.reindexObject()
        self.assertTrue(simplenews.sticky)

        view = getMultiAdapter(
            (portal.collection, request),
            name="sticky_summary_view"
        )
        results = view.results()
        self.assertEqual(len(results['sticky_results']), 2)
        self.assertEqual(len(results['standard_results']), 0)

