from base_api import BaseAPI
import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj

from abc import ABCMeta, abstractmethod

class BaseHomeAPI(BaseAPI):
    __metaclass__ = ABCMeta

    def __init__(self, path, params):
        super(BaseHomeAPI, self).__init__(path, params)

        self.address = ""
        self.citystatezip = ""
        self.homelink = ""
        self.graphlink = ""
        self.maplink = ""
        self.compslink = ""
        self.zpid = ""
        self.zestimate = ""
        self.lastupdated = ""
        self.rentestimate = ""
        self.lastupdated_rent = ""
        self.homes = []

    @abstractmethod
    def parse_address(self, node):
        raise NotImplementedError("Must override parse_address")

    def parse_links(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_HOMELINK:
                self.homelink = child.text
            elif tag == tags.TAG_GRAPHLINK:
                self.graphlink = child.text
            elif tag == tags.TAG_MAPLINK:
                self.maplink = child.text
            elif tag == tags.TAG_COMPSLINK:
                self.compslink = child.text

    def parse_rentestimate(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_AMOUNT:
                self.rentestimate = child.text
            elif tag == tags.TAG_LASTUPDATED:
                self.lastupdated_rent = child.text

    def parse_zestimate(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_AMOUNT:
                self.zestimate = child.text
            elif tag == tags.TAG_LASTUPDATED:
                self.lastupdated = child.text


    def parse_result(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_ZPID:
                self.zpid = child.text
            elif tag == tags.TAG_LINKS:
                self.parse_links(child)
            elif tag == tags.TAG_ZESTIMATE:
                self.parse_zestimate(child)
            elif tag == tags.TAG_RENTESTIMATE:
                self.parse_rentestimate(child)
            elif tag == tags.TAG_ADDRESS:
                self.parse_address(child)

    def parse_results(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_RESULT:
                self.parse_result(child)
                home = HomeObj(self.address, self.citystatezip, self.homelink, self.graphlink, self.maplink, self.compslink, self.zpid, self.zestimate, self.lastupdated, self.rentestimate, self.lastupdated_rent)
                self.homes.append(home)

        if len(self.homes) > 1:
            print "get_search_results parse_results num_results > 1!!!"

    def parse_response(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_RESULTS:
                self.parse_results(child)    

