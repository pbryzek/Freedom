class AddressObj(object):
    def __init__(self, address, city, state, zip, redfin_link):
        self.address = address.replace("(Unable to map)", "")
        self.citystatezip = city + ", " + state + " " + zip
        self.redfin_link = redfin_link
