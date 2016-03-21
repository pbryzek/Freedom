from base_home_api import BaseHomeAPI

import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj


# create the client
class APIGetCompsRequest(BaseHomeAPI):

    def __init__(self, type, zpid, count, dom):
        #Specific endpoint
        path = paths.GET_COMPS

        #Params to send with request
        params = {"zpid": zpid, "count": count}

        super(APIGetCompsRequest, self).__init__(type, path, params)

    def request(self):
        response = super(APIGetCompsRequest, self).request()

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
<?xml version="1.0" encoding="utf-8"?><Comps:comps xsi:schemaLocation="http://www.zillow.com/static/xsd/Comps.xsd http://www.zillowstatic.com/vstatic/9041678/static/xsd/Comps.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:Comps="http://www.zillow.com/static/xsd/Comps.xsd"><request><zpid>24792995</zpid><count>2</count></request><message><text>Request successfully processed</text><code>0</code></message><response><properties><principal><zpid>24792995</zpid><links><homedetails>http://www.zillow.com/homedetails/2629-75th-Ave-Oakland-CA-94605/24792995_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/2629-75th-Ave-Oakland-CA-94605/24792995_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24792995_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24792995_zpid/</comparables></links><address><street>2629 75th Ave</street><zipcode>94605</zipcode><city>Oakland</city><state>CA</state><latitude>37.766287</latitude><longitude>-122.174004</longitude></address><zestimate><amount currency="USD">255607</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">2891</valueChange><valuationRange><low currency="USD">219822</low><high currency="USD">278612</high></valuationRange><percentile>14</percentile></zestimate><localRealEstate><region name="Eastmont" id="268129" type="neighborhood"><zindexValue>289,400</zindexValue><links><overview>http://www.zillow.com/local-info/CA-Oakland/Eastmont/r_268129/</overview><forSaleByOwner>http://www.zillow.com/eastmont-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/eastmont-oakland-ca/</forSale></links></region></localRealEstate></principal><comparables><comp score="12.0"><zpid>24796631</zpid><links><homedetails>http://www.zillow.com/homedetails/1245-80th-Ave-Oakland-CA-94621/24796631_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/1245-80th-Ave-Oakland-CA-94621/24796631_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24796631_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24796631_zpid/</comparables></links><address><street>1245 80th Ave</street><zipcode>94621</zipcode><city>Oakland</city><state>CA</state><latitude>37.755334</latitude><longitude>-122.184366</longitude></address><zestimate><amount currency="USD">272353</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">6094</valueChange><valuationRange><low currency="USD">245118</low><high currency="USD">296865</high></valuationRange><percentile>71</percentile></zestimate><localRealEstate><region name="Fitchburg" id="268158" type="neighborhood"><links><overview>http://www.zillow.com/local-info/CA-Oakland/Fitchburg/r_268158/</overview><forSaleByOwner>http://www.zillow.com/fitchburg-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/fitchburg-oakland-ca/</forSale></links></region></localRealEstate></comp><comp score="11.0"><zpid>24796634</zpid><links><homedetails>http://www.zillow.com/homedetails/1231-80th-Ave-Oakland-CA-94621/24796634_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/1231-80th-Ave-Oakland-CA-94621/24796634_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/24796634_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/24796634_zpid/</comparables></links><address><street>1231 80th Ave</street><zipcode>94621</zipcode><city>Oakland</city><state>CA</state><latitude>37.755148</latitude><longitude>-122.184656</longitude></address><zestimate><amount currency="USD">204629</amount><last-updated>03/12/2016</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">-3888</valueChange><valuationRange><low currency="USD">178027</low><high currency="USD">223046</high></valuationRange><percentile>21</percentile></zestimate><localRealEstate><region name="Fitchburg" id="268158" type="neighborhood"><links><overview>http://www.zillow.com/local-info/CA-Oakland/Fitchburg/r_268158/</overview><forSaleByOwner>http://www.zillow.com/fitchburg-oakland-ca/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/fitchburg-oakland-ca/</forSale></links></region></localRealEstate></comp></comparables></properties></response></Comps:comps><!-- H:004  T:19ms  S:2158  R:Sun Mar 13 17:06:52 PDT 2016  B:4.0.25909-master.a723596~hotfix_pre.53ac87d -->
"""
