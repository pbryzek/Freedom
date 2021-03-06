from property_parser import PropertyParser
from property_downloader import PropertyDownloader
import consts.switches as switches

from common.globals import handle_err_msg

def execute_property(type):

    if switches.DOWNLOAD_ENABLED:
        prop_downloader = PropertyDownloader(type)
        ret_val = prop_downloader.download_redfin_input()

        if not ret_val:
            handle_err_msg("Property Downloader did not return True, Quitting!")
            return        
 
    if switches.PARSER_ENABLED:
        prop_parser = PropertyParser(type)
        prop_parser.parse()
        prop_parser.make_requests()

def execute_redfin():
    execute_property(switches.PROPERTY_TYPE_REDFIN)

def main():
    if switches.REDFIN_ENABLED:
        execute_redfin()

if __name__ == "__main__":
    main()

