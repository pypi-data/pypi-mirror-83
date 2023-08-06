# -*- coding: utf-8 -*-
from cpskin.contenttypes.content.product import IProduct  # NOQA E501
from cpskin.contenttypes.testing import CPSKIN_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class ProductIntegrationTest(unittest.TestCase):

    layer = CPSKIN_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_product_schema(self):
        fti = queryUtility(IDexterityFTI, name='Product')
        schema = fti.lookupSchema()
        self.assertEqual(IProduct, schema)

    def test_ct_product_fti(self):
        fti = queryUtility(IDexterityFTI, name='Product')
        self.assertTrue(fti)

    def test_ct_product_factory(self):
        fti = queryUtility(IDexterityFTI, name='Product')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IProduct.providedBy(obj),
            u'IProduct not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_product_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Product',
            id='product',
        )

        self.assertTrue(
            IProduct.providedBy(obj),
            u'IProduct not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_product_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Product')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_product_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Product')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'product_id',
            title='Product container',
         )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
