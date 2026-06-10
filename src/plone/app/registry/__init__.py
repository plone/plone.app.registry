from plone.app.registry.registry import Registry  # noqa: F401

jbot_deprecations = {
    "plone.app.registry.browser.templates.controlpanel_layout.pt": "plone.app.layout.controlpanel.templates.registry_controlpanel_layout.pt",
    "plone.app.registry.browser.templates.delete_layout.pt": "plone.app.layout.controlpanel.templates.registry_delete_layout.pt",
    "plone.app.registry.browser.templates.edit_layout.pt": "plone.app.layout.controlpanel.templates.registry_edit_layout.pt",
    "plone.app.registry.browser.templates.exportxml.pt": "plone.app.layout.controlpanel.templates.registry_exportxml.pt",
    "plone.app.registry.browser.templates.records.pt": "plone.app.layout.controlpanel.templates.registry_records.pt",
}
