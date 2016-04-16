from simple_salesforce import Salesforce
from objects.obj_home import HomeObj

from common.globals import handle_err_msg

import sys

class SFBridge(object):

    _instance = None

    instance_domain = "na30.salesforce.com"
    username = "tony@lightningproperties.com"
    password = "Januszbarbara$5"
    token = "6PSeOTpzWUtwScqCLT4vR3I2"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SFBridge, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.sf = Salesforce(username=self.username, password=self.password, security_token=self.token)

    def get_comps_by_listing_name(self, listing_name):
        comp_objs = self.sf.Comp__c.get_by_custom_id("Listing__c", listing_name)
        for comp_obj in comp_objs:
            print comp_obj


    def get_listing_by_id(self, listing_id):
        listing_obj = self.sf.Listing__c.get(listing_id)
        return listing_obj

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

    def save_email_to_sf(self, email_html, listing_id):
        params = {}
        params["Buyers_Marketing_Email__c"] = email_html

    def normalize_data(self, data):
        if isinstance(data, basestring):
            normalized = data.strip().lower()
            return normalized
        return data

    def create_comp_in_sf(self, comp, listing_id):
        home = comp.home
        params = self.create_home_params(home)

        params["Listing__c"] = listing_id
        params["Sold_Date__c"] = comp.solddate_sf
        params["Sold_Price__c"] = self.normalize_data(comp.soldprice)
        params["Comp_Score__c"] = self.normalize_data(comp.comp_score)
        params["Distance__c"] = self.normalize_data(comp.distance)
        params["PPSqFt__c"] = self.normalize_data(comp.sqftprice)
   
        comp_response = self.sf.Comp__c.create(params)
        comp_ret = self.handle_sf_response(comp_response)
        return comp_ret

    def create_listing_in_sf(self, home, mao_high, mao_med, mao_light, principal_arv, rehab_high, rehab_med, rehab_light, avg_sqfootage):
        params = self.create_home_params(home)

        tier_sf = ""
        if home.tier == 1:
            tier_sf = "Tier_1"
        else:
            tier_sf = "Tier_2"

        #params["RecordType"] = tier_sf
        params["AVG_Sq_Ft__c"] = self.normalize_data(avg_sqfootage)
        params["MAO_High__c"] = self.normalize_data(mao_high)
        params["MAO_Light__c"] = self.normalize_data(mao_light)
        params["MAO_Medium__c"] = self.normalize_data(mao_med)
        params["Principal_ARV__c"] = self.normalize_data(principal_arv)
        params["Rehab_High__c"] = self.normalize_data(rehab_high)
        params["Rehab_Light__c"] = self.normalize_data(rehab_light)
        params["Rehab_Medium__c"] = self.normalize_data(rehab_med)
        params["Listing_Source__c"] = self.normalize_data(home.type)
        params["Hot_Words__c"] = self.normalize_data(home.num_hot_words)
        params["Rent_Estimate__c"] = self.normalize_data(home.rentestimate)
        params["MLS__c"] = self.normalize_data(home.listing_id)

        try:
            listing_response = self.sf.Listing__c.create(params)
        except:
            duplicate_str = "duplicate value found: Unique_Identifier__c duplicates value on record with id: "
            err_msg = str(sys.exc_info()[1])
            if duplicate_str in err_msg:
                len_dup_str = len(duplicate_str)
                dup_index = err_msg.index(duplicate_str) + len_dup_str
                dup_end_index = err_msg.index("'", dup_index)
                listing_id = err_msg[dup_index:dup_end_index]
 
                listing_response = self.sf.Listing__c.update(listing_id, params)
                return listing_id 
            else:
                handle_err_msg("Got unexpected error from SalesForce, returning None! " + err_msg)
                return None    

        listing_ret = self.handle_sf_response(listing_response)
        return listing_ret

    def create_home_params(self, home): 
        city = self.normalize_data(home.city).title()
        address = self.normalize_data(home.address_st).title()
        state = self.normalize_data(home.state).upper()

        params = {
            "Baths__c" : self.normalize_data(home.baths),
            "Beds__c" : self.normalize_data(home.beds),
            "City__c" : city,
            "Comps_Link__c" : self.normalize_data(home.compslink),
            "DOM__c" : self.normalize_data(home.dom),
            "Graph_Link__c" : self.normalize_data(home.graphlink), 
            "Home_Link__c" : self.normalize_data(home.homelink), 
            "Latitude__c" : self.normalize_data(home.latitude), 
            "Longitude__c" : self.normalize_data(home.longitude),
            "Lot_Size__c" : self.normalize_data(home.lotsize),
            "Map_Link__c" : self.normalize_data(home.maplink),
            "Redfin_Link__c" : self.normalize_data(home.redfin_link), 
            "Sq_Ft__c" : self.normalize_data(home.sqfootage),
            "State__c" : state,
            "Street_Name__c" : address,
            "Street_Number__c" : self.normalize_data(home.address_num), 
            "Year_Built__c" : self.normalize_data(home.yearbuilt), 
            "ZEstimate__c" : self.normalize_data(home.zestimate),
            "Zip_Code__c" : self.normalize_data(home.zip), 
            "ZPID__c" : self.normalize_data(home.zpid)
          }
        return params
