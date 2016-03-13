from base_home_api import BaseHomeAPI

import consts.paths as paths
import consts.xml_tags as tags
import xml.etree.ElementTree as ET
from objects.obj_home import HomeObj


# create the client
class APIGetDeepCompsRequest(BaseHomeAPI):

    def __init__(self, zpid, count):
        #Specific endpoint
        path = paths.GET_DEEP_COMPS

        #Params to send with request
        params = {"zpid": zpid, "count": count}

        super(APIGetDeepCompsRequest, self).__init__(path, params)

    #Implementing abstract method but not needed here
    def parse_address(self, node):
        pass

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

