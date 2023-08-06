# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.printrss.testing import COLLECTIVE_PRINTRSS_INTEGRATION_TESTING  # noqa
from collective.printrss.interfaces import IRssFeed

import unittest2 as unittest


class rss_feedIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PRINTRSS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='rss_feed')
        schema = fti.lookupSchema()
        self.assertEqual(IRssFeed, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='rss_feed')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='rss_feed')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IRssFeed.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('rss_feed', 'rss_feed')
        self.assertTrue(
            IRssFeed.providedBy(self.portal['rss_feed'])
        )
