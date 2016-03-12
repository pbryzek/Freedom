from get_search_results_api import APIGetSearchResultsRequest
import consts.paths as paths

address = "333 Pali Court"
citystatezip = "Oakland, CA 94611"
rentzestimate = True

newline = "\n"
title_comma_separate = "address, citystatezip, homelink, graphlink, maplink, compslink, zpid, zestimate, lastupdated, rentestimate, lastupdated_rent"

csv_path = paths.RESULTS_PATH + paths.RESULTS_CSV

f = open(csv_path,'w')
f.write(title_comma_separate)
f.write(newline) 

get_search_api = APIGetSearchResultsRequest(address, citystatezip, rentzestimate)
homes = get_search_api.request()
home = homes[0]
comma_separated = home.create_csv()
f.write(comma_separated)

f.close()
