class AddressObj(object):
    def __init__(self, address, city, state, zip):
        self.address = address.replace("(Unable to map)", "")
        self.citystatezip = city + ", " + state + " " + zip
