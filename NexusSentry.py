# Main Functions
# ----------------------
import screen #for OCR
import interpreter #for interpreting messages

# Connections
# ----------------------
from blitz_js_query.blitz import Blitz

# NexusBot
# ----------------------
import NexusBot

# Misc
# ----------------------
import datetime
import calendar
import time




# Set up Request Lists to avoid double-posting in short time
timestart = calendar.timegm(time.gmtime())
NexusBotCount = 7
RequestCache = []
NexusBotCache = []

# Create slots for cache
for i in range(0, 30):
    RequestCache.append(i)
for i in range(0, 6):
    NexusBotCache.append(i)

# Connect to api.nexus-stats.com
api = Blitz({
    "api_url": "https://api.nexus-stats.com",
    "api_port": "443"
})
ItemList = {}



while True:

    # Screen rendering & OCR
    #---------------------------

    # Prepare image
    screen.shot()
    screen.enhance()

    # Run Tesseract, each line in array
    Msg = screen.ocr()

    # Remove redundant characters
    Msg = interpreter.cleanAll(Msg)



    # Message interpretation
    #---------------------------

    # Get item database from Nexus
    api.get("/warframe/v1/items/list").then(lambda res: print(res))



    # = Process each line =
    for l in range(0, len(Msg)):

        # Syntax Variables
        TOcount = 0 # used to assign trade operators to single requests
        TOval = []
        TO = None
        Request = []

        # Optimize input line for processing
        MsgWords = interpreter.convertLine(Msg[l])

        # Get Username from line
        Username = interpreter.getUsername(MsgWords)

        # Then remove special characters in rest of text
        MsgWords = interpreter.cleanBody(MsgWords, Username)




        # = Start Message Body Interpretation =
        for i in range(0, len(MsgWords)):

            # Determine Trade Operator
            TO = interpreter.getTradeOperator(MsgWords[i])

            # Add TO to list
            if not TO == None:
                TOcount = TOcount + 1 #increases every time TO is added
                TOval.append(TO) #save as WTS, 1 & compare TO number with Item Number

            # Get Request
            Request = interpreter.getRequest(i, MsgWords, ItemJSON, TOcount, TOval)



            # If Request is valid, send to server
            if not str(Msg[l]) in RequestCache and not (Request[0] == '' or Request[1] == ''):

                print(Request)

                payload = \
                {
                    'username': Username,
                    'to': Request[0],
                    'item': Request[1],
                    'comp': Request[2],
                    'type': Request[3],
                    'price': Request[4],
                    'user_key': 'python',
                    'user_secret': "super secret"
                }

                api.post("/warframe/v1/requests/new", payload)

        # = End of Message Body Interpretation =



        # Add User to Request Cache
        RequestCache.pop(0)
        RequestCache.append(str(Msg[l]))

    # = End of Processing each line =


    print('Job Done')
