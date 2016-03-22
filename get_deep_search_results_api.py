from base_home_api import BaseHomeAPI

import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj


# create the client
class APIGetDeepSearchResultsRequest(BaseHomeAPI):
    def __init__(self, type, address, citystatezip, dom, listing_id, num_hot_words, rentzestimate=False):
        #Specific endpoint
        path = paths.GET_DEEP_SEARCH_RESULTS

        #Params to send with request
        params = {"address": address, "citystatezip": citystatezip, "rentzestimate":rentzestimate}

        super(APIGetDeepSearchResultsRequest, self).__init__(type, path, params)

        #To build the home object
        self.address = address
        self.citystatezip = citystatezip
        self.dom = dom
        self.listing_id = listing_id
        self.num_hot_words = num_hot_words

    def request(self):
        response = super(APIGetDeepSearchResultsRequest, self).request()
 
        root = ET.fromstring(response.content)
        for child in root:
            tag = child.tag
            if tag == tags.TAG_MESSAGE:
                err_code = super(BaseHomeAPI, self).parse_error_msg(child)
            elif tag == tags.TAG_RESPONSE:
                self.parse_response(child)

        return self.homes
"""
<?xml version="1.0" encoding="utf-8"?><SearchResults:searchresults xsi:schemaLocation="http://www.zillow.com/static/xsd/SearchResults.xsd http://www.zillowstatic.com/vstatic/9041678/static/xsd/SearchResults.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SearchResults="http://www.zillow.com/static/xsd/SearchResults.xsd"><request><address>2629 75 TH Ave</address><citystatezip>Oakland, CA 94605</citystatezip></request><message><text>Request successfully processed</text><code>0</code></message><response><results><result><zpid>24792995</zpid><links><homedetails>http://www.zillow.com/homedetails/2629-75th-Ave-Oakland-CA-94605/24792995_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/2629-75th-Ave-Oakland-CA-94605/24792995_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24792995_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24792995_zpid/</comparables></links><address><street>2629 75th Ave</street><zipcode>94605</zipcode><city>Oakland</city><state>CA</state><latitude>37.766287</latitude><longitude>-122.174004</longitude></address><FIPScounty>6001</FIPScounty><useCode>SingleFamily</useCode><taxAssessmentYear>2015</taxAssessmentYear><taxAssessment>105533.0</taxAssessment><yearBuilt>1941</yearBuilt><lotSizeSqFt>2500</lotSizeSqFt><finishedSqFt>910</finishedSqFt><bathrooms>1.0</bathrooms><bedrooms>2</bedrooms><totalRooms>4</totalRooms><lastSoldDate>04/22/2011</lastSoldDate><lastSoldPrice currency="USD">99000</lastSoldPrice><zestimate><amount currency="USD">255607</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">2891</valueChange><valuationRange><low currency="USD">219822</low><high currency="USD">278612</high></valuationRange><percentile>0</percentile></zestimate><rentzestimate><amount currency="USD">1925</amount><last-updated>03/13/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">-4</valueChange><valuationRange><low currency="USD">1752</low><high currency="USD">2291</high></valuationRange></rentzestimate><localRealEstate><region name="Eastmont" id="268129" type="neighborhood"><zindexValue>289,400</zindexValue><links><overview>http://www.zillow.com/local-info/CA-Oakland/Eastmont/r_268129/</overview><forSaleByOwner>http://www.zillow.com/eastmont-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/eastmont-oakland-ca/</forSale></links></region></localRealEstate></result></results></response></SearchResults:searchresults><!-- H:001  T:27ms  S:1434  R:Sun Mar 13 17:50:02 PDT 2016  B:4.0.25909-master.a723596~hotfix_pre.53ac87d -->
"""
