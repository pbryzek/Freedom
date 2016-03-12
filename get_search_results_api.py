from base_api import BaseAPI
import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj


# create the client
class APIGetSearchResultsRequest(BaseAPI):
    def __init__(self, address, citystatezip, rentzestimate=False):
        #To build the home object
        self.address = address
        self.citystatezip = citystatezip
        self.homelink = ""
        self.graphlink = ""
        self.maplink = ""
        self.compslink = ""
        self.zpid = ""
        self.zestimate = ""
        self.lastupdated = ""
        self.rentestimate = ""
        self.lastupdated_rent = ""
        self.homes = []

        #Specific endpoint
        path = paths.GET_SEARCH_RESULTS
       
        #Params to send with request
        params = {"address": address, "citystatezip": citystatezip, "rentzestimate":rentzestimate}

        super(APIGetSearchResultsRequest, self).__init__(path, params)

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

    def parse_results(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_RESULT:
                self.parse_result(child)
                home = HomeObj(self.address, self.citystatezip, self.homelink, self.graphlink, self.maplink, self.compslink, self.zpid, self.zestimate, self.lastupdated, self.rentestimate, self.lastupdated_rent)
                self.homes.append(home)

        if len(self.homes) > 1:
            print "get_search_results parse_results num_results > 1!!!"

    def parse_response(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_RESULTS:
                self.parse_results(child)

    def request(self):
        response = super(APIGetSearchResultsRequest, self).request()
        print "Response = " + response.content

        root = ET.fromstring(response.content)
        for child in root:
            tag = child.tag
            if tag == tags.TAG_MESSAGE:
                super(APIGetSearchResultsRequest, self).parse_error_msg(child)
            elif tag == tags.TAG_RESPONSE:
                self.parse_response(child)
            
        return self.homes

"""
<?xml version="1.0" encoding="utf-8"?><SearchResults:searchresults xsi:schemaLocation="http://www.zillow.com/static/xsd/SearchResults.xsd http://www.zillowstatic.com/vstatic/9041678/static/xsd/SearchResults.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SearchResults="http://www.zillow.com/static/xsd/SearchResults.xsd"><request><address>333 Pali Court</address><citystatezip>Oakland, CA 94611</citystatezip></request><message><text>Request successfully processed</text><code>0</code></message><response><results><result><zpid>24819940</zpid><links><homedetails>http://www.zillow.com/homedetails/333-Pali-Ct-Oakland-CA-94611/24819940_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/333-Pali-Ct-Oakland-CA-94611/24819940_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24819940_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24819940_zpid/</comparables></links><address><street>333 Pali Ct</street><zipcode>94611</zipcode><city>Oakland</city><state>CA</state><latitude>37.846186</latitude><longitude>-122.224464</longitude></address>

<zestimate><amount currency="USD">2342467</amount><last-updated>03/11/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">-11230</valueChange><valuationRange><low currency="USD">2178494</low><high currency="USD">2483015</high></valuationRange><percentile>0</percentile></zestimate><rentzestimate><amount currency="USD">8044</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">-53</valueChange><valuationRange><low currency="USD">6837</low><high currency="USD">13594</high></valuationRange></rentzestimate><localRealEstate><region name="Merriwood" id="268289" type="neighborhood"><zindexValue>949,900</zindexValue><links><overview>http://www.zillow.com/local-info/CA-Oakland/Merriwood/r_268289/</overview><forSaleByOwner>http://www.zillow.com/merriwood-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/merriwood-oakland-ca/</forSale></links></region></localRealEstate></result></results></response></SearchResults:searchresults><!-- H:001  T:31ms  S:1097  R:Sat Mar 12 14:16:36 PST 2016  B:4.0.25909-master.a723596~hotfix_pre.53ac87d -->
"""
