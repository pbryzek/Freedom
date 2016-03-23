from property_parser import PropertyParser
from property_downloader import PropertyDownloader
import consts.switches as switches

from common.globals import handle_err_msg

def execute_property(type):
    pro_downloader = PropertyDownloader(type)
    ret_val = pro_downloader.open_chrome()

    if not ret_val:
        handle_err_msg("Property Downloader did not return True, Quitting!")
        return        

    #prop_parser = PropertyParser(type)
    #prop_parser.parse()
    #prop_parser.make_requests()

def execute_redfin():
    execute_property(switches.PROPERTY_TYPE_REDFIN)

def main():
    if switches.REDFIN_ENABLED:
        execute_redfin()

if __name__ == "__main__":
    main()

