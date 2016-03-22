import consts.switches as switches
import webbrowser

#Class responsible for downloading the inputs
class PropertyDownloader(object):

    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    def __init__(self, type):
        self.type = type

        if type == switches.PROPERTY_TYPE_REDFIN:
            self.url = "https://www.redfin.com/city/13654/CA/Oakland"

    def open_chrome(self):
        webbrowser.get(self.chrome_path).open(self.url)        

