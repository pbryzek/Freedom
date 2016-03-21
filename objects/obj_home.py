class HomeObj(object):
    def __init__(self, type, address, citystatezip, dom, listing_id, beds, baths, yearbuilt, sqfootage, latitude, longitude, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent):

        self.address = address.replace(",", " ")
        self.citystatezip = citystatezip.replace(",", " ") 

        self.yearbuilt = yearbuilt
        self.sqfootage = sqfootage
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
        self.zestimate = zestimate 
        self.lastupdated = lastupdated 
        self.rentestimate = rentestimate 
        self.lastupdated_rent = lastupdated_rent

        #Distance from home, used to keep the csv consistent
        self.distance = 0

        self.dom = dom
        self.listing_id = listing_id

        self.type = type

    def create_csv(self):
        comma_separated = self.type + "," + self.address + "," + self.citystatezip + "," + str(self.dom) + "," + str(self.listing_id) + "," + self.beds + "," + self.baths + "," + self.sqfootage + "," + self.yearbuilt + "," + self.latitude + "," + self.longitude + "," + self.redfin_link + "," + self.chartlink + "," + self.homelink + "," + self.graphlink + "," + self.maplink + "," + self.compslink + "," + self.zpid + "," + self.zestimate + "," + self.lastupdated + "," + self.rentestimate + "," + self.lastupdated_rent + "," + str(self.distance)

        return comma_separated
