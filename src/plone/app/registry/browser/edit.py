from Acquisition import ImplicitAcquisitionWrapper
from plone.z3cform import layout
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


_ = MessageFactory("plone")


class RecordEditForm(form.EditForm):
    """Edit a single record"""

    record = None

    @property
    def action(self):
        return f"{self.context.absolute_url()}/edit/{self.record.__name__}"

    def getContent(self):
        return ImplicitAcquisitionWrapper({"value": self.record.value}, self.context)

    def update(self):
        self.fields = field.Fields(
            self.record.field,
        )
        super().update()

    def updateActions(self):
        super().updateActions()
        self.actions["save"].addClass("btn btn-primary")
        self.actions["cancel"].addClass("btn btn-secondary")

    @property
    def label(self):
        return _("Edit record: ${name}", mapping={"name": self.record.__name__})

    @button.buttonAndHandler(_("Save"), name="save")
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.record.value = data["value"]
        IStatusMessage(self.request).addStatusMessage(_("Changes saved."), "info")
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Edit cancelled."), "info")
        self.request.response.redirect(self.context.absolute_url())


@implementer(IPublishTraverse)
class RecordEditView(layout.FormWrapper):
    form = RecordEditForm

    def __init__(self, context, request):
        super().__init__(context, request)
        self.request["disable_border"] = True

    def publishTraverse(self, request, name):
        path = self.request["TraversalRequestNameStack"] + [name]
        path.reverse()
        key = "/".join(path)
        del self.request["TraversalRequestNameStack"][:]
        record = self.context.records[key]
        self.record = record
        self.form_instance.record = record
        return self
