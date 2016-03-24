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

    def create_listing_in_sf(self, home, mao_high, mao_med, mao_light, principal_arv, rehab_high, rehab_med, rehab_light):
        st_name = home.address_st
        st_num = home.address_num
        params = {
            "AVG_Sq_Ft__c" : home.sqfootage,
            "Baths__c" : home.baths,
            "Beds__c" : home.beds,
            "City__c" : home.city,
            "Comps_Link__c" : home.compslink,
            "DOM__c" : home.dom,
            "Graph_Link__c" : home.graphlink, 
            "Home_Link__c" : home.homelink, 
            "Hot_Words__c" : home.num_hot_words, 
            "Latitude__c" : home.latitude, 
            "Listing_Source__c" : home.type,
            "Longitude__c" : home.longitude,
            "Lot_Size__c" : home.lotsize,
            "MAO_High__c" : mao_high,
            "MAO_Light__c" : mao_light,
            "MAO_Medium__c" : mao_med,
            "Map_Link__c" : home.maplink,
            "Principal_ARV__c" : principal_arv,
            "Redfin_Link__c" : home.redfin_link, 
            "Rehab_High__c" : rehab_high,
            "Rehab_Light__c" : rehab_light,
            "Rehab_Medium__c" : rehab_med,
            "Rent_Estimate__c" : home.rentestimate,
            "Sq_Ft__c" : home.sqfootage,
            "State__c" : home.state,
            "Street_Name__c" : home.address_st,
            "Street_Number__c" : home.address_num, 
            "Year_Built__c" : home.yearbuilt, 
            "ZEstimate__c" : home.zestimate,
            "Zip_Code__c" : home.zip, 
            "ZPID__c" : home.zpid
          }

        listing_response = self.sf.Listing__c.create(params)

