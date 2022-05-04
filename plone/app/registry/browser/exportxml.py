from lxml import etree
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility

import os


_current_dir = os.path.dirname(__file__)


def _sort_first_lower(key):
    return key[0].lower()


class RegistryExporterView(BrowserView):
    """this view make sane exports of the registry.

    Main goal is to export in a way, that the output can be reused as
    best practive settings
    """

    template = ViewPageTemplateFile(
        os.path.join(_current_dir, "templates", "exportxml.pt")
    )

    def __call__(self):
        interface = self.request.form.get("interface", None)
        name = self.request.form.get("name", None)
        if not interface and not name:
            return self.template()
        return self.export(sinterface=interface, sname=name)

    def interfaces(self):
        prefixes = []
        registry = getUtility(IRegistry)
        baseurl = "{}/@@configuration_registry_export_xml?interface=".format(
            self.context.absolute_url()
        )
        for record in registry.records.values():
            if record.interfaceName is None:
                continue
            name = record.interfaceName
            url = f"{baseurl}{record.interfaceName}"
            pair = (name, url)
            if pair not in prefixes:
                prefixes.append(pair)

        return sorted(prefixes, key=_sort_first_lower)

    def prefixes(self):
        prefixes = []
        registry = getUtility(IRegistry)
        baseurl = "{}/@@configuration_registry_export_xml?".format(
            self.context.absolute_url()
        )
        for record in registry.records.values():
            if record.interfaceName == record.__name__:
                continue

            def add_split(part):
                url = f"{baseurl}name={part}"
                pair = (part, url)
                if pair not in prefixes:
                    prefixes.append(pair)
                if part.rfind("/") > part.rfind("."):
                    new_parts = part.rsplit("/", 1)
                else:
                    new_parts = part.rsplit(".", 1)
                if len(new_parts) > 1:
                    add_split(new_parts[0])

            add_split(record.__name__)
        return sorted(prefixes, key=_sort_first_lower)

    def export(self, sinterface=None, sname=None):
        registry = getUtility(IRegistry)
        root = etree.Element("registry")
        values = {}  # full prefix to valuerecord
        interface2values = {}
        interface2prefix = {}
        for record in registry.records.values():
            if sinterface and sinterface != record.interfaceName:
                continue
            if sname and not record.__name__.startswith(sname):
                continue
            prefix, value_key = record.__name__.rsplit(".", 1)
            xmlvalue = etree.Element("value")
            if record.value is None:
                continue
            if isinstance(record.value, (list, tuple)):
                for element in record.value:
                    xmlel = etree.SubElement(xmlvalue, "element")
                    xmlel.text = element
            elif isinstance(record.value, bool):
                xmlvalue.text = "True" if record.value else "False"
            elif isinstance(record.value, str):
                xmlvalue.text = record.value
            else:
                xmlvalue.text = str(record.value)

            if record.interfaceName:
                xmlvalue.attrib["key"] = value_key
                if record.interfaceName not in interface2values:
                    interface2values[record.interfaceName] = []
                interface2values[record.interfaceName].append(record.__name__)
                interface2prefix[record.interfaceName] = prefix
            values[record.__name__] = xmlvalue

        for ifname in sorted(interface2values):
            xmlrecord = etree.SubElement(root, "records")
            xmlrecord.attrib["interface"] = ifname
            xmlrecord.attrib["prefix"] = interface2prefix[ifname]
            for value in sorted(interface2values[ifname]):
                xmlrecord.append(values.pop(value))
        for name, xmlvalue in values.items():
            xmlrecord = etree.SubElement(root, "records")
            xmlrecord.attrib["prefix"] = name
            xmlrecord.append(xmlvalue)

        self.request.response.setHeader("Content-Type", "text/xml")
        filename = ""
        if sinterface:
            filename += sinterface
        if sinterface and sname:
            filename += "_-_"
        if sname:
            filename += sname
        self.request.response.setHeader(
            "Content-Disposition", f"attachment; filename={filename}.xml"
        )
        return etree.tostring(
            root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )
