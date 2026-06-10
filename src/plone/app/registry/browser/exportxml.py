import zope.deferredimport

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry import RegistryExporterView instead.",
    RegistryExporterView="plone.app.layout.controlpanels.registry:RegistryExporterView",
)
