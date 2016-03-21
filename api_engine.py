from get_search_results_api import APIGetSearchResultsRequest
from get_chart_api import APIGetChartRequest
from get_deep_comps_api import APIGetDeepCompsRequest
from get_comps_api import APIGetCompsRequest
from get_deep_search_results_api import APIGetDeepSearchResultsRequest

import consts.paths as paths
import consts.switches as switches
import time

class APIEngine(object):

    newline = "\n"
    csv_path = ""
    
    def __init__(self, address, citystatezip, redfin_link, dom, listing_id, type):
        self.address = address
        self.citystatezip = citystatezip       
        self.redfin_link = redfin_link
        self.dom = dom 
        self.listing_id = listing_id
        self.type = type
        ts = int(time.time())
        if type == switches.PROPERTY_TYPE_REDFIN:
            self.csv_path = paths.RESULTS_PATH + paths.REDFIN_RESULTS_PATH + "_" + str(ts) + paths.CSV_ENDING

    def create_csv(self, home, comps):
        with open(self.csv_path, "a") as csvfile: 
            main_csv_string = ""
       
            title_comma_separate = "prop type, address, citystatezip, dom, listing_id, beds, baths, sqfootage, yearbuilt, latitude, longitude, redfin link, chartlink, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent, distance, sold price, sold date, comp score, $/sqft"

            main_csv_string += title_comma_separate
            main_csv_string += self.newline
            
            comma_separated = home.create_csv()
            main_csv_string += comma_separated
            main_csv_string += self.newline

            print "Evaluating " + str(len(comps)) + " valid comps"
            principal_arv = 0
            sqft_aggregate_value = 0
            
            for comp in comps:
                comp_comma_separated = comp.create_csv()
                main_csv_string += comp_comma_separated
                main_csv_string += self.newline

                sqft_value = int(comp.sqftprice)
                sqft_aggregate_value += sqft_value

            num_comps = len(comps)
            if num_comps == 0:
                return

            #Get the average price/sqft for comps sold
            avg_sqft_price = sqft_aggregate_value / num_comps

            principal_arv = 0
            principal_sqfootage = 0
            if home.sqfootage.strip() != '':
                principal_sqfootage = int(home.sqfootage)
                principal_arv = avg_sqft_price * principal_sqfootage
            repair_light = (principal_sqfootage * switches.LIGHT_REHAB)
            repair_med = (principal_sqfootage * switches.MEDIUM_REHAB)
            repair_high = (principal_sqfootage * switches.HIGH_REHAB)

            commision = 0
            if principal_arv < switches.PRICE_POINT_1:
                commision = switches.COMMISSION_POINT_1
            elif principal_arv < switches.PRICE_POINT_2:
                commision = switches.COMMISSION_POINT_2
            else:
                commision = switches.COMMISSION_POINT_3

            arv = (switches.ARV_PERCENTAGE * principal_arv)
            mao_light = arv - repair_light - commision
            mao_med = arv - repair_med - commision
            mao_high = arv - repair_high - commision

            #If the mao_med is greater than our max price, skip this home
            if switches.MAX_PRICE < mao_med:
                return

            #Finally write out the string
            csvfile.write(main_csv_string)

            mao_header = "principal_arv,avg $/sqft, mao_light,mao_med,mao_high" 
            mao_comma_separated = str(principal_arv) + "," + str(avg_sqft_price) + "," + str(mao_light) + "," + str(mao_med) + "," + str(mao_high)
            csvfile.write(mao_header)
            csvfile.write(self.newline)
            csvfile.write(mao_comma_separated)
            csvfile.write(self.newline)           
 
            csvfile.write(self.newline)

    def make_requests(self):
        print ""
        print "Getting info for property: " + self.address + " " + self.citystatezip
        #First get the zpid of the home in question

        ##get_search_api = APIGetSearchResultsRequest(self.type, self.address, self.citystatezip, switches.RENTZESTIMATE)
        ##homes = get_search_api.request()
        ##if len(homes) == 0:
        ##    print "Get Search Results API did not return any results!"
        ##    return

        get_deep_search_api = APIGetDeepSearchResultsRequest(self.type, self.address, self.citystatezip, self.dom, self.listing_id, switches.RENTZESTIMATE)
        homes = get_deep_search_api.request()
        if len(homes) == 0:
            print "Get Deep Search Results API did not return any results!"
            return

        home = homes[0]
        home.redfin_link = self.redfin_link
        #self.create_csv(home, [])
        #return 

        zpid = home.zpid

        #Get the deep comps for that home
        deep_comps_api = APIGetDeepCompsRequest(self.type, zpid, switches.NUM_COMPS_REQUESTED, home.latitude, home.longitude, home.sqfootage)
        deep_comps = deep_comps_api.request()

        #self.create_csv(home, deep_comps)
        #return

        if len(deep_comps) < switches.MIN_NUM_COMPS:
            print "Only " + str(len(deep_comps)) + " deep comps found which is less than the min of " + str(switches.MIN_NUM_COMPS) + " zpid=" + zpid

        #Get the comps for that home
        comps = []
        #comps_api = APIGetCompsRequest(self.type, zpid, switches.NUM_COMPS_REQUESTED)
        #comps = comps_api.request()

        #if len(comps) < switches.MIN_NUM_COMPS:
        #    print "Only " + str(len(comps)) + " comps found which is less than the min of " + str(switches.MIN_NUM_COMPS) + " zpid=" + zpid  

        total_comps = len(deep_comps) + len(comps)
        if total_comps < switches.MIN_NUM_COMPS:
            print "A total of " + str(total_comps) + " were found, skipping."
            return 

        #Get the chart api
        #chart_api = APIGetChartRequest(zpid)
        #home.chartlink = chart_api.request()

        #Finally put the results in a csv 
        self.create_csv(home, deep_comps)
