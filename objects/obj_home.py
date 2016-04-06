from common.globals import handle_err_msg
from common.globals import format_citystatezip
import consts.switches as switches

class HomeObj(object):
    def __init__(self, type, address, city, state, zip, dom, listing_id, beds, baths, yearbuilt, sqfootage, lotsize, latitude, longitude, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent, num_hot_words):

        self.address = address.replace(",", " ").strip()
        address_pieces = self.address.split()
        
        self.address_num = ""
        self.address_st = ""
        if len(address_pieces) > 0:
            self.address_num = address_pieces[0]
            address_num_len = len(self.address_num)
            self.address_st = self.address[address_num_len:].strip()

        if "-" in self.address_num:
             handle_err_msg("ERROR! found a dash in the property numbers: " + self.address)

        self.citystatezip = format_citystatezip(city, state, zip)

        self.city = city
        self.state = state
        self.zip = zip

        self.num_hot_words = num_hot_words
        self.yearbuilt = yearbuilt
        self.sqfootage = sqfootage
        self.lotsize = lotsize
        self.baths = baths
        self.beds = beds
        self.latitude = latitude
        self.longitude = longitude

        self.homelink = homelink 
        self.graphlink = graphlink 
        self.maplink = maplink 
        self.compslink = compslink 
        self.chartlink = ""
        self.redfin_link = ""

        self.zpid = zpid
        if not zestimate:
            zestimate = "-1" 
        self.zestimate = zestimate 
        self.lastupdated = lastupdated 
        self.rentestimate = rentestimate 
        self.lastupdated_rent = lastupdated_rent

        #Distance from home, used to keep the csv consistent
        self.distance = 0

        #If the DOM is less than the standard, then it is a tier 2 property
        if dom and not (dom is None):
            self.dom = dom
        else:
            self.dom = 0

        if dom < switches.MIN_DOM:
            self.tier = 2
        else:
            self.tier = 1
        self.listing_id = listing_id

        self.type = type

    def create_csv(self):
        if self.homelink is None:
            print "self.homelink is null"
        if self.graphlink is None:
            print "self.graphlink is None"
        if self.maplink is None:
            print "self.maplink is null"
        if self.compslink is None:
            print "self.compslink is None"
        if self.zpid is None:
            print "self.zpid is null"
        if self.zestimate is None:
            print "self.zestimate is None"
        comma_separated_1 = self.type + "," + self.address_num + "," + self.address_st + "," + self.city + "," + self.state + "," + self.zip + "," 
        comma_separated_2 = str(self.dom) + "," + str(self.listing_id) + "," + self.beds + "," + self.baths + "," + self.sqfootage + "," + str(self.lotsize) + "," 
        comma_separated_3 = self.yearbuilt + "," + self.latitude + "," + self.longitude + "," + self.redfin_link + "," + self.chartlink + "," 
        comma_separated_4 = self.homelink + "," + self.graphlink + "," + self.maplink + "," + self.compslink + "," + self.zpid + "," + self.zestimate + "," 
        comma_separated_5 = self.lastupdated + "," + self.rentestimate + "," + self.lastupdated_rent + "," + str(self.distance) + "," + str(self.num_hot_words)

        comma_separated = comma_separated_1 + comma_separated_2 + comma_separated_3 + comma_separated_4 + comma_separated_5
        return comma_separated
