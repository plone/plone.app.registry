from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch

def _true(s, v):
    return True

def _is_in(s, v):
    return s in v

def _starts_with(s, v):
    return v.startswith(s)

class RecordsControlPanel(BrowserView):

    def __call__(self):
        form = self.request.form
        search = form.get('q')
        searchp = form.get('qp')
        compare = _is_in
        if searchp:
            search = searchp
        if search is not None and search.startswith('prefix:'):
            search = search[len('prefix:'):]
            compare = _starts_with
        if not search:
            compare = _true

        self.prefixes = {}
        self.records = []
        for record in self.context.records.values():
            ifaceName = record.interfaceName
            ifaceNamePart = ''
            if not ifaceName is None:
                ifaceNamePart = ifaceName.split('.')[-1]
            if ifaceNamePart not in self.prefixes:
                self.prefixes[ifaceNamePart] = record.interfaceName
            if compare(search, record.__name__):
                self.records.append(record)
        self.records = Batch(self.records, 10,
            int(form.get('b_start', '0')), orphan=1)
        return self.index()
