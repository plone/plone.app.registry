# -*- coding: utf-8 -*-
from Products.CMFPlone.PloneBatch import Batch
from Products.Five import BrowserView
from zope.component.hooks import getSite


def _true(s, v):
    return True


def _is_in(s, v):
    return s in v


def _starts_with(s, v):
    return v.startswith(s)


_okay_prefixes = [
    'Products',
    'plone.app',
    'plone']


class RecordsControlPanel(BrowserView):

    @property
    def control_panel_url(self):
        return u"{0}/@@overview-controlpanel".format(getSite().absolute_url())

    def __call__(self):
        form = self.request.form
        search = form.get('q')
        searchp = form.get('qp')
        compare = _is_in
        if searchp not in (None, ''):
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
            if ifaceName is not None:
                recordPrefix = ifaceName.split('.')[-1]
                prefixValue = record.interfaceName
            else:
                prefixValue = record.__name__
                for prefix in _okay_prefixes:
                    name = record.__name__
                    if name.startswith(prefix):
                        recordPrefix = '.'.join(
                            name.split('.')[:len(prefix.split('.')) + 1])
                        prefixValue = recordPrefix
                        break
            if recordPrefix not in self.prefixes:
                self.prefixes[recordPrefix] = prefixValue
            if (
                compare(search, prefixValue)
                or compare(search, record.__name__)
            ):
                self.records.append(record)
        self.records = Batch(
            self.records,
            15,
            int(form.get('b_start', '0')),
            orphan=1
        )
        return self.index()
