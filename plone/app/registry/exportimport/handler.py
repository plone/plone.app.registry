from zope.component import queryUtility

from elementtree import ElementTree

from zope.dottedname.resolve import resolve

from plone.registry.interfaces import IRegistry, IPersistentField, IInterfaceAwareRecord
from plone.registry import Record

from plone.supermodel.interfaces import IFieldExportImportHandler
from plone.supermodel.interfaces import IFieldNameExtractor

from plone.supermodel.utils import pretty_xml, element_to_value, value_to_element

_marker = object()

def import_registry(context):
    
    logger = context.getLogger('plone.app.registry')
    registry = queryUtility(IRegistry)
    
    if registry is None:
        logger.info("Cannot find registry")
        return

    body = context.readDataFile('registry.xml')
    if body is not None:
        importer = RegistryImporter(registry, context)
        importer.importDocument(body)
        
def export_registry(context):

    logger = context.getLogger('plone.app.registry')
    registry = queryUtility(IRegistry)
    
    if registry is None:
        logger.info("Cannot find registry")
        return

    exporter = RegistryExporter(registry, context)
    body = exporter.exportDocument()
    if body is not None:
        context.writeDataFile('registry.xml', body, 'text/xml')

class RegistryImporter(object):
    """Helper classt to import a registry file
    """

    LOGGER_ID = 'plone.app.registry'

    def __init__(self, context, environ):
        self.context = context
        self.environ = environ
        self.logger = environ.getLogger(self.LOGGER_ID)

    def importDocument(self, document):
        tree = ElementTree.fromstring(document)
        
        if self.environ.shouldPurge():
            self.context.records.clear()

        for node in tree:
            if node.tag.lower() == 'record':
                self.importRecord(node)
            elif node.tag.lower() == 'records':
                self.importRecords(node)

    def importRecord(self, node):
        
        name = str(node.get('name', ''))
        delete = node.get('delete', 'false')
        
        interface_name = str(node.get('interface', ''))
        field_name = str(node.get('field', ''))

        if not name and (interface_name and field_name):
            name = "%s.%s" % (interface_name, field_name,)
        
        if not name:
            raise NameError("No name given for <record /> node!")
        
        # Handle deletion and quit
        if delete.lower() == 'true':
            if name in self.context.records:
                del self.context.records[name]
                self.logger.info("Deleted record %s." % name)
            else:
                self.logger.warning("Record %s was marked for deletion, but was not found." % name)
            return
        
        # See if we have an existing record
        existing_record = self.context.records.get(name, None)
        
        interface = None
        field = None
        value = _marker
        value_purge = True
        
        # If we are given an interface and field name, try to resolve them
        if interface_name and field_name:
            try:
                interface = resolve(interface_name)
                field = IPersistentField(interface[field_name])
            except ImportError:
                self.logger.warning("Failed to import interface %s for record %s" % (interface_name, name))
                interface = None
                field = None
            except KeyError:
                self.logger.warning("Interface %s specified for record %s has no field %s." % (interface_name, name, field_name,))
                interface = None
                field = None
            except TypeError:
                self.logger.warning("Field %s in interface %s specified for record %s cannot be used as a persistent field." % (field_name, interface_name, name,))            
                interface = None
                field = None
        
        # Find field and value nodes
        
        field_node = None
        value_node = None
         
        for child in node:
            if child.tag.lower() == 'field':
                field_node = child
            elif child.tag.lower() == 'value':
                value_node = child
        
        # Let field not potentially override interface[field_name]
        if field_node is not None:
            field_type = field_node.attrib.get('type', None)
            field_type_handler = queryUtility(IFieldExportImportHandler, name=field_type)
            if field_type_handler is None:
                raise TypeError("Field of type %s used for record %s is not supported." % (field_type, name))
            else:
                field = field_type_handler.read(field_node)
                if not IPersistentField.providedBy(field):
                    raise TypeError("Only persistent fields may be imported. %s used for record %s is invalid." % (field_type, name,))
        
        # Fall back to existing record if neither a field node nor the
        # interface yielded a field
        
        change_field = True
        
        if field is None and existing_record is not None:
            change_field = False
            field = existing_record.field
        
        if field is None:
            raise ValueError("Cannot find a field for the record %s. Add a <field /> element or reference an interface and field name." % name)
        
        # Extract the value

        if value_node is not None:
            value_purge = value_node.attrib.get('purge', '').lower() != 'false'
            value = element_to_value(field, value_node, default=_marker)

        # Now either construct or update the record
        
        if value is _marker:
            value = field.default
            value_purge = True
        
        if existing_record is not None:
            if change_field:
                existing_record.field = field
            
            existing_value = existing_record.value
            if change_field or value != existing_value:
                
                if not value_purge and type(value) == type(existing_value):
                    if isinstance(value, (list, tuple,)):
                        value = existing_value + value
                    elif isinstance(value, (set, frozenset,)):
                        value = existing_value.union(value)
                    elif isinstance(value, dict):
                        existing_value.update(value)
                        value = existing_value
                
                existing_record.value = value
        else:
            self.context.records[name] = Record(field, value, 
                                                interface=interface,
                                                field_name=field_name)

    def importRecords(self, node):
        
        # May raise ImportError if interface can't be found or KeyError if
        # attribute is missing.
        
        interface_name = node.attrib.get('interface', None)
        if interface_name is None:
            raise KeyError(u"A <records /> node must have an 'interface' attribute.")
        
        # May raise ImportError
        interface = resolve(interface_name)

        omit = []
        for child in node:
            if child.tag.lower() == 'omit':
                if child.text:
                    omit.append(unicode(child.text))
        
        # May raise TypeError
        self.context.register_interface(interface, omit=tuple(omit))

class RegistryExporter(object):
    
    LOGGER_ID = 'plone.app.registry'

    def __init__(self, context, environ):
        self.context = context
        self.environ = environ
        self.logger = environ.getLogger(self.LOGGER_ID)
    
    def exportDocument(self):
        root = ElementTree.Element('registry')
        
        for record in self.context.records.values():
            node = self.exportRecord(record)
            root.append(node)

        return pretty_xml(root)

    def exportRecord(self, record):
        
        node = ElementTree.Element('record')
        node.attrib['name'] = record.__name__
        
        if IInterfaceAwareRecord.providedBy(record):
            node.attrib['interface'] = record.interface_name
            node.attrib['field'] = record.field_name

        # write field
        
        field_type = IFieldNameExtractor(record.field)()
        handler = queryUtility(IFieldExportImportHandler, name=field_type)
        if handler is None:
            self.logger.warning("Field type %s specified for record %s cannot be exported" % (field_type, record.__name__,))
        else:
            field_element = handler.write(record.field, None, field_type, element_name='field')
            node.append(field_element)
            
        # write value
        
        value_element = value_to_element(record.field, record.value, name='value', force=True)
        node.append(value_element)

        return node