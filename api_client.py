import requests
import consts.paths as paths

class APIClient(object):
    """Creates an API client object
    """

    def __init__(self, path, params, method="GET"):
        #Zillow specific key
        self.zws_id = "X1-ZWz19tezrsrabv_5qhl2"

        #Specific endpoint
        self.path = path

        #Base URL
        self.base_url = paths.BASE_URL

        #The params to send along with the request.
        self.params = params

        #GET or POST
        self.method = method

    def request(self):
        """Makes a request to the API with the given parameters
        """
        
        # add the authentication parameters (sent with every request)
        self.params["zws-id"] = self.zws_id

        full_url = self.base_url + self.path

        print full_url
        print self.params

        # send a request to the api server
        result = requests.request(
            method = self.method,
            url = full_url,
            params = self.params
        )

        return result
