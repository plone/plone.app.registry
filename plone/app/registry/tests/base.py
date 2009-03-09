from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

@onsetup
def setupPackage():
    """ set up the package and its dependencies """
    fiveconfigure.debug_mode = True
    import plone.app.registry
    zcml.load_config('configure.zcml', plone.app.registry)
    fiveconfigure.debug_mode = False

setupPackage()
PloneTestCase.setupPloneSite(extension_profiles=(
    'plone.app.registry:default',
))


class RegistryTestCase(PloneTestCase.PloneTestCase):
    """Base class for integration tests
    """