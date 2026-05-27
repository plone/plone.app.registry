import zope.deferredimport

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry_records import RecordDeleteView instead.",
    RecordDeleteView="plone.app.layout.controlpanels.registry_records:RecordDeleteView",
)
