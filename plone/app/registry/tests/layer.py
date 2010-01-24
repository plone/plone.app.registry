from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

from Products.Five import fiveconfigure, zcml

ptc.setupPloneSite()

class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):
    
    def afterSetUp(self):
        import plone.app.registry
        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml', plone.app.registry)
        fiveconfigure.debug_mode = False
        self.addProfile('plone.app.registry:default')

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])
