import os
import sys

#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

os.chdir(scriptPath)

#append the relative location you want to import from
sys.path.append("..")

from sf_bridge import SFBridge
from google_map_downloader import GoogleMapDownloader

sf_bridge = SFBridge()
listing_obj = sf_bridge.get_listing_by_id(PROPERTY_ID)
latitude = listing_obj["Latitude__c"]
longitude = listing_obj["Longitude__c"]
zoom_factor = 13

class ImageUploader(object):
   
    def __init__(self, latitude, longitude, zoom_factor=12):
        self.latitude = latitude
        self.longitude = longitude
        self.zoom_factor = zoom_factor
    
        self.gmd = GoogleMapDownloader(latitude, longitude, zoom_factor) 
        print("The tile coorindates are {}".format(gmd.getXY()))
  
    def create_google_map_image(self, zoom_factor):
        #If the zoom factor has changed, re-create the gmd
        if self.zoom_factor != zoom_factor:
            self.gmd = GoogleMapDownloader(self.latitude, self.longitude, self.zoom_factor) 

        try:
            # Get the high resolution image
            img = gmd.generateImage()
        except IOError:
            print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
        else:
            #Save the image to disk
            img.save("high_resolution_image.png")
            print("The map has successfully been created")

def main():
    try:
        # Get the high resolution image
        img = gmd.generateImage()
    except IOError:
        print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
    else:
        #Save the image to disk
        img.save("high_resolution_image.png")
        print("The map has successfully been created")


if __name__ == '__main__':
    main()

