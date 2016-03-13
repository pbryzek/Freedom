from get_search_results_api import APIGetSearchResultsRequest
from get_chart_api import APIGetChartRequest
from get_deep_comps_api import APIGetDeepCompsRequest

import consts.paths as paths
import time

class APIEngine(object):
    newline = "\n"
    ts = int(time.time())
    
    csv_path = paths.RESULTS_PATH + str(ts) + "_" + paths.RESULTS_CSV
    rentzestimate = True
    min_num_comps = 3
    #25 is the max
    num_comps_requested = 25

    def __init__(self, address, citystatezip):
        self.address = address
        self.citystatezip = citystatezip        

    def create_csv(self, home, comps):
        with open(self.csv_path, "a") as csvfile:        
            title_comma_separate = "address, citystatezip, chartlink, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent"
            csvfile = open(csv_path,'a')
            csvfile.write(title_comma_separate)
            csvfile.write(newline)

            comma_separated = home.create_csv()
            csvfile.write(comma_separated)

            for comp in comps:
                comp_comma_separated = comp.create_csv()
                csvfile.write(comp_comma_separated)
                csvfile.write(newline)

            csvfile.write(newline)

    def make_requests(self):
        #First get the zpid of the home in question
        get_search_api = APIGetSearchResultsRequest(self.address, self.citystatezip, self.rentzestimate)
        homes = get_search_api.request()
        home = homes[0]
        zpid = home.zpid

        #Get the chart api
        chart_api = APIGetChartRequest(zpid)
        home.chartlink = chart_api.request()

        #Get the comps for that home
        deep_comps_api = APIGetDeepCompsRequest(zpid, self.num_comps_requested)
        comps = deep_comps_api.request()

        if len(comps) >= self.min_num_comps:
            self.create_csv(home, comps)
        else:
            "Less than 3 comps found for zpid=" + zpid + " skipping"
