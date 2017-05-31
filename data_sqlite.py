from pyredictit import pyredictit
import json
import sys, os
root =os.path.abspath("../../../../..")
sys.path.append(root)
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from env_vars import *

"""
# to handle missing values for some of the type of prices (real values are expected)
def handle_missing(thing):
    try:
        thing=float(thing)
    except:
        thing = thing
        
    if type(thing)!=type(float(1)):
        return float(-1.0)
    #a missing value is denoted by a floating point version of negative 1
    else:
        return thing


conn = sqlite3.connect('predictit.db')
cursor = conn.cursor()
pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username=user_name,password=password)
events = pyredictit_api.search_for_contracts()

for evnt in events:
        ######first SQLITE #############
            # Insert a row of data
    raw_event = json.loads(evnt)
    event_str    = str(raw_event["URL"])
    name         = " ".join([''.join(e for e in strin if e.isalnum())  for strin in str(raw_event["Name"]).split()])
    
    ID_str       = str(raw_event["ID"])
    ticker       = str(raw_event["TickerSymbol"])
    short_name   = " ".join([''.join(e for e in strin if e.isalnum())  for strin in str(raw_event["ShortName"]).split()])
    time_stamp   = str(raw_event["TimeStamp"])
    status       = str(raw_event["Status"])
    image        = str(raw_event["Image"])
    category     = str("https://www.predictit.org/Market/" + raw_event["Category"])
    category_name= str(raw_event["Category"])

    values = str(tuple((name, event_str, ID_str, ticker, short_name, time_stamp, status, image, category_name, category)))
    #print(values)
    questions=cursor.execute("SELECT * FROM questions WHERE ID="+ID_str)
    
    for question in questions:
        if not question:
            cursor.execute("INSERT INTO questions VALUES" + str(values))
            for q in cursor.execute("SELECT * FROM questions WHERE ID="+ID_str):
                print(q)
                
        else:
            pass
        
    #create new time stamp
    time_stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    
    values = str(tuple((ID_str, status, time_stamp)))
                 
    cursor.execute("INSERT INTO question_vars VALUES" + str(values))
    # Save (commit) the changes
    conn.commit()

    for cont in raw_event["Contracts"]:
                ##########SQLite###################
        contract     = str(cont["URL"])
        name         = " ".join([''.join(e for e in strin if e.isalnum())  for strin in str(cont["Name"]).split()])

        ID           = str(cont["ID"])
        short_name   = " ".join([''.join(e for e in strin if e.isalnum())  for strin in str(cont["ShortName"]).split()])

        long_name    = " ".join([''.join(e for e in strin if e.isalnum())  for strin in str(cont["LongName"]).split()])

        ticker       = str(cont["TickerSymbol"])
        date_end     = str(cont["DateEnd"])
        image        = str(cont["Image"])
        status       = str(cont["Status"])
        last_trade_p = handle_missing(cont["LastTradePrice"])
        best_buy_yes = handle_missing(cont["BestBuyYesCost"])
        best_buy_no  = handle_missing(cont["BestBuyNoCost"])
        best_sell_yes= handle_missing(cont["BestSellYesCost"])
        best_sell_no = handle_missing(cont["BestSellNoCost"])
        last_close_p = handle_missing(cont["LastClosePrice"])
        
        
        
        values = str(tuple((name,contract, ID, ID_str, ticker, short_name, long_name,image, time_stamp)))

        
        contracts=cursor.execute("SELECT * FROM contracts WHERE ID="+ID)
        for contract in contracts:
            if not contract:
                print(shortname)
                cursor.execute("INSERT INTO contracts VALUES" + str(values))
            else:
                pass
            
        values = str(tuple((ID, time_stamp, date_end, status, last_trade_p, best_buy_yes, best_buy_no, best_sell_yes, best_sell_no, last_close_p)))
        
        cursor.execute("INSERT INTO contract_vars VALUES" + str(values))
        conn.commit()

conn.close()
        
"""
