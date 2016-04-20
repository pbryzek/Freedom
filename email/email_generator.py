import os
import sys
import codecs
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

os.chdir(scriptPath)

#append the relative location you want to import from
sys.path.append("..")

from sf_bridge import SFBridge

ENABLE_SENDING_EMAIL = True
ENABLE_SAVE_EMAIL_SF = False

TEMPLATE_READ_NAME = "./inputs/email_marketing_template.html"
TEMPLATE_WRITE_NAME = "./results/email_marketing_"

HTML_EXTENSION = ".html"

#This is the SF ID which represent the property we will generate buyer's marketing materials
PROPERTY_ID = "a0036000002cZyY"

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

DESCRIPTION_REPLACE_STR = "DESCRIP TEXT TO FIND AND REPLACE"
MAP_1_REPLACE_STR = "https://images.benchmarkemail.com/client562548/image2993695.jpg"
MAP_2_REPLACE_STR = "https://images.benchmarkemail.com/client562548/image2993697.jpg"

COMP_REPLACE_STR = "COMP TEXT TO FIND AND REPLACE"

ARV_STR = "ARV: "
ARV_REPLACE_STR = ARV_STR + "INSERT"

class EmailGenerator(object):

    def handle_dollars(self, num):
        num_str = self.clean_num_str(num) 
        dollars = self.convert_to_dollars(num_str)
        return dollars

    def convert_to_dollars(self, num):
        dollars = "$" + num
        return dollars

    def clean_num_str(self, num_str):
        if not isinstance(num_str, basestring):
            num_str = str(num_str) 
        num_str = num_str.replace(".0", "")
        return num_str

    def create_buyer_marketing_email(self):
        #Get the listing object
        sf_bridge = SFBridge()
        listing_obj = sf_bridge.get_listing_by_id(PROPERTY_ID)

        #Parse out the relevant info
        listing_obj["AVG_Sq_Ft__c"]
        listing_name = listing_obj["Name"].strip()
        st_num = self.clean_num_str(listing_obj["Street_Number__c"].strip())
        st = listing_obj["Street_Name__c"].strip()
        state = listing_obj["State__c"].strip()
        latitude = listing_obj["Latitude__c"]
        longitude = listing_obj["Longitude__c"]
        city = listing_obj["City__c"].strip()
        zip = listing_obj["Zip_Code__c"].strip()
        mao_med = listing_obj["MAO_Medium__c"]
        mls_num = listing_obj["MLS__c"]
        mls_num = mls_num.replace("-", "")

        num_beds = listing_obj["Beds__c"]
        num_baths = listing_obj["Baths__c"]
        num_sqft = self.clean_num_str(listing_obj["Sq_Ft__c"])
        lotsize = self.clean_num_str(listing_obj["Lot_Size__c"])
        yearbuilt = listing_obj["Year_Built__c"]

        avg_dom = self.clean_num_str(listing_obj["AVG_DOM__c"])

        actual_repair_num = self.clean_num_str(listing_obj["Actual_Rehab_Estimate__c"])
        actual_repair = self.convert_to_dollars(actual_repair_num)
        actual_list_price_num = self.clean_num_str(listing_obj["Actual_Offer__c"])
        actual_list_price = self.convert_to_dollars(actual_list_price_num)        

        avg_sold_price_num = self.clean_num_str(listing_obj["Median_Value__c"])
        avg_sold_price = self.convert_to_dollars(avg_sold_price_num)

        med_sqf = self.clean_num_str(listing_obj["Median_SQF__c"])
        med_beds = listing_obj["Median_of_Beds__c"]
        med_baths = listing_obj["Median_of_Baths__c"]
        med_value_num = self.clean_num_str(listing_obj["Median_Value__c"])
        med_value = self.convert_to_dollars(med_value_num)
        med_year = listing_obj["Median_Year_Built__c"]
        arv = listing_obj["Principal_ARV__c"]

        prop_description = listing_obj["Description__c"]

        map_link_1 = listing_obj["Image_Google_1__c"]
        map_link_2 = listing_obj["Image_Google_2__c"] 
        image_main = listing_obj["Image_Main__c"]

        image_1 = listing_obj["Image_1__c"]
        image_2 = listing_obj["Image_2__c"]

        listing_address = st_num + " " + st + ", " + city + ", " + state + " " + zip
        listing_address_filename = listing_address.replace(" ", "_")
        listing_address_filename = listing_address_filename.replace(",", "")
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
        new_arv_str = ARV_STR + self.handle_dollars(str(arv)) 
        html_template = html_template.replace(ARV_REPLACE_STR, new_arv_str)

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
        new_avg_dom = AVG_DOM_STR + str(avg_dom)
        html_template = html_template.replace(AVG_DOM_REPLACE_STR, new_avg_dom)
        new_med_year = MED_YEAR_STR + str(med_year)
        html_template = html_template.replace(MED_YEAR_REPLACE_STR, new_med_year) 

        html_template = html_template.replace(DESCRIPTION_REPLACE_STR, prop_description)
        html_template = html_template.replace(MAP_1_REPLACE_STR, map_link_1)
        html_template = html_template.replace(MAP_2_REPLACE_STR, map_link_2)

        comp_objs = sf_bridge.get_comps_by_listing_id(PROPERTY_ID)

        #Create new html rows for every comp.
        new_comp_rows = ""

        for comp in comp_objs:
            COMP_IMAGE = comp["Image_Main__c"] 
            
            city = comp["City__c"]
            state = comp["State__c"]
            street = comp["Street_Name__c"]
            number = self.clean_num_str(comp["Street_Number__c"])
            zip = self.clean_num_str(comp["Zip_Code__c"])
            COMP_ADDRESS = str(number) + " " + street + ", " + city + ", " + str(zip) 
           
            sqft = comp["Sq_Ft__c"]
            COMP_SQFT = self.clean_num_str(str(sqft)) + " SQF"
            
            sold_date = comp["Sold_Date__c"]
            COMP_SOLD = "Sold " + sold_date
            
            price = comp["Sold_Price__c"]
            COMP_PRICE = self.handle_dollars(str(price))

            COMP_INFO = COMP_ADDRESS + "<br>" + COMP_PRICE + "<br>" + COMP_SQFT + "<br>" + COMP_SOLD

	    new_comp_row_html = '<tr><td align="left">' + COMP_INFO + '</td><td align="right"><img src="' + COMP_IMAGE + '" width="150" style="max-width: 150px; display: block; width: 150px;" alt="" border="0"></td></tr><tr><td style="overflow:hidden; height: 10px;"><span style="font-family: "Times New Roman", Times, Baskerville, Georgia, serif;"text-transform:capitalize;line-height:100%;"></span></td><td></td></tr>'

            new_comp_rows += new_comp_row_html

        html_template = html_template.replace(COMP_REPLACE_STR, new_comp_rows)
        #Finally write it to file.
        encoded_html_template = html_template.encode("utf8")
        output_template_name = TEMPLATE_WRITE_NAME + listing_address_filename + HTML_EXTENSION
        with open(output_template_name, 'w') as fh_w:
            fh_w.write(encoded_html_template)

        if ENABLE_SAVE_EMAIL_SF:
            sf_bridge.save_email_to_sf(encoded_html_template, PROPERTY_ID)

        self.send_email(encoded_html_template)

    def send_email(self, encoded_html_template):
        if not ENABLE_SENDING_EMAIL:
            return

        from_email = "refreedomgroup@gmail.com"
        email_password = "januszbarbara" 
        to_email = "asdughman@gmail.com"

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Buyer's Marketing"
        msg['From'] = from_email
        msg['To'] = to_email

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(encoded_html_template, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)

        # Send the message via gmail SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(from_email, email_password)
        mail.sendmail(from_email, to_email, msg.as_string())
        mail.quit()

    def count_letters(self, word):
        return len(word) - word.count(' ')

def main():
    email_generator = EmailGenerator()
    email_generator.create_buyer_marketing_email()

if __name__ == "__main__":
    main()
