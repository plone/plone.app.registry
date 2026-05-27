import zope.deferredimport

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry import RegistryEditForm instead.",
    RegistryEditForm="plone.app.layout.controlpanels.registry:RegistryEditForm",
)

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry import ControlPanelFormWrapper instead.",
    ControlPanelFormWrapper="plone.app.layout.controlpanels.registry:ControlPanelFormWrapper",
)
