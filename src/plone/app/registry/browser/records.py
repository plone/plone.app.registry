import zope.deferredimport

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry_records import IAddFieldForm instead.",
    IAddFieldForm="plone.app.layout.controlpanels.registry_records:IAddFieldForm",
)

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry_records import RecordsControlPanel instead.",
    RecordsControlPanel="plone.app.layout.controlpanels.registry_records:RecordsControlPanel",
)
