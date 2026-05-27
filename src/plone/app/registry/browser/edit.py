import zope.deferredimport

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry_records import RecordEditForm instead.",
    RecordEditForm="plone.app.layout.controlpanels.registry_records:RecordEditForm",
)

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.controlpanels.registry_records import RecordEditView instead.",
    RecordEditView="plone.app.layout.controlpanels.registry_records:RecordEditView",
)
