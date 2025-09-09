from OFS.SimpleItem import SimpleItem
from plone.registry import registry


class Registry(registry.Registry, SimpleItem):
    """A Zope 2 style registry"""

    def __init__(self, id, title=None):
        super().__init__()

        self.id = id
        self.title = title
