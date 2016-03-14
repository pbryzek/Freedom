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
    ts = int(time.time())
    csv_path = paths.RESULTS_PATH + str(ts) + "_" + paths.RESULTS_CSV
    
    def __init__(self, address, citystatezip, redfin_link):
        self.address = address
        self.citystatezip = citystatezip       
        self.redfin_link = redfin_link 

    def create_csv(self, home, comps):
        with open(self.csv_path, "a") as csvfile:        
            title_comma_separate = "address, citystatezip, beds, baths, sqfootage, yearbuilt, latitude, longitude, redfin link, chartlink, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent"
            csvfile.write(title_comma_separate)
            csvfile.write(self.newline)

            comma_separated = home.create_csv()
            csvfile.write(comma_separated)

            for comp in comps:
                comp_comma_separated = comp.create_csv()
                csvfile.write(comp_comma_separated)
                csvfile.write(self.newline)

            csvfile.write(self.newline)

    def make_requests(self):
        print ""
        print "Getting info for property: " + self.address + " " + self.citystatezip
        #First get the zpid of the home in question

        ##get_search_api = APIGetSearchResultsRequest(self.address, self.citystatezip, switches.RENTZESTIMATE)
        ##homes = get_search_api.request()
        ##if len(homes) == 0:
        ##    print "Get Search Results API did not return any results!"
        ##    return

        get_deep_search_api = APIGetDeepSearchResultsRequest(self.address, self.citystatezip, switches.RENTZESTIMATE)
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
        deep_comps_api = APIGetDeepCompsRequest(zpid, switches.NUM_COMPS_REQUESTED)
        deep_comps = deep_comps_api.request()

        if len(deep_comps) < switches.MIN_NUM_COMPS:
            print "Only " + str(len(deep_comps)) + " deep comps found which is less than the min of " + str(switches.MIN_NUM_COMPS) + " zpid=" + zpid

        #Get the comps for that home
        comps_api = APIGetCompsRequest(zpid, switches.NUM_COMPS_REQUESTED)
        comps = comps_api.request()

        if len(comps) < switches.MIN_NUM_COMPS:
            print "Only " + str(len(comps)) + " comps found which is less than the min of " + str(switches.MIN_NUM_COMPS) + " zpid=" + zpid  

        total_comps = len(deep_comps) + len(comps)
        if total_comps < switches.MIN_NUM_COMPS:
            print "A total of " + str(total_comps) + " were found, skipping."
            return 

        #Get the chart api
        chart_api = APIGetChartRequest(zpid)
        home.chartlink = chart_api.request()

        #Finally put the results in a csv 
        self.create_csv(home, comps)
