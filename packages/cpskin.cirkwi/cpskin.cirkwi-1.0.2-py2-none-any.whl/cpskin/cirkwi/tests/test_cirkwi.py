# -*- coding: utf-8 -*-
from cpskin.cirkwi.interfaces import ICirkwi
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.component import createObject


from cpskin.cirkwi.testing import CPSKIN_CIRKWI_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


class CirkwiIntegrationTest(unittest.TestCase):

    layer = CPSKIN_CIRKWI_INTEGRATION_TESTING
    cirkwi = None

    def _createCirkwi(self, title, desc, cdf_host="3249", cdf_outils="570", cdf_lang="fr"):
        """Method to create a cirkwi"""
        self.cirkwi = api.content.create(
            type="cirkwi",
            title=title,
            description=desc,
            cdf_host=cdf_host,
            cdf_outils=cdf_outils,
            cdf_lang=cdf_lang,
            container=self.portal,
        )

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self._createCirkwi("cirkwi",
                           "test description",
                           cdf_host="3249",
                           cdf_outils="570",
                           cdf_lang="fr")

    def test_cirkwi_portal_type_is_registered(self):
        """Test if new portal_type cirkwi is in registered types"""
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('cirkwi' in registered_types)

    def test_cirkwiview_class_registration(self):
        """Test the cirkwi view"""
        from cpskin.cirkwi.browser.cirkwiview import CirkwiView
        view = self.cirkwi.restrictedTraverse('cirkwiview')
        self.assertTrue(isinstance(view, CirkwiView))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='cirkwi')
        self.assertTrue(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='cirkwi')
        schema = fti.lookupSchema()
        self.assertEqual(ICirkwi, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='cirkwi')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ICirkwi.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('cirkwi', 'cirkwi1')
        c1 = self.portal['cirkwi1']
        self.assertTrue(ICirkwi.providedBy(c1))

