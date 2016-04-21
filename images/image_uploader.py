import os
import sys

#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

os.chdir(scriptPath)

#append the relative location you want to import from
sys.path.append("..")

from sf_bridge import SFBridge
from google_map_downloader import GoogleMapDownloader

#This is the SF ID which represent the property we will generate buyer's marketing materials
PROPERTY_ID = "a0036000002cZyY"

SAVE_PATH = "./results/"

class ImageUploader(object):
  
    def __init__(self, latitude, longitude, address, zoom_factor=12):
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.zoom_factor = zoom_factor      
    
        self.gmd = GoogleMapDownloader(latitude, longitude, zoom_factor) 
  
    def create_google_map_image(self, zoom_factor=12):
        #If the zoom factor has changed, re-create the gmd
        if self.zoom_factor != zoom_factor:
            self.gmd = GoogleMapDownloader(self.latitude, self.longitude, self.zoom_factor) 
        try:
            # Get the high resolution image
            img = self.gmd.generateImage()
        except IOError:
            print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
        else:
            #Save the image to disk
            file_path = SAVE_PATH + self.address + ".png" 
            img.save(file_path)
            print("The map has successfully been created")

def main():
    sf_bridge = SFBridge()
    listing_obj = sf_bridge.get_listing_by_id(PROPERTY_ID)
    latitude = listing_obj["Latitude__c"]
    longitude = listing_obj["Longitude__c"]
    st_num = listing_obj["Street_Number__c"]
    st = listing_obj["Street_Name__c"]
    city = listing_obj["City__c"]
    state = listing_obj["State__c"]
    address = st_num + "_" + st + "_" + city + "_" + state 
    zoom_factor = 13

    image_uploader = ImageUploader(latitude, longitude, address, zoom_factor)
    image_uploader.create_google_map_image()
    

if __name__ == '__main__':
    main()

