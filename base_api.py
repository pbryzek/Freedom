import consts.paths as paths
import consts.xml_tags as tags
from api_client import APIClient
from abc import ABCMeta, abstractmethod

# create the client
class BaseAPI(object):
    __metaclass__ = ABCMeta

    REQ_SUCCESS = "0"
    SERVICE_ERROR = "1"
    INVALID_ZWSID = "2"
    SERVICE_UNAVAILABLE = "3"
    API_UNAVAILABLE = "4"
 
    INVALID_ZPID = "500"
    INVALID_COUNT = "501"
    ZPID_NOT_FOUND = "502"
    ZESTIMATE_NOT_FOUND = "503"
    NO_RESULTS = "504"

    def __init__(self, path, params):
        #Specific endpoint
        self.path = path
       
        #Params to send with request
        self.params = params

    def translate_code(self, code):
        if code == self.REQ_SUCCESS:
            return "Success"
        elif code == self.SERVICE_ERROR:
            return "Service Error"
        elif code == self.INVALID_ZWSID:
            return "Invalid ZWSID"
        elif code == self.SERVICE_UNAVAILABLE:
            return "Service Unavailable"
        elif code == self.API_UNAVAILABLE:
            return "API Unavailable"
        elif code == self.NO_RESULTS:
            return "No Results"
        elif code == self.INVALID_ZPID:
            return "Zpid was not specified or invalid"
        elif code == self.INVALID_COUNT:
            return "Count param not specified or invalid"
        elif code == self.ZESTIMATE_NOT_FOUND:
            return "Property does not have a Zestimate"
        else:
            return ""

    def parse_error_msg(self, node):
        error_msg = ""
        error_code = ""
        for child in node:
            tag = child.tag
            if tag == tags.TAG_TEXT:
                error_msg = child.text
            elif tag == tags.TAG_CODE:
                error_code = child.text
            else:
                print "base_api parse_error_msg Unhandled tag " + tag

        if error_code != self.REQ_SUCCESS:
            error_description = self.translate_code(error_code)
            print_error_msg = error_code + " " + error_description + " " + error_msg
            print "Response from API ! " + print_error_msg

        return error_code

    def request(self):
        print "Fetching " + self.path

        api = APIClient(self.path, self.params, paths.GET_METHOD)
        result = api.request()

        print "Status code = " + str(result.status_code)

        if result.status_code != 200:
            print "Error hitting the API " + result.status_code
 
        return result
