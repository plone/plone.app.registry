from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse

from plone.z3cform import layout
from z3c.form import form, field, button

from Products.statusmessages.interfaces import IStatusMessage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone.app.registry')
PMF = MessageFactory('plone')

class RecordEditForm(form.EditForm):
    """Edit a single record
    """
    
    record = None
    
    def getContent(self):
        return {'value': self.record.value}
        
    def update(self):
        self.fields = field.Fields(self.record.field,)
        super(RecordEditForm, self).update()

    def updateActions(self):
        super(RecordEditForm, self).updateActions()
        self.actions['save'].addClass("context")
        self.actions['cancel'].addClass("standalone")
        
    @property
    def label(self):
        return _(u"Edit record: ${name}", mapping={'name': self.record.__name__})

    @button.buttonAndHandler(PMF(u"label_save", default=u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.record.value = data['value']
        IStatusMessage(self.request).addStatusMessage(PMF(u"Changes saved."), "info")
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(PMF(u"label_cancel", default=u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(PMF(u"message_edit_item_cancelled",
            default=u"Edit cancelled."), "info")
        self.request.response.redirect(self.context.absolute_url())

class RecordEditView(layout.FormWrapper):
    implements(IPublishTraverse)
    form = RecordEditForm
    
    def __init__(self, context, request):
        super(RecordEditView, self).__init__(context, request)
        self.request['disable_border'] = True
    
    def publishTraverse(self, request, name):
        record = self.context.records[name]
        self.record = record
        self.form_instance.record = record
        return self
