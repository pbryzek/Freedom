from simple_salesforce import Salesforce
from objects.obj_home import HomeObj

from common.globals import handle_err_msg

class SFBridge(object):

    _instance = None

    instance_domain = "na30.salesforce.com"
    username = "tony@refreedomgroup.com"
    password = "Januszbarbara$5"
    token = "6PSeOTpzWUtwScqCLT4vR3I2"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SFBridge, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.sf = Salesforce(username=self.username, password=self.password, security_token=self.token)

    def handle_sf_response(self, response):
        #[(u'id', u'a0036000002aU8lAAE'), (u'success', True), (u'errors', [])]
        was_success = response["success"]
        
        if was_success:
            handle_err_msg("Response was a success")
            return_id = response["id"]
            return return_id
        else:
            errs = response["errors"]
            handle_err_msg("Response had errors!" + str(errs))
            return None

    def create_comp_in_sf(self, comp, listing_id):
        home = comp.home
        params = self.create_home_params(home)

        params["Listing__c"] = listing_id
        params["Sold_Date__c"] = comp.solddate_sf
        params["Sold_Price__c"] = comp.soldprice
        params["Comp_Score__c"] = comp.comp_score
        params["Distance__c"] = comp.distance
        params["PPSqFt__c"] = comp.sqftprice
   
        comp_response = self.sf.Comp__c.create(params)
        comp_ret = self.handle_sf_response(comp_response)
        return comp_ret

    def create_listing_in_sf(self, home, mao_high, mao_med, mao_light, principal_arv, rehab_high, rehab_med, rehab_light, avg_sqfootage):
        params = self.create_home_params(home)

        params["AVG_Sq_Ft__c"] = avg_sqfootage
        params["MAO_High__c"] = mao_high
        params["MAO_Light__c"] = mao_light
        params["MAO_Medium__c"] = mao_med
        params["Principal_ARV__c"] = principal_arv
        params["Rehab_High__c"] = rehab_high
        params["Rehab_Light__c"] = rehab_light
        params["Rehab_Medium__c"] = rehab_med
        params["Listing_Source__c"] = home.type
        params["Hot_Words__c"] = home.num_hot_words
        params["Rent_Estimate__c"] = home.rentestimate

        listing_response = self.sf.Listing__c.create(params)
        listing_ret = self.handle_sf_response(listing_response)
        return listing_ret

    def create_home_params(self, home): 
        params = {
            "Baths__c" : home.baths,
            "Beds__c" : home.beds,
            "City__c" : home.city,
            "Comps_Link__c" : home.compslink,
            "DOM__c" : home.dom,
            "Graph_Link__c" : home.graphlink, 
            "Home_Link__c" : home.homelink, 
            "Latitude__c" : home.latitude, 
            "Longitude__c" : home.longitude,
            "Lot_Size__c" : home.lotsize,
            "Map_Link__c" : home.maplink,
            "Redfin_Link__c" : home.redfin_link, 
            "Sq_Ft__c" : home.sqfootage,
            "State__c" : home.state,
            "Street_Name__c" : home.address_st,
            "Street_Number__c" : home.address_num, 
            "Year_Built__c" : home.yearbuilt, 
            "ZEstimate__c" : home.zestimate,
            "Zip_Code__c" : home.zip, 
            "ZPID__c" : home.zpid
          }
        return params
