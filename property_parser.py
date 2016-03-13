from api_engine import APIEngine
from objects.obj_address import AddressObj
import consts.paths as paths

class PropertyParser(object):
    properties_csv = paths.INPUTS_PATH + paths.PROPERTIES_CSV

    address_index = 2
    city_index = 3
    state_index = 4
    zip_index = 5

    def __init__(self):
        self.addresses = []

    def parse(self):
        with open(self.properties_csv, "r") as csvfile:
            lines = csvfile.readlines()
            first = True
            for line in lines:
                if first:
                    first = False
                    continue

                cols = line.split(",") 
                address = cols[self.address_index]
                city = cols[self.city_index]
                state = cols[self.state_index]
                zip = cols[self.zip_index]
    
                address_obj = AddressObj(address, city, state, zip)
                self.addresses.append(address_obj)

    def make_requests(self):
        for address_obj in addresses:
            address = address_obj.address
            citystatezip = address_obj.citystatezip

            api_engine = APIEngine(address, citystatezip)
            api_engine.make_requests()

    def print_properties(self):
        for address_obj in self.addresses:
            print address_obj.address
            print address_obj.citystatezip
            print ""

