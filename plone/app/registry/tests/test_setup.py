from unittest import defaultTestLoader
from Products.PloneTestCase.ptc import PloneTestCase

from Acquisition import aq_base

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from plone.app.registry.tests.layer import Layer

class TestSetup(PloneTestCase):
    
    layer = Layer
    
    def test_tool_installed(self):
        self.failUnless('portal_registry' in self.portal.objectIds())
        self.failUnless(IRegistry.providedBy(self.portal.portal_registry))
    
    def test_local_utility_installed(self):
        registry = getUtility(IRegistry)
        self.failUnless(aq_base(registry) is aq_base(self.portal.portal_registry))
    
def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
