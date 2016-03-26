import haversine

import dateutil.parser

class CompObj(object):
    def __init__(self, home, principal_lat, principal_long, comp_score, soldprice, solddate):
        self.home = home
        self.principal_lat = principal_lat
        self.principal_long = principal_long
        self.comp_score = comp_score['score']
        self.soldprice = soldprice
        self.solddate = solddate
        self.sqftprice = int(soldprice) / int(home.sqfootage) 
        solddate_date = dateutil.parser.parse(solddate)
        self.solddate_sf = solddate_date.isoformat()
        self.distance = self.get_distance()

    def get_distance(self):
        principal_point = (float(self.principal_lat), float(self.principal_long))
        comp_point = (float(self.home.latitude), float(self.home.longitude))
 
        miles = haversine.distance(principal_point, comp_point)

        return miles      

    def create_csv(self):
        distance = self.get_distance()
        self.home.distance = distance
        home_csv = self.home.create_csv()

        home_csv += "," + str(self.soldprice) + "," + str(self.solddate) + "," + str(self.comp_score) + "," + str(self.sqftprice)

        return home_csv     
