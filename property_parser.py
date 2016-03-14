from api_engine import APIEngine
from objects.obj_address import AddressObj
import consts.paths as paths
import consts.switches as switches

class PropertyParser(object):
    properties_csv = paths.INPUTS_PATH + paths.PROPERTIES_CSV

    address_index = 2
    city_index = 3
    state_index = 4
    zip_index = 5
    price_index = 6
    dom_index = 15
    redfin_link_index = 24
    shortsale_index = 32

    def __init__(self):
        self.addresses = []

    def parse(self):
        with open(self.properties_csv, "r") as csvfile:
            lines = csvfile.readlines()
            first = True
            num_properties = len(lines) - 1
            print "Number of properties evaluating = " + str(num_properties)
            if switches.MAX_PROPERTIES_TO_EVALUATE != -1:
                print "Script only allowing the evaluation of " + str(switches.MAX_PROPERTIES_TO_EVALUATE) + " properties"           

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
                price = int(cols[self.price_index])
         
                is_shortsale_str = cols[self.shortsale_index].lower().strip()
                dom_str = cols[self.dom_index].strip()

                ###
                #Do initial filter of the properties
                ###
                if dom_str != '' and (int(dom_str) < switches.MIN_DOM):
                    num_dom_skipped += 1
                    continue
  
                if (not switches.SHORTSALE_SUPPORTED) and (is_shortsale_str == "true"):
                    num_shortsales_skipped += 1
                    continue

                if price > switches.MAX_PRICE:
                    price_skipped_props += 1
                    continue
                elif price < switches.MIN_PRICE:
                    low_price_skipped_props += 1
                    continue

                address = cols[self.address_index]
                if "Undisclosed" in address:
                    num_undisclosed += 1
                    continue    

                city = cols[self.city_index]
                state = cols[self.state_index]
                zip = cols[self.zip_index]

                dom = cols[self.dom_index]
                redfin_link = cols[self.redfin_link_index]

                address_obj = AddressObj(address, city, state, zip, redfin_link)
                self.addresses.append(address_obj)
 
                num_properties_analyzed += 1

        total_props = num_properties - price_skipped_props - low_price_skipped_props - num_shortsales_skipped - num_dom_skipped

        print "Number of properties skipped due to address Undisclosed = " + str(num_undisclosed) 
        print "Number of properties skipped due to shortsale = " + str(num_shortsales_skipped)
        print "Number of properties skipped due to price too high = " + str(price_skipped_props)
        print "Number of properties skipped due to price too low = " + str(low_price_skipped_props)
        print "Number of properties skipped due to DOM too low = " + str(num_dom_skipped)
        print "Total Number of properties evaluated = " + str(num_properties_analyzed)
        print ""

    def make_requests(self):
        for address_obj in self.addresses:
            address = address_obj.address
            citystatezip = address_obj.citystatezip
            redfin_link = address_obj.redfin_link

            api_engine = APIEngine(address, citystatezip, redfin_link)
            api_engine.make_requests()

    def print_properties(self):
        for address_obj in self.addresses:
            print address_obj.address
            print address_obj.citystatezip
            print ""

