# -*- coding: utf-8 -*-
from lxml.etree import XMLSyntaxError
from plone.app.registry.exportimport.handler import RegistryExporter
from plone.app.registry.exportimport.handler import RegistryImporter
from plone.autoform.form import AutoExtensibleForm
from plone.registry import field as registry_field
from plone.registry import Record
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from z3c.form.action import ActionErrorOccurred
from z3c.form.interfaces import WidgetActionExecutionError
from zope import schema
from zope.component.hooks import getSite
from zope.event import notify
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleVocabulary

import logging
import string


logger = logging.getLogger('plone.app.registry')


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


class FakeEnv(object):

    def getLogger(self, name):
        return logger

    def shouldPurge(self):
        return False


_valid_field_name_chars = string.ascii_letters + '._'


def checkFieldName(val):
    for letter in val:
        if letter not in _valid_field_name_chars:
            raise Invalid('Not a valid field name')
    return True


class IAddFieldForm(Interface):
    name = schema.ASCIILine(
        title=_(u'label_field_name', default=u'Field Name'),
        description=u'Must be in a format like "plone.my_name". Only letters, periods and underscores.',
        required=True,
        constraint=checkFieldName)

    title = schema.TextLine(
        title=_(u'label_field_title', default=u'Field Title'),
        required=True)

    field_type = schema.Choice(
        title=u'Field Type',
        vocabulary=SimpleVocabulary.fromValues([
            'Bytes', 'BytesLine', 'ASCII', 'ASCIILine', 'Text', 'TextLine', 'Bool', 'Int',
            'Float', 'Decimal', 'Password',
            'Datetime', 'Date', 'Timedelta', 'SourceText', 'URI', 'Id', 'DottedName',
            # XXX not supporting these types yet as it requires additional config
            # 'Tuple', 'List', 'Set', 'FrozenSet', 'Dict',
        ])
    )

    required = schema.Bool(
        title=u'Required',
        default=False
    )


class RecordsControlPanel(AutoExtensibleForm, form.Form):
    schema = IAddFieldForm
    ignoreContext = True
    submitted = False

    template = ViewPageTemplateFile('templates/records.pt')

    @property
    def action(self):
        return '{url}#autotoc-item-autotoc-3'.format(url=self.context.absolute_url())

    def updateActions(self):
        super(RecordsControlPanel, self).updateActions()
        self.actions['addfield'].addClass('btn-primary')

    @button.buttonAndHandler(u'Add field', name='addfield')
    def action_addfield(self, action):
        data, errors = self.extractData()
        self.submitted = True
        if not errors:
            field_class = getattr(registry_field, data['field_type'], None)
            if field_class is None:
                notify(
                    ActionErrorOccurred(
                        action,
                        WidgetActionExecutionError('field_type', Invalid('Invalid Field'))))
                return
            if data['name'] in self.context:
                notify(
                    ActionErrorOccurred(
                        action,
                        WidgetActionExecutionError('name', Invalid('Field name already in use'))))
                return

            new_field = field_class(title=data['title'], required=data['required'])
            new_record = Record(new_field)
            self.context.records[data['name']] = new_record
            messages = IStatusMessage(self.request)
            messages.add(u"Successfully added field %s" % data['name'], type=u"info")
            return self.request.response.redirect('{url}/edit/{field}'.format(
                url=self.context.absolute_url(),
                field=data['name']))

    def import_registry(self):
        try:
            fi = self.request.form['file']
            body = fi.read()
        except (AttributeError, KeyError):
            messages = IStatusMessage(self.request)
            messages.add(u"Must provide XML file", type=u"error")
            body = None
        if body is not None:
            importer = RegistryImporter(self.context, FakeEnv())
            try:
                importer.importDocument(body)
            except XMLSyntaxError:
                messages = IStatusMessage(self.request)
                messages.add(u"Must provide valid XML file", type=u"error")
        return self.request.response.redirect(self.context.absolute_url())

    def export_registry(self):
        exporter = RegistryExporter(self.context, FakeEnv())
        body = exporter.exportDocument()
        resp = self.request.response
        resp.setHeader('Content-type', 'text/xml')
        resp.setHeader('Content-Disposition', 'attachment; filename=registry.xml')
        resp.setHeader("Content-Length", len(body))
        return body

    @property
    def control_panel_url(self):
        return u"{0}/@@overview-controlpanel".format(getSite().absolute_url())

    def __call__(self):
        form = self.request.form
        if self.request.REQUEST_METHOD == 'POST':
            if form.get('button.exportregistry'):
                return self.export_registry()
            if form.get('button.importregistry'):
                return self.import_registry()
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
            if (compare(search, prefixValue) or compare(search, record.__name__)):
                self.records.append(record)
        self.records = Batch(
            self.records,
            15,
            int(form.get('b_start', '0')),
            orphan=1
        )
        return super(RecordsControlPanel, self).__call__()
