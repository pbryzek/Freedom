import consts.switches as switches
import webbrowser
import os
import consts.paths as paths

from os import walk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from common.globals import handle_err_msg

#Class responsible for downloading the inputs
class PropertyDownloader(object):

    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    def __init__(self, type):
        self.type = type

        #Create an instance of a Chrome browser
        self.webbrowser = webdriver.Chrome()

        if type == switches.PROPERTY_TYPE_REDFIN:
            self.url = "https://www.redfin.com/city/13654/CA/Oakland"

    def download_redfin_input(self):
        self.webbrowser.get(self.url)
        download_button = self.webbrowser.find_element_by_link_text("(Download All)")
        download_button.send_keys(Keys.RETURN)
        self.webbrowser.quit()

        #The Redfin csv downloaded here
        files = []
        for (dirpath, dirnames, filenames) in walk(paths.REDFIN_INPUT_PATH):
            files.extend(filenames)

        num_inputs = 0
        redfin_dl_file_name = ""

        for file in files:
            if paths.REDFIN_INPUT_PREFIX in file and file.index(paths.REDFIN_INPUT_PREFIX) == 0:
                num_inputs += 1
                redfin_dl_file_name = paths.REDFIN_INPUT_PATH + file

        if num_inputs > 1:
            handle_err_msg("Num Input files for Redfin > 1! Quitting!")
            return False    
        elif num_inputs != 1:
            handle_err_msg("Num Input files for Redfin != 1! Quitting!")
            return False

        #Now move that file into the inputs section, and delete it.
        redfin_input_file = paths.INPUTS_PATH + paths.REDFIN_PROPERTIES_CSV
        try:
            os.remove(redfin_input_file)
        except OSError:
            pass

        os.rename(redfin_dl_file_name, redfin_input_file)

        return True
