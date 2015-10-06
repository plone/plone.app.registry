# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface


class ITestSettings(Interface):

    name = schema.TextLine(title=u"Name", default=u"Mr. Registry")
    age = schema.Int(title=u"Age", min=0)


class ITestSettingsDisallowed(Interface):

    name = schema.TextLine(title=u"Name", default=u"Mr. Registry")
    age = schema.Int(title=u"Age", min=0)
    blob = schema.Object(title=u"Blob", schema=Interface)
