#This is the controls for parameters for the criteria we are filtering properties on

#Download Enabled
DOWNLOAD_ENABLED = True

#Parsing Enabled
PARSER_ENABLED = True

#When handling err msgs, should those be printed to the screen?
PRINT_ERR_MSG_TO_SCREEN = False

#When handling err msgs, should those be stored in the file system?
WRITE_ERR_MSG_TO_FS = True

#Types of properties that are set based on what type of input used (e.g. redfin spreadsheet = MLS)
PROPERTY_TYPE_REDFIN = "redfin"
PROPERTY_TYPE_RE_AGENT = "agent"
PROPERTY_TYPE_FORECLOSURE = "foreclosure"
PROPERTY_TYPE_ALL = "all"

#Switch that sets which inputs to run on this test
REDFIN_ENABLED = True

#Max number of properties we are allowing the script to evaluate
#MAX_PROPERTIES_TO_EVALUATE = 5
MAX_PROPERTIES_TO_EVALUATE = -1

#Num comps we are requesting from the Zillow API, 25 is the max
NUM_COMPS_REQUESTED = 25

#Should we get the Zestimate?
RENTZESTIMATE = True

#The min number of comps required to analyze a property
MIN_NUM_COMPS = 3

#Are we allowing shortsales?  This filter is done on the initial csv evaluation
SHORTSALE_SUPPORTED = False

#Max price of a property we are interested in    
MAX_PRICE = 800000
#MAX_PRICE = 1500000

#Min price of a property we are intereted in
#MIN_PRICE = 50000
MIN_PRICE = -1

#The min number of Days on Market we are interested in    
MIN_DOM = 30

#The max +- sq footage that the comparable property needs to be within the principal property
SQ_FOOTAGE_PERCENTAGE = .15

#The max distance that the comparable property needs to be within the principal property in miles
MAX_DISTANCE_FROM_PRINCIPAL = .5

#The commissions we will make per price point
COMMISSION_POINT_1 = 10000
COMMISSION_POINT_2 = 15000
COMMISSION_POINT_3 = 30000

PRICE_POINT_1 = 300000
PRICE_POINT_2 = 1000000

#The Repairs based on amount sq footage
LIGHT_REHAB = 35
MEDIUM_REHAB = 45
HIGH_REHAB = 60

#The percent of the ARV that we will use for the MAO
ARV_PERCENTAGE = .75

#Valid number of months for Comp Sold Date in months
SOLD_PRICE_INTERVAL = 6
