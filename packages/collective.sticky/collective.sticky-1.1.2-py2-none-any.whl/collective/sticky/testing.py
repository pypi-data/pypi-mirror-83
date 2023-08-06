# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2
from plone import api
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI


class CollectiveStickyLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.sticky
        self.loadZCML('testing.zcml', package=collective.sticky)
        z2.installProduct(app, 'collective.sticky')
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.sticky')
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        self.applyProfile(portal, 'plone.app.contenttypes:plone-content')
        self.applyProfile(portal, 'collective.sticky:default')

        fti = queryUtility(IDexterityFTI, name='News Item')
        behaviors = list(fti.behaviors)
        behaviors.append('collective.sticky.behavior.ISticky')
        fti._updateProperty('behaviors', tuple(behaviors))

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        simplenews = api.content.create(portal, 'News Item', 'simplenews', title=u"Simple News")
        simplenews.sticky = False
        simplenews.reindexObject()
        stickynews = api.content.create(portal, 'News Item', 'stickynews', title=u"Sticky News")
        stickynews.sticky = True
        stickynews.reindexObject()
        collection = api.content.create(portal, 'Collection', 'collection', title=u'Collection')
        query = [{'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['News Item']},]
        collection.setQuery(query)
        setRoles(portal, TEST_USER_ID, ['Member'])


FIXTURE = CollectiveStickyLayer()

INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='collective.sticky:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name='collective.sticky:Functional')
