import string

class AddressObj(object):
    
    hot_words = ["cheap", "handy man", "fast"]

    def __init__(self, address, city, state, zip, redfin_link, dom, listing_id, description):
        self.address = address.replace("(Unable to map)", "")
        self.citystatezip = city + ", " + state + " " + zip
        self.redfin_link = redfin_link
        self.dom = dom
        self.listing_id = listing_id

        exclude = set(string.punctuation)
        description = ''.join(ch for ch in description if ch not in exclude)

        clean_description = description.strip().lower()

        self.num_hot_words = 0
        for hot_word in self.hot_words:
            if hot_word in clean_description:
                self.num_hot_words += 1
