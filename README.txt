Introduction
============

``plone.app.registry`` provides Plone UI and GenericSetup integration for
`plone.registry`_, which in turn implements a configuration registry for
Zope applications. For details about how the registry works, please see the
`plone.registry`_ documentation. What follows is a brief overview of common
usage patterns.

.. contents::

Overview
========

The registry provided by `plone.registry`_ is intended to store settings in
a safe, easily accessible manner. This makes it well-suited for applications
and add-on products that need to manage some configurable, user-editable
values. It is intended to replace the use of (less powerful and user friendly)
Zope 2 property sheets, as well as (less safe and more difficult to access)
persistent local utilities for managing such configuration.

The registry is *not* an arbitrary data store. For the most part, you can
store any Python primitive there, but not more complex data structures or
objects. This means that the registry cannot be broken by packages being
uninstalled, and that it can provide a simple, generic user interface for
editing values.

The registry is made up of *records*. A record consists of a *field*,
describing the record, and a current *value*.  Fields are based on the
venerable ``zope.schema``, although the standard allowable field types are
defined in the module ``plone.registry.field``. (This is partly because the
field definitions are actually persisted with the record, and partly because
``plone.registry`` performs some additional validation to ensure the integrity
of the registry).

A record can be created programmatically, though in a Plone context it is more
common to install records using the ``records.xml`` GenericSetup syntax. Once
the record has been created, its value can be read and set using a standard
Python dictionary syntax. Accessing the record and field is just as easy.

Each record has a unique name. That name should be a *dotted name* prefixed
by the package owning the record. For example, a record owned by the package
``plone.foobar`` could have a name like ``plone.foobar.frabnoz``.

Usage
=====

This section describes how the registry is most commonly used in a Plone
context. For more details, please see the `plone.registry`_ documentation.

Using GenericSetup to manipulate the registry
---------------------------------------------

The best way to create, modify and delete registry records when writing Plone
add-on products is normally to use GenericSetup.

Creating records
~~~~~~~~~~~~~~~~

Once you have decided that you need a particular record, you need to answer
two questions:

1. What should the record be called?
2. What type of data should it hold?

Let's say you wanted to create a record call ``my.package.timeout``, holding
an integer. Integers are described by the field type
``plone.registry.field.Int``. Almost all the standard fields you would find
in ``zope.schema`` have an equivalent field in ``plone.registry.field``. The
main exception is ``Object``, which is unsupported. Also, ``Choice`` fields
only support vocabularies given by string name, or as a list of string values.

To install such a record, you could add a ``registry.xml`` step to the
GenericSetup profile of your product like this::

    <registry>

        <record name="my.package.timeout">
            <field type="plone.registry.field.Int">
                <title>Timeout</title>
                <min>0</min>
            </field>
            <value>100</value>
        </record>

    </registry>

Let's look at this in more detail:

* There is one record declared. The name is given in the ``name`` attribute.
* First, we define the field type, by giving the full dotted name to the
  field class. Unless you have installed a third party package providing
  additional persistent fields, this will be a class in
  ``plone.registry.field`` mirroring a corresponding class in ``zope.schema``.
* Inside the ``<field />`` element, we list any required or optional
  attributes of the field. This uses `plone.supermodel`_ syntax. In essence,
  each allowed field attribute is represented by a tag (so the ``title``
  attribute can be set with the ``<title />`` tag). If an attribute is
  required for a field, the corresponding tag is required here.
* We then set the value. This must obviously be a valid value for the field
  type.

Most field attributes are simple tags like the ones shown above, with the
field name used as the tag name, and a string representation of the value
used as the contents of the tag. Collection fields are a little more involved,
however. A collection field (like a ``List`` or ``Tuple``) has a
``value_type`` property containing another field. Their values (and defaults)
are also sequences. Let's look at an example::

    <record name="my.package.animals">
        <field type="plone.registry.field.Tuple">
            <title>Animals</title>
            <description>A list of cool animals</description>
            <value_type type="plone.registry.field.TextLine" />
        </field>
        <value>
            <element>Dog</element>
            <element>Cat</element>
            <element>Elephant</element>
        </value>
    </record>

Notice how the ``<value_type />`` tag takes a ``type`` attribute just like
the outer ``<field />`` tag. Here we have shown a value type with no options,
but if you need, you can put tags for additional field attributes inside the
``<value_type />`` tag.

Also notice how the value is represented. Each element in the sequence (a
tuple in this case) is given by an ``<element />`` tag.

``Dict`` fields also have a ``<key_type />`` and elements that are key/value
pairs. They can be configured like so::

    <record name="my.package.animalFood">
        <field type="plone.registry.field.Dict">
            <title>Food eaten by animals</title>
            <key_type type="plone.registry.field.TextLine" />
            <value_type type="plone.registry.field.TextLine" />
        </field>
        <value>
            <element key="Dog">Dog food</element>
            <element key="Cat">Cat food</element>
            <element key="Elephant">Squirrels</element>
        </value>
    </record>

Setting values
~~~~~~~~~~~~~~

Once a record has been defined, its value can be updated in a similar manner::

    <record name="my.package.animalFood">
        <value purge="false">
            <element key="Squirrel">Nuts</element>
            <element key="Piranha">Other piranha</element>
        </value>
    </record>

Here, we have simply omitted the ``<field />`` element. It is an error to
do this unless that field already exists in the registry.

Also notice how we have used the ``purge`` attribute. When setting the value
of a list, multi-valued field such as a tuple, list, set or dictionary, this
attribute will cause the values listed to be added to the existing collection,
rather than overriding the collection entirely, as would happen if the
``purge`` attribute was set to ``true`` or omitted.

Deleting records
~~~~~~~~~~~~~~~~

To delete a record, use the ``delete`` attribute::

    <record name="my.package.animalFood" delete="true" />

If the record does not exist, a warning will be logged, but processing will
continue.

Creating records based on an interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

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

Using the registry in Python code
---------------------------------

Accessing the registry
~~~~~~~~~~~~~~~~~~~~~~

Using the records proxy
~~~~~~~~~~~~~~~~~~~~~~~

Registry events
~~~~~~~~~~~~~~~


Standard field types
--------------------


Editing records through the web
-------------------------------

This package provides a control panel found in Plone's Site Setup under
"Configuration registry". Here, you can view all records with names,
titles, descriptions, types and current values, as well as edit individual
records.

Creating a custom control panel
-------------------------------



.. _plone.registry: http://pypi.python.org/pypi/plone.registry
.. _plone.supermodel: http://pypi.python.org/pypi/plone.supermodel
