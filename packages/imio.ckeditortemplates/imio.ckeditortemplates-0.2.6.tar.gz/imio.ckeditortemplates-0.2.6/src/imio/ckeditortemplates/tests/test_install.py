# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent

from Products.CMFCore.utils import getToolByName

from imio.ckeditortemplates.testing import IMIO_CKEDITORTEMPLATES_INTEGRATION


class TestIntegration(unittest.TestCase):
    layer = IMIO_CKEDITORTEMPLATES_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        notify(BeforeTraverseEvent(self.portal, self.request))

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        pid = 'imio.ckeditortemplates'
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_template_are_avaiable(self):
        pass

    def test_ckeditor_filtering(self):
        ptools = getToolByName(self.portal, 'portal_properties')
        cktools = ptools['ckeditor_properties']
        self.assertTrue(cktools.filtering == "disabled")
        self.assertTrue("{ name : ' Mail', element : 'p', attributes : { 'class' : 'mail' } },\n" in cktools.menuStyles)

    def test_ckeditor_toolbar(self):
        ptools = getToolByName(self.portal, 'portal_properties')
        cktools = ptools['ckeditor_properties']
        self.assertTrue(cktools.toolbar == "Custom")
        self.assertTrue("'Templates'" in cktools.toolbar_Custom)
