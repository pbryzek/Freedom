from base_home_api import BaseHomeAPI

import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj
from objects.obj_comp import CompObj

import consts.switches as switches
from common.globals import handle_err_msg

import time

# create the client
class APIGetDeepCompsRequest(BaseHomeAPI):

    def __init__(self, type, zpid, count, principal_lat, principal_long, principal_sqfootage):
        #Specific endpoint
        path = paths.GET_DEEP_COMPS

        #Params to send with request
        params = {"zpid": zpid, "count": count}

        super(APIGetDeepCompsRequest, self).__init__(type, path, params)

        self.principal_lat = principal_lat 
        self.principal_long = principal_long
        self.principal_sqfootage = principal_sqfootage

    #Called from the parent.
    def parse_address(self, node):
        self.city = ""
        self.state = ""
        self.zip = ""

        for child in node:
            tag = child.tag
            if tag == tags.TAG_LATITUDE:
                self.latitude = child.text
            elif tag == tags.TAG_LONGITUDE:
                self.longitude = child.text
            elif tag == tags.TAG_STREET:
                self.address = child.text
            elif tag == tags.TAG_CITY:
                self.city = child.text
            elif tag == tags.TAG_STATE:
                self.state = child.text
            elif tag == tags.TAG_ZIP:
                self.zip = child.text

    def parse_comp(self, node):
        comp_score = node.attrib
        #Leverage the parent's parsing mechanism
        self.parse_result(node)

        home = HomeObj(self.type, self.address, self.city, self.state, self.zip, "", "", self.beds, self.baths, self.yearbuilt, self.sqfootage, self.lotsize, self.latitude, self.longitude, self.homelink, self.graphlink, self.maplink, self.compslink, self.zpid, self.zestimate, self.lastupdated, self.rentestimate, self.lastupdated_rent, 0)

        comp = CompObj(home, self.principal_lat, self.principal_long, comp_score, self.soldprice, self.solddate)
        miles = comp.get_distance()
        sqfootage = int(home.sqfootage)

        #Do rules to see if these are valid comps
        if miles > switches.MAX_DISTANCE_FROM_PRINCIPAL:
            handle_err_msg("Comp property is " + str(miles) + " away from the principal and max allowed miles = " + str(switches.MAX_DISTANCE_FROM_PRINCIPAL) + " skipping")
            return

        if self.principal_sqfootage.strip() != '':
            min_sqfootage = int(self.principal_sqfootage) * (1-switches.SQ_FOOTAGE_PERCENTAGE) 
            max_sqfootage = int(self.principal_sqfootage) * (1+switches.SQ_FOOTAGE_PERCENTAGE)
            if (sqfootage < min_sqfootage) or (sqfootage > max_sqfootage):
                handle_err_msg("Comp property sq footage is " + str(sqfootage) + " which is outside the allowed range of min: " + str(min_sqfootage) + " max: " + str(max_sqfootage) + " skipping")
                return              

        if self.solddate.strip() != '':
            solddate_time = time.strptime(self.solddate, "%m/%d/%Y") 

            now_str = time.strftime("%m/%d/%Y")       
            now_time = time.strptime(now_str, "%m/%d/%Y")

            #Num seconds different
            time_diff_s = (time.mktime(now_time) - time.mktime(solddate_time)) / 60 
            time_diff_m = time_diff_s / 60
            time_diff_h = time_diff_s / 60
            time_diff_d = time_diff_h / 24
            time_diff_mon = time_diff_d / 30

            if switches.SOLD_PRICE_INTERVAL < time_diff_mon:
                handle_err_msg("Sold date: " + str(self.solddate) + " is " + str(time_diff_mon) + " months diff which is > than the max of " + str(switches.SOLD_PRICE_INTERVAL) + " skipping")
                return

        self.homes.append(comp)

    def parse_comparables(self, node):
        num_comps = 0
        for child in node:
            tag = child.tag
            if tag == tags.TAG_COMP:
                num_comps += 1
                self.parse_comp(child)

        handle_err_msg("Found a total of " + str(num_comps) + " total comps")

    def parse_properties(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_PRINCIPAL:
                pass
            elif tag == tags.TAG_COMPARABLES:
                self.parse_comparables(child)

    def parse_response(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_PROPERTIES:
                self.parse_properties(child)

    def request(self):
        response = super(APIGetDeepCompsRequest, self).request()

        root = ET.fromstring(response.content)
        for child in root:
            tag = child.tag
            if tag == tags.TAG_MESSAGE:
                err_code = super(BaseHomeAPI, self).parse_error_msg(child)
                if err_code == self.NO_RESULTS:
                    return []
            elif tag == tags.TAG_RESPONSE:
                self.parse_response(child)

        return self.homes

"""
<?xml version="1.0" encoding="utf-8"?><Comps:comps xsi:schemaLocation="http://www.zillow.com/static/xsd/Comps.xsd http://www.zillowstatic.com/vstatic/9041678/static/xsd/Comps.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:Comps="http://www.zillow.com/static/xsd/Comps.xsd"><request><zpid>24792995</zpid><count>2</count></request><message><text>Request successfully processed</text><code>0</code></message><response><properties><principal><zpid>24792995</zpid><links><homedetails>http://www.zillow.com/homedetails/2629-75th-Ave-Oakland-CA-94605/24792995_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/2629-75th-Ave-Oakland-CA-94605/24792995_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24792995_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24792995_zpid/</comparables></links><address><street>2629 75th Ave</street><zipcode>94605</zipcode><city>Oakland</city><state>CA</state><latitude>37.766287</latitude><longitude>-122.174004</longitude></address><taxAssessmentYear>2015</taxAssessmentYear><taxAssessment>105533.0</taxAssessment><yearBuilt>1941</yearBuilt><lotSizeSqFt>2500</lotSizeSqFt><finishedSqFt>910</finishedSqFt><bathrooms>1.0</bathrooms><bedrooms>2</bedrooms><totalRooms>4</totalRooms><lastSoldDate>04/22/2011</lastSoldDate><lastSoldPrice currency="USD">99000</lastSoldPrice><zestimate><amount currency="USD">255607</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">2891</valueChange><valuationRange><low currency="USD">219822</low><high currency="USD">278612</high></valuationRange><percentile>14</percentile></zestimate><localRealEstate><region name="Eastmont" id="268129" type="neighborhood"><zindexValue>289,400</zindexValue><links><overview>http://www.zillow.com/local-info/CA-Oakland/Eastmont/r_268129/</overview><forSaleByOwner>http://www.zillow.com/eastmont-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/eastmont-oakland-ca/</forSale></links></region></localRealEstate></principal><comparables><comp score="12.0"><zpid>24796631</zpid><links><homedetails>http://www.zillow.com/homedetails/1245-80th-Ave-Oakland-CA-94621/24796631_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/1245-80th-Ave-Oakland-CA-94621/24796631_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24796631_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24796631_zpid/</comparables></links><address><street>1245 80th Ave</street><zipcode>94621</zipcode><city>Oakland</city><state>CA</state><latitude>37.755334</latitude><longitude>-122.184366</longitude></address><taxAssessmentYear>2015</taxAssessmentYear><taxAssessment>107400.0</taxAssessment><yearBuilt>1927</yearBuilt><lotSizeSqFt>6000</lotSizeSqFt><finishedSqFt>912</finishedSqFt><bathrooms>1.0</bathrooms><bedrooms>2</bedrooms><totalRooms>4</totalRooms><lastSoldDate>12/17/2015</lastSoldDate><lastSoldPrice currency="USD">150000</lastSoldPrice><zestimate><amount currency="USD">272353</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">6094</valueChange><valuationRange><low currency="USD">245118</low><high currency="USD">296865</high></valuationRange><percentile>71</percentile></zestimate><localRealEstate><region name="Fitchburg" id="268158" type="neighborhood"><links><overview>http://www.zillow.com/local-info/CA-Oakland/Fitchburg/r_268158/</overview><forSaleByOwner>http://www.zillow.com/fitchburg-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/fitchburg-oakland-ca/</forSale></links></region></localRealEstate></comp><comp score="11.0"><zpid>24796634</zpid><links><homedetails>http://www.zillow.com/homedetails/1231-80th-Ave-Oakland-CA-94621/24796634_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/1231-80th-Ave-Oakland-CA-94621/24796634_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24796634_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24796634_zpid/</comparables></links><address><street>1231 80th Ave</street><zipcode>94621</zipcode><city>Oakland</city><state>CA</state><latitude>37.755148</latitude><longitude>-122.184656</longitude></address><taxAssessmentYear>2015</taxAssessmentYear><taxAssessment>57008.0</taxAssessment><yearBuilt>1907</yearBuilt><lotSizeSqFt>5998</lotSizeSqFt><finishedSqFt>660</finishedSqFt><bathrooms>1.0</bathrooms><bedrooms>1</bedrooms><totalRooms>4</totalRooms><lastSoldDate>11/12/2015</lastSoldDate><lastSoldPrice currency="USD">185000</lastSoldPrice><zestimate><amount currency="USD">204629</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">-3888</valueChange><valuationRange><low currency="USD">178027</low><high currency="USD">223046</high></valuationRange><percentile>21</percentile></zestimate><localRealEstate><region name="Fitchburg" id="268158" type="neighborhood"><links><overview>http://www.zillow.com/local-info/CA-Oakland/Fitchburg/r_268158/</overview><forSaleByOwner>http://www.zillow.com/fitchburg-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/fitchburg-oakland-ca/</forSale></links></region></localRealEstate></comp></comparables></properties></response></Comps:comps><!-- H:001  T:49ms  S:3037  R:Sun Mar 13 17:36:09 PDT 2016  B:4.0.25909-master.a723596~hotfix_pre.53ac87d -->
"""
