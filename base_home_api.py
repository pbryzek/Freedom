from base_api import BaseAPI
import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj
import common.globals as globals

from abc import ABCMeta, abstractmethod

class BaseHomeAPI(BaseAPI):
    __metaclass__ = ABCMeta

    def __init__(self, type, path, params):
        super(BaseHomeAPI, self).__init__(path, params)

        #What type of property is this, e.g. redfin, agent, foreclosure etc.
        self.type = type

        self.num_hot_words = 0
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.citystatezip = ""
        self.latitude = ""
        self.longitude = ""
        self.yearbuilt = ""
        self.beds = "" 
        self.baths = "" 
        self.sqfootage = "" 
        self.lotsize = ""

        self.homelink = ""
        self.graphlink = ""
        self.maplink = ""
        self.compslink = ""
        self.zpid = ""
        self.zestimate = ""
        self.lastupdated = ""
        self.rentestimate = ""
        self.lastupdated_rent = ""

        self.soldprice = ""
        self.solddate = ""
        self.dom = ""
        self.listing_id = ""
        self.homes = []

    def parse_address(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_LATITUDE:
                self.latitude = child.text
            elif tag == tags.TAG_LONGITUDE:
                self.longitude = child.text

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
            elif tag == tags.TAG_YEARBUILT:
                self.yearbuilt = child.text
            elif tag == tags.TAG_SQ_FOOTAGE:
                self.sqfootage = child.text
            elif tag == tags.TAG_LOT_SIZE:
                self.lotsize = child.text
            elif tag == tags.TAG_BATHROOMS:
                self.baths = child.text
            elif tag == tags.TAG_BEDROOMS:
                self.beds = child.text
            elif tag == tags.TAG_SOLD_PRICE:
                self.soldprice = child.text
            elif tag == tags.TAG_SOLD_DATE:
                self.solddate = child.text

    def parse_results(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_RESULT:
                self.parse_result(child)

                home = HomeObj(self.type, self.address, self.city, self.state, self.zip, self.dom, self.listing_id, self.beds, self.baths, self.yearbuilt, self.sqfootage, self.lotsize, self.latitude, self.longitude, self.homelink, self.graphlink, self.maplink, self.compslink, self.zpid, self.zestimate, self.lastupdated, self.rentestimate, self.lastupdated_rent, self.num_hot_words)
                self.homes.append(home)

        if len(self.homes) > 1:
            globals.handle_err_msg("get_search_results parse_results num_results > 1!!!")

    def parse_response(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_RESULTS:
                self.parse_results(child)    
