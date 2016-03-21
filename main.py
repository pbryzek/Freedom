from property_parser import PropertyParser
import consts.switches as switches

def main():
    if switches.REDFIN_ENABLED:
        prop_parser = PropertyParser(switches.PROPERTY_TYPE_REDFIN)
        prop_parser.parse()
        prop_parser.make_requests()

if __name__ == "__main__":
    main()

