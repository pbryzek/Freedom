class HomeObj(object):
    def __init__(self, address, citystatezip, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent):

        self.address = address.replace(",", " ")
        self.citystatezip = citystatezip.replace(",", " ") 

        self.homelink = homelink 
        self.graphlink = graphlink 
        self.maplink = maplink 
        self.compslink = compslink 
        self.zpid = zpid 
        self.zestimate = zestimate 
        self.lastupdated = lastupdated 
        self.rentestimate = rentestimate 
        self.lastupdated_rent = lastupdated_rent

    def create_csv(self):
        comma_separated = self.address + "," + self.citystatezip + "," + self.homelink + "," + self.graphlink + "," + self.maplink + "," + self.compslink + "," + self.zpid + "," + self.zestimate + "," + self.lastupdated + "," + self.rentestimate + "," + self.lastupdated_rent

        return comma_separated
