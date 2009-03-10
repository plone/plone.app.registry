import plone.supermodel.exportimport
from plone.registry import field

# Field import/export handlers

BytesHandler = plone.supermodel.exportimport.BaseHandler(field.Bytes)
BytesLineHandler = plone.supermodel.exportimport.BaseHandler(field.BytesLine)

ASCIIHandler = plone.supermodel.exportimport.BaseHandler(field.ASCII)
ASCIILineHandler = plone.supermodel.exportimport.BaseHandler(field.ASCIILine)

TextHandler = plone.supermodel.exportimport.BaseHandler(field.Text)
TextLineHandler = plone.supermodel.exportimport.BaseHandler(field.TextLine)

PasswordHandler = plone.supermodel.exportimport.BaseHandler(field.Password)
SourceTextHandler = plone.supermodel.exportimport.BaseHandler(field.SourceText)

DottedNameHandler = plone.supermodel.exportimport.BaseHandler(field.DottedName)
URIHandler = plone.supermodel.exportimport.BaseHandler(field.URI)
IdHandler = plone.supermodel.exportimport.BaseHandler(field.Id)

BoolHandler = plone.supermodel.exportimport.BaseHandler(field.Bool)
IntHandler = plone.supermodel.exportimport.BaseHandler(field.Int)
FloatHandler = plone.supermodel.exportimport.BaseHandler(field.Float)

DatetimeHandler = plone.supermodel.exportimport.BaseHandler(field.Datetime)
DateHandler = plone.supermodel.exportimport.BaseHandler(field.Date)

TupleHandler = plone.supermodel.exportimport.BaseHandler(field.Tuple)
ListHandler = plone.supermodel.exportimport.BaseHandler(field.List)
SetHandler = plone.supermodel.exportimport.BaseHandler(field.Set)
FrozenSetHandler = plone.supermodel.exportimport.BaseHandler(field.FrozenSet)

DictHandler = plone.supermodel.exportimport.DictHandler(field.Dict)

ChoiceHandler = plone.supermodel.exportimport.ChoiceHandler(field.Choice)