from property_parser import PropertyParser

def main():
    prop_parser = PropertyParser()
    prop_parser.parse()
    #prop_parser.print_properties()
    prop_parser.make_requests()

if __name__ == "__main__":
    main()

