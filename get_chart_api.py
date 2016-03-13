from base_api import BaseAPI
import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET

# create the client
class APIGetChartRequest(BaseAPI):

    def __init__(self, zpid):
        self.chart_url = ""

        #Specific endpoint
        path = paths.GET_CHART

        #The format of the chart
        type = "dollar"
        #type = "percent"

        #Params to send with request
        params = {"zpid":zpid, "unit-type": type}

        super(APIGetChartRequest, self).__init__(path, params)

    def parse_response(self, node):
        for child in node:
            tag = child.tag
            if tag == tags.TAG_URL:
                self.chart_url = child.text

    def request(self):
        response = super(APIGetChartRequest, self).request()

        root = ET.fromstring(response.content)
        for child in root:
            tag = child.tag
            if tag == tags.TAG_MESSAGE:
                super(APIGetChartRequest, self).parse_error_msg(child)
            elif tag == tags.TAG_RESPONSE:
                self.parse_response(child)

        return self.chart_url

"""
<?xml version="1.0" encoding="utf-8"?><Chart:chart xsi:schemaLocation="http://www.zillow.com/static/xsd/Chart.xsd http://www.zillowstatic.com/vstatic/9041678/static/xsd/Chart.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:Chart="http://www.zillow.com/static/xsd/Chart.xsd"><request><zpid>24819940</zpid><unit-type>dollar</unit-type></request><message><text>Request successfully processed</text><code>0</code></message><response><url>http://www.zillow.com/app?chartDuration=1year&amp;chartType=partner&amp;page=webservice%2FGetChart&amp;service=chart&amp;zpid=24819940</url><graphsanddata>http://www.zillow.com/homedetails/333-Pali-Ct-Oakland-CA-94611/24819940_zpid/#charts-and-data</graphsanddata></response></Chart:chart><!-- H:001  T:3ms  S:201  R:Sat Mar 12 15:51:23 PST 2016  B:4.0.25909-master.a723596~hotfix_pre.53ac87d -->
"""
