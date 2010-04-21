Introduction
============

``plone.app.registry`` provides Plone UI and GenericSetup integration for
`plone.registry`_, which in turn implements a configuration registry for
Zope applications. For details about how the registry works, please see the
`plone.registry`_ documentation. What follows is a brief overview of common
usage patterns in Plone.

.. contents:: Table of contents

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
describing the record, and a *value*.  Fields are based on the venerable
``zope.schema``, although the standard allowable field types are defined in
the module ``plone.registry.field``. (This is partly because the field
definitions are actually persisted with the record, and partly because 
``plone.registry`` performs some additional validation to ensure the integrity
of the registry).

A record can be created programmatically, though in a Plone context it is more
common to install records using the ``records.xml`` GenericSetup syntax. Once
the record has been created, its value can be read and set using standard
Python dictionary syntax. Accessing the record and field is just as easy.

Each record has a unique name, which must be a *dotted name* prefixed by the
package owning the record. For example, a record owned by the package
``my.package`` could have a name like ``my.package.myrecord``.

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
Finally, you cannot use the ``constraint`` property to set a validator
function, although other validation (such as min/max values) will work.

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
* In the record, we first define the field type, by giving the full dotted
  name to the field class. Unless you have installed a third party package
  providing additional persistent fields, this will be a class in
  ``plone.registry.field`` mirroring a corresponding class in ``zope.schema``.
* Inside the ``<field />`` element, we list any required or optional
  attributes of the field. This uses `plone.supermodel`_ syntax. In essence,
  each allowed field attribute is represented by a tag (so the ``title``
  attribute can be set with the ``<title />`` tag), with the attribute value
  given as the tag body. If an attribute is required for a field, the
  corresponding tag is required here.
* We then set the value. This must obviously be a valid value for the field
  type.

Note that the ``<value />`` is optional. If not given, the field will default
to its ``missing_value`` until it is set. The ``<field />`` is optional if
the record has already been initialised elsewhere.

Most field attributes are simple tags like the ones shown above, with the
field name used as the tag name, and a string representation of the value
used as the contents of the tag. Collection fields are a little more involved,
however. A collection field (like a ``List`` or ``Tuple``) has a
``value_type`` property containing another field. Also, their values and
defaults are sequences. Let's look at an example::

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
tuple in this case) is given by an ``<element />`` tag, with the element
value given as the body of that tag.

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

Once a record has been defined, its value can be set or updated using
GenericSetup like so::

    <record name="my.package.animalFood">
        <value purge="false">
            <element key="Squirrel">Nuts</element>
            <element key="Piranha">Other piranha</element>
        </value>
    </record>

This is often useful if you have a record defined in one package that is
appended to or customised in another package.

In the example above, we used the ``purge`` attribute. When setting the value
of a multi-valued field such as a tuple, list, set or dictionary, setting this
attribute to ``false`` will cause the values listed to be added to the
existing collection, rather than overriding the collection entirely, as would
happen if the ``purge`` attribute was set to ``true`` or omitted.

Deleting records
~~~~~~~~~~~~~~~~

To delete a record, use the ``delete`` attribute::

    <record name="my.package.animalFood" delete="true" />

If the record does not exist, a warning will be logged, but processing will
continue.

Creating records based on an interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the examples above, we created individual records directly in the registry.
Sometimes, however, it is easier to work with traditional schema interfaces
that group together several related fields. As we will see below,
``plone.registry`` and ``plone.app.registry`` provide certain additional
functionality for groups of records created from an interface.

For example, we could have an interface like this::

    from zope.interface import Interface
    from zope import schema
    
    class IZooSettings(Interface):
        
        entryPrice = schema.Decimal(title=u"Admission charge")
        messageOfTheDay = schema.TextLine(title=u"A banner message", default=u"Welcome!")

Notice how we are using standard ``zope.schema`` fields. These will be
converted to persistent fields (by adapting them to ``IPersistentField`` from
``plone.registry``) when the registry is populated. If that is not possible,
an error will occur on import.

To register these records, we simply add the following to ``registry.xml``::

    <records interface="my.package.interfaces.IZooSettings" />


This will create one record for each field. The record names are the full
dotted names to the fields, so in this case they would be
``my.package.interfaces.IZooSettings.entryPrice`` and
``my.package.interfaces.IZooSettings.messageOfTheDay``.

If you just want to use the interface as a template you can supply a
``prefix`` attribute:

    <records interface="my.package.interfaces.IZooSettings" prefix="my.zoo" />

which will generate fields named ``my.zoo.entryPrice`` and
``my.zoo.messageOfTheDay``.

In order to set the values of the fields created by a <records /> directive
you must provide ``value`` entries with keys corresponding to the fields on
the interface, as follows::

    <records interface="my.package.interfaces.IZooSettings" prefix="my.zoo">
        <value key="entryPrice">40</value>
        <value key="messageOfTheDay">We've got lions and tigers!</value>
    </records>

Values can be set as above using the full record name. However, we can also
explicitly state that we are setting a record bound to an interface, like so::

    <record interface="my.package.interfaces.IZooSettings" field="entryPrice">
        <value>10.0</value>
    </record>

This is equivalent to::

    <record interface="my.package.interfaces.IZooSettings.entryPrice">
        <value>10.0</value>
    </record>

You can also use the ``interface``/``field`` syntax to register a new record
from an individual field.

Finally, if the interface contains fields that cannot or should be set, they
may be omitted::

    <records interface="my.package.interfaces.IZooSettings">
        <omit>someField</omit>
    </records>

The ``<omit />`` tag can be repeated to exclude multiple fields.

Using the registry in Python code
---------------------------------

Now that we have seen how to manage records through GenericSetup, we can start
using values from the registry in our code.

Accessing the registry
~~~~~~~~~~~~~~~~~~~~~~

To get or set the value of a record, yoweu must first look up the registry
itself. The registry is registered as a local utility, so we can look it up
with::

    from zope.component import getUtility
    from plone.registry.interfaces import IRegistry
    
    registry = getUtility(IRegistry)

Values can now get read or set using simple dictionary syntax::

    timeout = registry['my.package.timeout']

We can also use ``get()`` to get the value conditionally, and an ``in`` check
to test whether the registry contains a particular record.

The returned value will by of a type consistent with the field for the record
with the given name. It can be set in the same manner::

    registry['my.package.timeout'] = 120

If you need to access the underlying record, use the ``records`` attribute::

    timeoutRecord = registry.records['my.package.timeout']

The record returned conforms to ``plone.registry.interfaces.IRecord`` and has
two main attributes: ``value`` is the current record value, and ``field`` is
the persistent field instance. If the record was created from an interface,
it will also provide ``IInterfaceAwareRecord`` and have three additional
attributes: ``interfaceName``, the string name of the interface;
``interface``, the interface instance itself, and ``fieldName``, the name of
the field in the interface from which this record was created.

In unit tests, it may be useful to create a new record programmatically.
You can do that like so::
    
    from plone.registry.record import Record
    from plone.registry import field
    
    registry['my.record'] = Record(field.TextLine(title=u"A record"), u"Test")

The constructor takes a persistent field and the initial value as parameters.

To register records for an interface programmatically, we can do::

    registry.registerInterface(IZooSettings)

You can omit fields by passing an ``omit`` parameter giving a sequence of
omitted field names.

See ``plone.registry`` for more details about how to introspect and manipulate
the registry records programmatically.

Using the records proxy
~~~~~~~~~~~~~~~~~~~~~~~

Above, we used dictionary syntax to access individual records and values. This
will always work, but for so-called interface-aware records - those which were
created from an interface e.g. using the ``<records />`` syntax - we have
another option: the records proxy. This allows us to look up all the records
that belong to a particular interface at the same time, returning an object
that provides the given interface and can be manipulated like an object, that
is still connected to the underlying registry.

To look up a records proxy for our ``IZooSettings`` interface, we can do::

    zooSettings = registry.forInterface(IZooSettings)

The ``zooSettings`` object now provides ``IZooSettings``. Values may be
read and set using attribute notation::

    zooSettings.messageOfTheDay = u"New message"
    currentEntryPrice = zooSettings.entryPrice

When setting a value, it is immediately validated and written to the registry.
A validation error exception may be raised if the value is not permitted by
the field for the corresponding record.

When fetching the records proxy, ``plone.registry`` will by default verify
that records exists for each field in the interface, and will raise an error
if this is not the case. To disable this check, you can do::
    
    zooSettings = registry.forInterface(IZooSettings, check=False)

This is sometimes useful in cases where it is not certain that the registry
has been initialised. You can also omit checking for individual fields, by
passing an ``omit`` parameter giving a tuple of field names.

Registry events
~~~~~~~~~~~~~~~

The registry emits events when it is modified:

* ``plone.registry.interfaces.IRecordAddedEvent`` is fired when a record has
  been added to the registry.
* ``plone.registry.interfaces.IRecordRemovedEvent`` is fired when a record
  has been removed from the registry.
* ``plone.registry.interfaces.IRecordModifiedEvent`` is fired when a record's
  value is modified.

You can register subscribers for these to catch any changes to the registry.
In addition, you can register an event handler that only listens to changes
pertaining to records associated with specific interfaces. For example::

    from zope.component import adapter
    from plone.registry.interfaces import IRecordModifiedEvent
    
    from logging import getLogger
    log = getLogger('my.package)
    
    @adapter(IZooSettings, IRecordModifiedEvent)
    def detectPriceChange(settings, event):
        if record.fieldName == 'entryPrice':
            log.warning("Someone change the price from %d to %d" % (event.oldValue, event.newValue,))

See `plone.registry`_ for details about these event types.

Editing records through the web
-------------------------------

This package provides a control panel found in Plone's Site Setup under
"Configuration registry". Here, you can view all records with names,
titles, descriptions, types and current values, as well as edit individual
records.

Creating a custom control panel
-------------------------------

The generic control panel is useful as a system administrator's tool for low-
level configuration. If you are writing a package aimed more at system
integrators and content managers, you may want to provide a more user-friendly
control panel to manage settings.

If you register your records from an interface as shown above, this package
provides a convenience framework based on `plone.autoform`_ and `z3c.form`_
that makes it easy to create your own control panel.

To use it, create a module like this::

    from plone.app.registry.browser.form import RegistryEditForm
    from plone.app.registry.browser.form import ControlPanelFormWrapper
    
    from my.package.interfaces import IZooSettings
    form plone.z3cform import layout
    
    class ZooControlPanelForm(RegistryEditForm):
        schema = IZooSettings
    
    ZooControlPanelView = layout.wrap_form(ZooControlPanelForm, ControlPanelFormWrapper)

Register the ``ZooControlPanelView`` as a view::

    <browser:page
        name="zoo-controlpanel"
        for="Products.CMFPlone.interfaces.IPloneSiteRoot"
        permission="cmf.ManagePortal"
        class=".controlpanel.ZooControlPanelView"
        />

Then install this in the Plone control panel using the ``controlpanel.xml``
import step in your GenericSetup profile::

    <?xml version="1.0"?>
    <object
        name="portal_controlpanel"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="my.package">
        
        <configlet
            title="Zoo settings"
            action_id="my.package.zoosettings"
            appId="my.package"
            category="Products"
            condition_expr=""
            url_expr="string:${portal_url}/@@zoo-controlpanel"
            icon_expr="string:${portal_url}/++resource++my.package/icon.png"
            visible="True"
            i18n:attributes="title">
                <permission>Manage portal</permission>
        </configlet>
    
    </object>

The ``icon_expr`` attribute should give a URL for the icon. Here, we have
assumed that a resource directory called ``my.package`` is registered and
contains the file ``icon.png``. You may omit the icon as well.

.. _plone.registry: http://pypi.python.org/pypi/plone.registry
.. _plone.supermodel: http://pypi.python.org/pypi/plone.supermodel
.. _plone.autoform: http://pypi.python.org/pypi/plone.autoform
.. _z3c.form: http://pypi.python.org/pypi/z3c.form
