Introduction
============

This package provides Plone UI integration for plone.registry. Specifically,
it:

  * creates a version of the Registry class that will show up in the ZMI
  * installs this to the site root and registers it as a local utility
    providing IRegistry.
  * registers a GenericSetup handler for `registry.xml` to create new records
    or change values
  * provides a GUI to modify the settings registry through the web
  
GenericSetup format
-------------------

The `registry.xml` GenericSetup format looks like this::

  <registry>
  
    <records interface="plone.registry.tests.ITestSchema1" />
    
    <records interface="plone.registry.tests.ITestSchema2">
        <omit>field1</omit>
    </records>
    
    <record name="plone.app.registry.tests.dummy1">
        <field type="plone.registry.field.TextLine">
            <title>Dummy one</title>
        </field>
        <value>New value</value>
    </record>
    
    <record interface="plone.registry.tests.ITestSchema3" field="test1">
        <value>Some value</value>
    </record>
    
    <record name="plone.app.registry.tests.dummy3">
        <value>Another value</value>
    </record>
    
    <record name="plone.app.registry.tests.dummy4" delete="true" />
    
  </registry>
  
In brief:
    
  * The root element is <registry />, containing zero or more <record />
    elements and zero or more <records /> elements.
  * A <record /> element will usually have a `name` attribute.
  * A <record /> element may instead have an `interface` and a `field`
    attribute. If so, the name is `${interface}.${field}`.
  * A <record /> element may have a <field /> child element that specifies
    the field of the record.
  * A <field /> element must have a `type` attribute giving the dotted name
    to the field class. It contains child elements based on the allowed
    options for that field. This is based on plone.supermodel.
  * A <record /> element may contain a <value /> element. This should contain
    a string representation of the value of the field, and will be validated.
  * A <record /> element may have a `delete` attribute. If this is set to 
    'true', the record will be deleted.
  * If a <records /> element is provided, it must have an `interface`
    attribute containing the full dotted name to a schema interface. Records
    will be created for each field in this interface.
  * A <records /> element may contain zero or more <omit /> elements. These
    should list the names of fields that will be omitted.