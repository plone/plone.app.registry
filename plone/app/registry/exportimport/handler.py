from zope.component import adapts
from zope.component import queryMultiAdapter, queryUtility

import zope.schema
from zope.schema.interfaces import IFromUnicode, ICollection

from zope.dottedname.resolve import resolve

from plone.registry.interfaces import IRegistry, IPersistentField, IInterfaceAwareRecord
from plone.registry import Record

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import XMLAdapterBase

from plone.supermodel.interfaces import IFieldExportImportHandler
from plone.supermodel.serializer import IFieldNameExtractor

_marker = object()

class RegistryXMLAdapter(XMLAdapterBase):
    adapts(IRegistry, ISetupEnviron)

    _LOGGER_ID = 'plone.app.registry'

    name = 'plone.app.registry'

    def _importNode(self, node):
        
        if self.environ.shouldPurge():
            self.context.records.clear()

        for child in node.childNodes:
            
            if child.nodeName.lower() == 'record':
                self._importRecord(child)
            elif child.nodeName.lower() == 'records':
                self._importRecords(child)

    def _exportNode(self):
        root = self._doc.createElement('registry')
        
        for record in self.context.records.values():
            child = self._doc.createElement('record')
            self._exportRecord(record, child)
            root.appendChild(child)

        return root
        
    def _importRecord(self, node):
        
        name = str(node.getAttribute('name'))
        delete = node.getAttribute('delete')
        
        interface_name = str(node.getAttribute('interface'))
        field_name = str(node.getAttribute('field'))

        if not name and interface_name and field_name:
            name = "%s.%s" % (interface_name, field_name,)
        
        if delete.lower() == 'true' and name in self.context.records:
            del self.context.records[name]
            return
        
        # See if we have an existing record
        existing_record = self.context.records.get(name, None)
        
        interface = None
        field = None
        value = _marker
        
        field_node = None
        value_node = None
        
        # If we are given an interface and field name, try to resolve them
        if interface_name and field_name:
            try:
                interface = resolve(interface_name)
                field = IPersistentField(interface[field_name])
            except ImportError:
                self._logger.warn("Failed to import interface %s for record %s" % (interface_name, name))
                interface = None
                field_name = None
            except KeyError:
                self._logger.warn("Interface %s specified for record %s has no field %s." % (interface_name, name, field_name,))
                interface = None
                field_name = None
            except TypeError:
                self._logger.warn("Field %s in interface %s specified for record %s cannot be used as a persistent field." % (field_name, interface_name, name,))            
                interface = None
                field_name = None
        
        # Find field and value nodes
        for child in node.childNodes:
            if child.nodeName.lower() == 'field':
                field_node = child
            elif child.nodeName.lower() == 'value':
                value_node = child
        
        # Let field not potentially override interface[field_name]
        if field_node is not None:
            field_type = node.getAttribute('type')
            field_type_handler = queryUtility(IFieldExportImportHandler, name=field_type)
            if field_type_handler is None:
                self._logger.warn("Field of type %s used for record %s is not supported." % (field_type, name))
            else:
                field = field_type_handler.read(field_node)
        
        # Fall back to existing record if neither a field node nor the
        # interface yielded a field
        
        change_field = True
        
        if field is None and existing_record is not None:
            change_field = False
            field = existing_record.field
        
        if field is None:
            raise KeyError(u"Cannot find a field for the record %s. Add a <field /> element or interface." % name)
        
        # Extract the value
        
        # TODO: Doesn't handle dict fields
        if value_node is not None:
            if ICollection.providedBy(field):
                value_type = field.value_type
                value = []
                for child in value_node.childNodes:
                    if child.nodeName.lower() != 'element':
                        continue
                    element_value = self._extract_text(child)
                    value.append(self._from_unicode(value_type, element_value))
                value = self._field_typecast(value_type, value)
            else:
                value = self.from_unicode(field, self._extract_text(child))

        # Now either construct or update the record
        
        if value is _marker:
            value = field.default
        
        if existing_record is not None:
            if change_field:
                existing_record.field = field
            existing_record.value = value
        else:
            self.context.records[name] = Record(field, interface=interface, field_name=field_name)

    def _importRecords(self, node):
        
        # May raise ImportError if interface can't be found
        interface = resolve(str(node.getAttribute('interface')))
        omit = []
        
        for child in node.childNodes:
            if child.nodeName.lower() == 'omit':
                omit.append(self._extract_text(child))
        
        self.context.register_interface(interface, omit=tuple(omit))
        
    def _exportRecord(self, record, node):
        
        node.setAttribute('name', record.__name__)
        
        if IInterfaceAwareRecord.providedBy(record):
            node.setAttribute('interface', record.interface_name)
            node.setAttribute('field', record.field_name)

        # write field
        
        name_extractor = IFieldNameExtractor(record.field)
        field_type = name_extractor()
        handler = queryUtility(IFieldExportImportHandler, name=field_type)
        if handler is None:
            self._logger.warn("Field type %s specified for record %s cannot be exported" % (field_type, record.__name__,))
        else:
            field_element = handler.write(record.field, 'value', field_type)
            field_element.removeAttribute('name')
            node.appendChild(field_element)
            
        # write value
        
        value_element = self._doc.createElement('value')
        
        # TODO: Doesn't handle dict fields
        if ICollection.providedBy(record.field):
            for e in record.value:
                list_element = self._doc.createElement('element')
                list_element.append(self._doc.createTextNode(unicode(e)))
                value_element.appendChild(list_element)
        else:
            value_element.append(self._doc.createTextNode(unicode(record.value)))
    
    # helpers
    
    def _extract_text(self, node):
        node.normalize()
        if len(node.childNodes) == 1 and node.childNodes[0].nodeType == node.TEXT_NODE:
            return unicode(node.childNodes[0].data)
        return None
        
    # borrowed from plone.supermodel
    
    def _from_unicode(self, field, value):
        if isinstance(value, str):
            value = unicode(value)        
        if IFromUnicode.providedBy(field) or isinstance(field, zope.schema.Bool):
            return field.fromUnicode(value)
        else:
            return self.field_typecast(field, value)
    
    def _field_typecast(self, field, value):
        typecast = getattr(field, '_type', None)
        if typecast is not None:
            if not isinstance(typecast, (list, tuple)):
                typecast = (typecast,)
            for tc in reversed(typecast):
                if callable(tc):
                    try:
                        value = tc(value)
                        break
                    except:
                        pass
        return value

def import_registry(context):
    
    logger = context.getLogger('plone.app.registry')
    registry = queryUtility(IRegistry)
    
    if registry is None:
        logger.info("Cannot find registry")
        return

    importer = queryMultiAdapter((registry, context), IBody, name='plone.app.registry')
    if importer:
        body = context.readDataFile('registry.xml')
        if body is not None:
            importer.body = body
    
def export_registry(context):

    logger = context.getLogger('plone.app.registry')
    registry = queryUtility(IRegistry)
    
    if registry is None:
        logger.info("Cannot find registry")
        return

    exporter = queryMultiAdapter((registry, context), IBody, name='plone.app.registry')
    if exporter:
        body = exporter.body
        if body is not None:
            context.writeDataFile('registry.xml', body, exporter.mime_type)