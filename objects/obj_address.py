import string

class AddressObj(object):
    
    hot_words = ["reo", "vacant", "foreclosure", "short sale", "fixer upper", "distressed property", "distressed owner", "probate sale", "divorce", "as is", "motivated seller", "handyman special", "investor special", "tlc", "needs work", "potential", "price reduction", "reduced price", "transaction fell through", "build the home of your dreams", "BOM", "Damaged", "Teardown", "Fire damage", "Water damage", "Redevelopment opportunity", "Needs remodeling", "Needs updating", "Needs renovation", "Contractor special", "Land value", "Dilapidated", "Add on", "Build new"]

    def __init__(self, address, city, state, zip, redfin_link, dom, listing_id, description, price):
        self.address = address.replace("(Unable to map)", "")
        self.city = city
        self.state = state
        self.zip = zip
        self.citystatezip = city + ", " + state + " " + zip
        self.price = price

        self.redfin_link = redfin_link
        self.dom = dom
        self.listing_id = listing_id

        exclude = set(string.punctuation)
        description = ''

        clean_description = description.strip().lower()

        self.num_hot_words = 0
        for hot_word in self.hot_words:
            hot_word_clean = hot_word.strip().lower()
            if hot_word_clean in clean_description:
                self.num_hot_words += 1
