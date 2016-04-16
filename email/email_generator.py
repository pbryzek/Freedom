import os
import sys
import codecs

#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
print scriptPath

os.chdir(scriptPath)

#append the relative location you want to import from
sys.path.append("..")

from sf_bridge import SFBridge

ENABLE_SENDING_EMAIL = False
ENABLE_SAVE_EMAIL_HTML_SF = False

TEMPLATE_READ_NAME = "./email_marketing_template.html"
TEMPLATE_WRITE_NAME = "./email_marketing_"

HTML_EXTENSION = ".html"

#This is the SF ID which represent the property we will generate buyer's marketing materials
PROPERTY_ID = "a0036000002achv"

#These are the strings for search and replace functionality
ADDRESS_REPLACE_STR = "1516 W 2nd St, Santa Ana, CA 92703"
LIST_PRICE_STR = "List Price: "
LIST_PRICE_REPLACE_STR = LIST_PRICE_STR + "$320,000"
MLS_STR = "MLS: "
MLS_REPLACE_STR = MLS_STR + "Off Market"
BED_STR = "Bedrooms: " 
BED_REPLACE_STR = BED_STR + "2"
BATH_STR = "Bathrooms: "
BATH_REPLACE_STR = BATH_STR + "1"
SQFT_STR = "Living SQF: "
SQFT_REPLACE_STR = SQFT_STR + "1,040" 
LOT_STR = "Lot SQF: "
LOT_REPLACE_STR = LOT_STR + "6,100"
REPAIR_STR = "Repair Estimate: "
REPAIR_REPLACE_STR = REPAIR_STR + "$31,200"
YEAR_STR = "Year Built: "
YEAR_REPLACE_STR = YEAR_STR + "1908"
GARAGE_TYPE_STR = "Garage Type: "
GARAGE_TYPE_REPLACE_STR = GARAGE_TYPE_STR + "None"
GARAGE_CAPACITY_STR = "Garage Capacity: "
GARAGE_CAPACITY_REPLACE_STR = GARAGE_CAPACITY_STR + "N/A"
AVG_SOLD_SQF_PRICE_STR = "Average Sold SQF Price: "
AVG_SOLD_SQF_PRICE_REPLACE_STR = AVG_SOLD_SQF_PRICE_STR + "$107"
MED_SQF_LIVING_AREA_STR = "Median SQF Living Area: "
MED_SQF_LIVING_AREA_REPLACE_STR = MED_SQF_LIVING_AREA_STR + "1,022"
MED_BEDS_STR = "Median # Beds: "
MED_BEDS_REPLACE_STR = MED_BEDS_STR + "2"
MED_BATHS_STR = "Median # Baths: "
MED_BATHS_REPLACE_STR = MED_BATHS_STR + "1"
MED_VALUE_STR = "Median Value: "
MED_VALUE_REPLACE_STR = MED_VALUE_STR + "$435.000"
AVG_DOM_STR = "Average DOM: "
AVG_DOM_REPLACE_STR = AVG_DOM_STR + "24"
MED_YEAR_STR = "Median Year Built: "
MED_YEAR_REPLACE_STR = MED_YEAR_STR + "1946"

DESCRIPTION_REPLACE_STR = "TEXT TO FIND AND REPLACE"
MAP_1_REPLACE_STR = "https://images.benchmarkemail.com/client562548/image2993695.jpg"
MAP_2_REPLACE_STR = "https://images.benchmarkemail.com/client562548/image2993697.jpg"

COMP_REPLACE_STR = "COMP TEXT TO FIND AND REPLACE"

class EmailGenerator(object):

    def create_buyer_marketing_email(self):
        #Get the listing object
        sf_bridge = SFBridge()
        listing_obj = sf_bridge.get_listing_by_id(PROPERTY_ID)

        #Parse out the relevant info
        listing_obj["AVG_Sq_Ft__c"]
        listing_name = listing_obj["Name"].strip()
        st_num = listing_obj["Street_Number__c"].strip()
        st = listing_obj["Street_Name__c"].strip()
        state = listing_obj["State__c"].strip()
        latitude = listing_obj["Latitude__c"]
        longitude = listing_obj["Longitude__c"]
        city = listing_obj["City__c"].strip()
        zip = listing_obj["Zip_Code__c"].strip()
        mao_med = listing_obj["MAO_Medium__c"]
        mls_num = listing_obj["MLS__c"]
        num_beds = listing_obj["Beds__c"]
        num_baths = listing_obj["Baths__c"]
        num_sqft = listing_obj["Sq_Ft__c"]
        lotsize = listing_obj["Lot_Size__c"]
        yearbuilt = listing_obj["Year_Built__c"]

        avg_dom = listing_obj["AVG DOM__c"]
        actual_repair = listing_obj["Actual_Rehab_Estimate__c"]
        actual_list_price = listing_obj["Actual_Offer__c"]
        avg_sold_price = listing_obj["Median_Value__c"]
        med_sqf = listing_obj["Median_SQF__c"]
        med_beds = listing_obj["Median_of_Beds__c"]
        med_baths = listing_obj["Median_of_Baths__c"]
        med_value = listing_obj["Median_Value__c"]
        med_year = listing_obj["Median_Year_Built__c"]

        prop_description = listing_obj["Description__c"]
        if not prop_description:
            prop_description = ""

        map_link_1 = listing_obj["Image_Google_1__c"]
        if not map_link_1:
            map_link_1 = "http://d32ogoqmya1dw8.cloudfront.net/images/sp/library/google_earth/google_maps_hello_world.jpg"

        map_link_2 = listing_obj["Image_Google_2__c"] 
        if not map_link_2:
            map_link_2 = "http://mike.teczno.com/img/google-maps-track.png"

        image_main = listing_obj["Image_Main__c"]
        if not image_main:
            image_main = "http://d32ogoqmya1dw8.cloudfront.net/images/sp/library/google_earth/google_maps_hello_world.jpg"

        #TODO remove this
        image_main = "https://na30.salesforce.com/sfc/p/#36000000axip/a/36000000GnMe/AsgrchTybZyJfMWylYrs_6dKDdYFiW0m7dWvDv5Z0Io"

        image_1 = listing_obj["Image_1__c"]
        if not image_1:
            image_1 = "http://mike.teczno.com/img/google-maps-track.png"

        image_2 = listing_obj["Image_2__c"]
        if not image_2: 
            image_2 = "http://d32ogoqmya1dw8.cloudfront.net/images/sp/library/google_earth/google_maps_hello_world.jpg"

        listing_address = st_num + " " + st + ", " + city + ", " + state + " " + zip
        listing_address_filename = listing_address.replace(" ", "_")
        listing_address = listing_address.title()
       
        fh = codecs.open(TEMPLATE_READ_NAME, 'r')
        html_template = fh.read().decode("utf8") 
        html_template = html_template.replace(ADDRESS_REPLACE_STR, listing_address)

        new_list_str = LIST_PRICE_STR + str(actual_list_price) 
        html_template = html_template.replace(LIST_PRICE_REPLACE_STR, new_list_str)
        new_mls_str = MLS_STR + mls_num 
        html_template = html_template.replace(MLS_REPLACE_STR, new_mls_str)
        new_bed_str = BED_STR + str(num_beds)
        html_template = html_template.replace(BED_REPLACE_STR, new_bed_str)
        new_bath_str = BATH_STR + str(num_baths)
        html_template = html_template.replace(BATH_REPLACE_STR, new_bath_str)
        new_sqft_str = SQFT_STR + str(num_sqft)
        html_template = html_template.replace(SQFT_REPLACE_STR, new_sqft_str)
        new_lot_str = LOT_STR + str(lotsize)
        html_template = html_template.replace(LOT_REPLACE_STR, new_lot_str)
        new_repair_str = REPAIR_STR + str(actual_repair) 
        html_template = html_template.replace(REPAIR_REPLACE_STR, new_repair_str)
        new_year_str = YEAR_STR + str(yearbuilt)
        html_template = html_template.replace(YEAR_REPLACE_STR, new_year_str) 

        #TODO maybe later add in the garage specific info?
        html_template = html_template.replace(GARAGE_TYPE_REPLACE_STR, "")
        html_template = html_template.replace(GARAGE_CAPACITY_REPLACE_STR, "")

        new_avg_sqf_str = AVG_SOLD_SQF_PRICE_STR + str(avg_sold_price)
        html_template = html_template.replace(AVG_SOLD_SQF_PRICE_REPLACE_STR, new_avg_sqf_str)
        new_med_sqf = MED_SQF_LIVING_AREA_STR + str(med_sqf)
        html_template = html_template.replace(MED_SQF_LIVING_AREA_REPLACE_STR, new_med_sqf)
        new_med_beds = MED_BEDS_STR + str(med_beds)
        html_template = html_template.replace(MED_BEDS_REPLACE_STR, new_med_beds)
        new_med_baths = MED_BATHS_STR + str(med_baths)
        html_template = html_template.replace(MED_BATHS_REPLACE_STR, new_med_baths)
        new_med_value = MED_VALUE_STR + str(med_value)
        html_template = html_template.replace(MED_VALUE_REPLACE_STR, new_med_value)
        new_avg_dom = AVG_DOM_STR + avg_dom
        html_template = html_template.replace(AVG_DOM_REPLACE_STR, new_avg_dom)
        new_med_year = MED_YEAR_STR + str(med_year)
        html_template = html_template.replace(MED_YEAR_REPLACE_STR, new_med_year) 

        html_template = html_template.replace(DESCRIPTION_REPLACE_STR, prop_description)
        html_template = html_template.replace(MAP_1_REPLACE_STR, map_link_1)
        html_template = html_template.replace(MAP_2_REPLACE_STR, map_link_2)

        output_template_name = TEMPLATE_WRITE_NAME + listing_address_filename + HTML_EXTENSION
        with open(output_template_name, 'w') as fh_w:
            fh_w.write(html_template.encode("utf8"))

            #Later get the comps
            comp_objs = sf_bridge.get_comps_by_listing_name(listing_name)
            COMP_IMAGE = "https://images.benchmarkemail.com/client562548/image2994182.jpg"
            COMP_ADDRESS = "538 S Daisy Ave, Santa Ana, 92703"
            COMP_SQFT = "1,161" + " SQF"
            COMP_SOLD = "Sold " + "1/28/2016"
            COMP_PRICE = "$390,000"

            #Create new html rows for every comp.
            new_comp_rows = ""
            for comp in comp_objs:
                new_comp_row_html = '<tr><td class="trMargin"><table cellspacing="0" cellpadding="0" border="0"><tbody><tr><td height="10"></td></tr></tbody></table></td></tr><tr><td class="bmeImageContainerRow" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td class="tdPart" valign="top"><table cellspacing="0" cellpadding="0" border="0" class="bmeImageContainer" width="560" align="left" style="float:left;"><tbody><tr><td valign="top" name="tdContainer"><table cellspacing="0" cellpadding="0" border="0" class="bmeImageTable" dimension="50%" imgid="2" style="float:right;" align="right" width="270" height="151"><tbody><tr><td name="bmeImgHolder" width="280" align="center" valign="top" height="151"><img src=' + COMP_IMAGE + ' class="mobile-img-large" width="270" style="max-width: 623px; display: block;" border="0"></td></tr></tbody></table><table cellspacing="0" cellpadding="0" border="0" class="bmeCaptionTable" style="float:left;" align="left" width="270"><tbody><tr><td name="tblCell" valign="top" align="left" style="font-family: Arial,Helvetica,sans-serif; font-size: 14px; font-weight: normal; color: #383838; text-align: left;"><div style="line-height: 150%;"><span style="font-family: 'Times New Roman', Times, Baskerville, Georgia, serif;"><br><br><br><span style="font-size: 16px;">' + COMP_ADDRESS + '</span></span><br><span style="font-family: 'Times New Roman', Times, Baskerville, Georgia, serif; font-size: 18px;">' + COMP_PRICE + '  
<br>' + COMP_SQFT + '<br>' + COMP_SOLD + '</span></div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr>'

                new_comp_rows += new_comp_row_html

            html_template = html_template.replace(COMP_REPLACE_STR , new_comp_rows)

def main():
    email_generator = EmailGenerator()
    email_generator.create_buyer_marketing_email()

if __name__ == "__main__":
    main()