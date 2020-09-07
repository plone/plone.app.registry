Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.7.7 (2020-09-07)
------------------

Bug fixes:


- Make interface list on configuration export page visible. [jensens] (#41)


1.7.6 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


1.7.5 (2019-05-01)
------------------

Bug fixes:


- broken value in records table in Python 3
  [petschki] (#36)


1.7.4 (2019-03-03)
------------------

Bug fixes:


- Fix export of registry with Generic Setup. [pbauer] (#34)


1.7.3 (2019-02-13)
------------------

Bug fixes:


- Fix some deprecation warnings. [gforcada] (#32)


1.7.2 (2018-06-19)
------------------

New features:

- Added a pragmatic XML exporter for registry records in a format meant to be used in add-ons or policy profiles.
  [jensens]


1.7.1 (2018-04-08)
------------------

Bug fixes:

- Python 2 / 3 compatible imports.
  [pbauer]


1.7 (2018-02-04)
----------------

New features:

- Added traceback info of filename to importer in order to ease debugging.
  [jensens]

Bug fixes:

- Python 2 / 3 compatible imports.
  [pbauer]

- Minor refactoring of registry import (DRY).
  [jensens]


1.6.1 (2017-06-04)
------------------

Bug fixes:

- remove unittest2 dependency
  [kakshay21]


1.6 (2017-05-23)
----------------

New features:

- be able to split your registry.xml file into multiple files in a sub-directory `registry`
  [vangheem]

- Add ability to import/export records through control panel
  [vangheem]

- Add ability to add new record through control panel
  [vangheem]

- Add ability to delete record through control panel
  [vangheem]

- Document new features
  [tkimnguyen]


1.5 (2016-10-23)
----------------

New features:

- Add support for *have* and *have-not* import conditions in
  registry.xml
  [datakurre]


1.4 (2016-09-14)
----------------

New features:

- Add support for optional condition attribute in registry.xml entries
  to allow conditional importing of records. Conditions themselves are
  not import (nor exported).
  [datakurre]


1.3.12 (2016-06-27)
-------------------

New:

- Add traceback info with record name to importer in order to ease debugging.
  [jensens]


1.3.11 (2016-03-31)
-------------------

New:

- For ``ControlPanelFormWrapper`` and ``@@configuration_registry``, construct the base url to the ``@@overview-controlpanel`` from the nearest site.
  This gives more flexibility when calling controlpanels on sub sites with local registries while in standard Plone installations the controlpanel is still bound to the portal url.
  [thet]


1.3.10 (2016-02-27)
-------------------

Fixes:

- Saving registry value in modal no longer reloads whole page
  [vangheem]


1.3.9 (2016-02-20)
------------------

Fixes:

- Document how to remove a registry record with Python.
  [gforcada]


1.3.8 (2016-02-08)
------------------

New:

- Updated to work with new plone.batching ``pagination`` selector as
  well as with old one.  [davilima6]


1.3.7 (2015-11-28)
------------------

Fixes:

- Updated Site Setup link in all control panels.
  Fixes https://github.com/plone/Products.CMFPlone/issues/1255
  [davilima6]


1.3.6 (2015-10-27)
------------------

New:

- Show loading icon in control panel when searching.
  [vangheem]

Fixes:

- Cleanup: pep8, utf8 headers, readability, etc.
  [jensens]

- Let our ``plone.app.registry`` import step depend on ``typeinfo``.
  The portal types may be needed for vocabularies.  For example, you
  could get an error when adding a not yet installed type to
  ``types_not_searched``.
  Fixes https://github.com/plone/Products.CMFPlone/issues/1118
  [maurits]


1.3.5 (2015-09-20)
------------------

- Fix styling alignment issues with the buttons.
  [sneridagh]


1.3.4 (2015-09-14)
------------------

- registry javascript fix to not auto-expand search field as it was
  not working well
  [vangheem]


1.3.3 (2015-09-08)
------------------

- Fix modal in control panel
  [vangheem]


1.3.2 (2015-08-20)
------------------

- Added the `structure` keyword to the TALES expression that returns the description for registry entries.
  This ensures that descriptions are properly escaped and HTML entities don't show up in descriptions.
  [pigeonflight]


1.3.1 (2015-07-18)
------------------

- Change the category of the configlet to 'plone-advanced'.
  [sneridagh]

- Make configlets titles consistent across the site, first letter capitalized.
  [sneridagh]


1.3.0 (2015-03-13)
------------------

- fix control panel filtering to work with plone 5 and patterns
  [vangheem]


1.2.3 (2013-05-23)
------------------

- Fix control panel filtering (https://dev.plone.org/ticket/13557)
  [vangheem, danjacka]


1.2.2 (2013-01-13)
------------------

- Acquisition-wrap value dictionary such that widgets get a useful
  context.
  [malthe]

- Allow XML comments in registry.xml
  [gweis]

- allow using purge=false in dict.value_type == list registry
  imports.
  [vangheem]


1.2.1 (2012-10-16)
------------------

- Unified the control panel html structure.
  [TH-code]

- Fix jquery selectors
  [vangheem]

- handle control panel prefixes for fields that do not
  have interfaces better.
  [vangheem]


1.2 (2012-08-29)
----------------

- Control panel: Records without interface no longer cause
  "AttributeError: 'NoneType' object has no attribute 'split'".
  [kleist]

- Allow deletion of records by interface in GenericSetup.
  [mitchellrj]

- Deprecated the 'delete' attribute of <record /> and <records /> nodes
  in GenericSetup, in favor of 'remove'.
  [mitchellrj]

- Show 'Changes canceled.' message after control panel edit form is canceled
  to comply with plone.app.controlpanel behavior.
  [timo]

- Redirect to the form itself on control panel edit form submit to comply with
  plone.app.controlpanel behavior.
  [timo]


1.2a1 (2012-06-29)
------------------

- Use lxml instead of elementtree.
  [davisagli]

- Remove unused zope.app.component import.
  [hannosch]

- Better control panel view.
  [vangheem]


1.1 (2012-04-15)
----------------

- Add support for internationalization of strings imported into the
  registry.
  [davisagli]


1.0.1 (2011-09-19)
------------------

- On the portal_registry configlet, enable the left-menu, to be more consistent
  with all other configlets.
  Fixes http://dev.plone.org/plone/ticket/11737
  [WouterVH]

- On the portal_registry configlet, add link to "Site Setup".
  Fixes http://dev.plone.org/plone/ticket/11855
  [WouterVH]


1.0 - 2011-05-13
----------------

- 1.0 Final release.
  [esteele]

- Add MANIFEST.in.
  [WouterVH]


1.0b6 - 2011-04-06
------------------

- Add ``collectionOfInterface`` export/import support.
  [elro]


1.0b5 - 2011-02-04
------------------

- Declare Products.CMFCore zcml dependency to fix zcml loading under Zope
  2.13.
  [elro]

- Add support for the <field ref="..." /> syntax to import FieldRefs.
  Requires plone.registry >= 1.0b4.
  [optilude]


1.0b4 - 2011-01-18
------------------

- Switch controlpanel slot to prefs_configlet_main.
  [toutpt]


1.0b3 - 2011-01-04
------------------

- Depend on ``Products.CMFPlone`` instead of ``Plone``.
  [elro]

- Show status messages and a back link in the control panel view.
  [timo]

- Use plone domain to translate messages of this package.
  [vincentfretin]

- Add a prefix support to controlpanel.RegistryEditForm
  [garbas]


1.0b2 - 2010-04-21
------------------

- Ensure fields that are imported from XML only (no interface) have a name.
  This fixes a problem with edit forms breaking.
  [optilude]

- Capitalize the control panel link to match the Plone standard.
  [esteele]

- Overlay now reloads the registry listing on successful submit.
  [esteele]

- Pass the name of the interface, not the interface itself to the <records />
  importer.
  [esteele]

- Modify JS overlay call to pull in the #content div.
  [esteele]

- Allow <value> elements inside <records> if they contain a key attribute.
  This uses the record importer to set the values after creation.
  [MatthewWilkes]

- Add a prefix attribute to the <records /> importer to take advantage of the
  interfaces-as-templates pattern from plone.registry
  [MatthewWilkes]

- Improved the look and feel of the registry records control panel.
  [optilude]

- Added explanation how to plug-in custom widgets for the registry [miohtama]


1.0b1 - 2009-08-02
------------------

- Test with plone.registry 1.0b1
  [optilude]


1.0a3 - 2009-07-12
------------------

- Catch up with changes in plone.supermodel's API.
  [optilude]


1.0a2 - 2009-04-17
------------------

- Fixed typo in ZCML registration; tuple has a 'p' in it.  This fixes exportimport of tuple fields.
  [MatthewWilkes]

- Add missing handlers.zcml include
  [MatthewWilkes]


1.0a1 - 2009-04-17
------------------

- Initial release
