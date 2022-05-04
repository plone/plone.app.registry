from zope import schema
from zope.interface import Interface


class ITestSettings(Interface):

    name = schema.TextLine(title="Name", default="Mr. Registry")
    age = schema.Int(title="Age", min=0)


class ITestSettingsDisallowed(Interface):

    name = schema.TextLine(title="Name", default="Mr. Registry")
    age = schema.Int(title="Age", min=0)
    blob = schema.Object(title="Blob", schema=Interface)
