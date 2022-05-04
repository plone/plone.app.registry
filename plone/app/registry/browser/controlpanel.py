from plone.autoform.form import AutoExtensibleForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("plone")


class RegistryEditForm(AutoExtensibleForm, form.EditForm):
    """Edit a records proxy based on an interface.

    To use this, you should use the <records /> element in a registry.xml
    GS import step to register records for a particular interface. Then
    subclass this form and set the 'schema' class variable to point to
    the same interface. You can use plone.autoform form hints to affect the
    rendering of the form, or override the update() method as appropriate.

    To get the standard control panel layout, use ControlPanelFormWrapper as
    the form wrapper, e.g.

        from plone.app.registry.browser.form import RegistryEditForm
        from plone.app.registry.browser.form import ControlPanelFormWrapper
        from my.package.interfaces import IMySettings
        form plone.z3cform import layout

        class MyForm(RegistryEditForm):
            schema = IMySettings

        MyFormView = layout.wrap_form(MyForm, ControlPanelFormWrapper)

    Then register MyFormView as a browser view.
    """

    control_panel_view = "@@overview-controlpanel"
    schema_prefix = None

    def getContent(self):
        return getUtility(IRegistry).forInterface(
            self.schema, prefix=self.schema_prefix
        )

    def updateActions(self):
        super().updateActions()
        self.actions["save"].addClass("btn btn-primary")
        self.actions["cancel"].addClass("btn btn-secondary")

    @button.buttonAndHandler(_("Save"), name="save")
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_("Changes saved."), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."), "info")
        self.request.response.redirect(
            f"{getSite().absolute_url()}/{self.control_panel_view}"
        )


class ControlPanelFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile("templates/controlpanel_layout.pt")

    @property
    def control_panel_url(self):
        return f"{getSite().absolute_url()}/@@overview-controlpanel"
