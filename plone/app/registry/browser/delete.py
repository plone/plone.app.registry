from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage


class RecordDeleteView(BrowserView):

    def __call__(self):
        if self.request.REQUEST_METHOD == 'POST':
            name = self.request.form.get('name')
            if isinstance(name, list) and len(name) > 0:
                name = name[0]
            if self.request.form.get('form.buttons.delete'):
                if name in self.context:
                    del self.context.records[name]
                    messages = IStatusMessage(self.request)
                    messages.add(u"Successfully deleted field %s" % name, type=u"info")
            elif self.request.form.get('form.buttons.cancel') and name:
                messages = IStatusMessage(self.request)
                messages.add(u"Successfully deleted field %s" % name, type=u"info")
            return self.request.response.redirect(self.context.absolute_url())
        return super(RecordDeleteView, self).__call__()
