from .modules import DiscoverModule
from packethardware import utils
from packethardware.component import Component
from lxml import etree


class DiscoveredComponents(list):
    def flatten(self):
        return [x.post_dict() for x in self]


class DiscoverComponents(DiscoverModule):
    def run(self, data):
        data["components"] = DiscoveredComponents()
        lshw = etree.ElementTree(etree.fromstring(utils.lshw()))

        for component in Component.__subclasses__():
            data["components"].extend(component.list(lshw))
