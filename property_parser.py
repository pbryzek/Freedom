from api_engine import APIEngine
from objects.obj_address import AddressObj
import consts.paths as paths
import consts.switches as switches
import time

from common.globals import handle_err_msg

class PropertyParser(object):

    address_index = -1
    city_index = -1
    state_index = -1
    zip_index = -1
    price_index = -1
    dom_index = -1
    redfin_link_index = -1
    listing_id_index = -1
    shortsale_index = -1

    def __init__(self, type):
        self.addresses = []
        self.type = type
        if type == switches.PROPERTY_TYPE_REDFIN:
            self.properties_csv = paths.INPUTS_PATH + paths.REDFIN_PROPERTIES_CSV
            self.address_index = 2
            self.city_index = 3
            self.state_index = 4
            self.zip_index = 5
            self.price_index = 6
            self.dom_index = 15
            self.redfin_link_index = 24
            self.listing_id_index = 26
            self.shortsale_index = 32

    def parse(self):
        with open(self.properties_csv, "r") as csvfile:
            lines = csvfile.readlines()
            first = True
            num_properties = len(lines) - 1
            
            handle_err_msg("Number of properties evaluating = " + str(num_properties))
            if switches.MAX_PROPERTIES_TO_EVALUATE != -1:
                handle_err_msg("Script only allowing the evaluation of " + str(switches.MAX_PROPERTIES_TO_EVALUATE) + " properties") 

            num_shortsales_skipped = 0
            price_skipped_props = 0
            low_price_skipped_props = 0
            num_dom_skipped = 0
            num_properties_analyzed = 0
            num_undisclosed = 0

            for line in lines:
                if first:
                    first = False
                    continue

                if switches.MAX_PROPERTIES_TO_EVALUATE != -1 and num_properties_analyzed == switches.MAX_PROPERTIES_TO_EVALUATE:
                    break

                cols = line.split(",") 

                if (not cols) or (cols == "\n") or (len(cols) == 1 and (cols[0] == '\n') ):
                    continue

                price = int(cols[self.price_index])
         
                is_shortsale_str = cols[self.shortsale_index].lower().strip()
                dom_str = cols[self.dom_index].strip()

                ###
                #Do initial filter of the properties
                ###
                if dom_str != '':
                    dom_int = int(dom_str)
                    if dom_int < switches.MIN_DOM:  
                        num_dom_skipped += 1
                        continue
                    if switches.MAX_DOM != -1 and dom_int > switches.MAX_DOM:
                        num_dom_skipped += 1
                        continue
  
                if (not switches.SHORTSALE_SUPPORTED) and (is_shortsale_str == "true"):
                    num_shortsales_skipped += 1
                    continue

                if price < switches.MIN_PRICE:
                    low_price_skipped_props += 1
                    continue

                address = cols[self.address_index]
                if "Undisclosed" in address:
                    num_undisclosed += 1
                    continue    

                city = cols[self.city_index]
                state = cols[self.state_index]
                zip = cols[self.zip_index]

                redfin_link = cols[self.redfin_link_index]
                listing_id = cols[self.listing_id_index]
                listing_id = listing_id.replace("-", "")

                description = "Cheap Home that sells FAST! Handy man special!"

                address_obj = AddressObj(address, city, state, zip, redfin_link, dom_str, listing_id, description, price)
                self.addresses.append(address_obj)
 
                num_properties_analyzed += 1

        total_props = num_properties - price_skipped_props - low_price_skipped_props - num_shortsales_skipped - num_dom_skipped

        handle_err_msg("Number of properties skipped due to address Undisclosed = " + str(num_undisclosed)) 
        handle_err_msg("Number of properties skipped due to shortsale = " + str(num_shortsales_skipped))
        handle_err_msg("Number of properties skipped due to price too high = " + str(price_skipped_props))
        handle_err_msg("Number of properties skipped due to price too low = " + str(low_price_skipped_props))
        handle_err_msg("Number of properties skipped due to DOM too low = " + str(num_dom_skipped))
        handle_err_msg("Total Number of properties evaluated = " + str(num_properties_analyzed))
        handle_err_msg("")

    def make_requests(self):
        ts = int(time.time())
        for address_obj in self.addresses:
            address = address_obj.address
            city = address_obj.city
            state = address_obj.state
            zip = address_obj.zip
            
            redfin_link = address_obj.redfin_link
            dom = address_obj.dom
            listing_id = address_obj.listing_id
            price = address_obj.price
            num_hot_words = address_obj.num_hot_words

            api_engine = APIEngine(address, city, state, zip, redfin_link, dom, listing_id, self.type, ts, num_hot_words, price)
            api_engine.make_requests()

    def print_properties(self):
        for address_obj in self.addresses:
            handle_err_msg(address_obj.address)
            handle_err_msg(address_obj.citystatezip)
            handle_err_msg("")

