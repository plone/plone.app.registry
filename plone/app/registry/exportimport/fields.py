from plone.supermodel.exportimport import BaseHandler
from plone.registry import field

# Field import/export handlers

BytesHandler = BaseHandler(field.Bytes, element_name="field")
BytesLineHandler = BaseHandler(field.BytesLine, element_name="field")

ASCIIHandler = BaseHandler(field.ASCII, element_name="field")
ASCIILineHandler = BaseHandler(field.ASCIILine, element_name="field")

IdHandler = BaseHandler(field.Id, element_name="field")
DottedNameHandler = BaseHandler(field.DottedName, element_name="field")
TextHandler = BaseHandler(field.Text, element_name="field")
TextLineHandler = BaseHandler(field.TextLine, element_name="field")

PasswordHandler = BaseHandler(field.Password, element_name="field")
URIHandler = BaseHandler(field.URI, element_name="field")
SourceTextHandler = BaseHandler(field.SourceText, element_name="field")

BoolHandler = BaseHandler(field.Bool, element_name="field")
IntHandler = BaseHandler(field.Int, element_name="field")
FloatHandler = BaseHandler(field.Float, element_name="field")

DatetimeHandler = BaseHandler(field.Datetime, element_name="field")
DateHandler = BaseHandler(field.Date, element_name="field")
TimedeltaHandler = BaseHandler(field.Timedelta, element_name="field")

TupleHandler = BaseHandler(field.Tuple, element_name="field")
ListHandler = BaseHandler(field.List, element_name="field")
SetHandler = BaseHandler(field.Set, element_name="field")
FrozenSetHandler = BaseHandler(field.FrozenSet, element_name="field")

DictHandler = BaseHandler(field.Dict, element_name="field")