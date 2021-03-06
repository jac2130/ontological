import sqlite3
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, FOAF
import rdflib
from pyredictit import pyredictit
import json
import sys, os
sys.path.append(os.path.abspath("../vars"))
from env_vars import *

wikidict={"Trump": "http://dbpedia.org/resource/Donald_Trump",
          "Clinton": "http://dbpedia.org/resource/Hillary_Clinton", "Ossoff": "https://en.wikipedia.org/wiki/Jon_Ossoff", "Virginia": "https://en.wikipedia.org/wiki/Virginia", "Georgia": "https://en.wikipedia.org/wiki/Georgia_(U.S._state)","Election":"https://en.wikipedia.org/wiki/Elections_in_the_United_States"}

def handle_missing(thing):
    try:
        thing=float(thing)
    except:
        thing = thing
        
    if type(thing)!=type(float(1)):
        return float(-1.0)
    else:
        return thing
###############SQLITE###############

conn = sqlite3.connect('predictit.db')
cursor = conn.cursor()

##############TABLES##########################################

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username=user_name,password=password)
events = pyredictit_api.search_for_contracts()

n = Namespace("https://www.predictit.org/Market/")
g = Graph()

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
    
    values = str(tuple((name,ID_str, ticker, short_name, time_stamp, status, image, category_name, category)))
    #print(values)
    cursor.execute("INSERT INTO questions VALUES" + str(values))
    
    # Save (commit) the changes
    conn.commit()
    ####################################################################
    """
    this is where the dbpedia parser goes, and each entity that will be discovered
    will have a type associated with it, like so:
    g.add( (entity, RDF.type, type) )
    and it will be related to the event, as such:

    g.add( (event, FOAF.refers_to, entity) )
    """

    #print(raw_contract.keys())
    
    event        = URIRef(raw_event["URL"])
    name         = Literal(raw_event["Name"])
    ID           = Literal(raw_event["ID"])
    ticker       = Literal(raw_event["TickerSymbol"])
    short_name   = Literal(raw_event["ShortName"])
    time_stamp   = Literal(raw_event["TimeStamp"])
    status       = Literal(raw_event["Status"])
    image        = URIRef(raw_event["Image"])
    category     = URIRef("https://www.predictit.org/Market/" + raw_event["Category"])
    category_name=Literal(raw_event["Category"])
    
    g.add( (event, RDF.type, FOAF.Event) )
    g.add( (image, RDF.type, FOAF.Image) )
    g.add( (category, RDF.type, FOAF.Category) )
    g.add( (category, FOAF.name, category_name) )
    g.add( (event, FOAF.category, category) )
    g.add( (category, FOAF.includes, event) )
    g.add( (event, FOAF.image, image) )
    g.add( (event, FOAF.name, name) )
    g.add( (event, FOAF.ID, ID) )
    g.add( (event, FOAF.ticker, ticker) )
    g.add( (event, FOAF.short_name, short_name) )
    g.add( (event, FOAF.time_stamp, time_stamp) )
    g.add( (event, FOAF.status, status) )
    for ref in raw_event["References"]:
        reference = URIRef(ref)
        g.add( (reference, FOAF.is_refered_to_by, event) )
        g.add( (event, FOAF.refers_to, reference) )
        
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
        values = str(tuple((name,ID, ID_str, ticker, short_name, long_name, date_end, status, image, last_trade_p, best_buy_yes, best_buy_no, best_sell_yes, best_sell_no, last_close_p)))
        #print(values)
        
        cursor.execute("INSERT INTO contracts VALUES" + str(values))
        """
        cursor.execute('''CREATE TABLE contracts
             (name text, ID text, question text, ticker text, short_name text, long_name text, date_end text, status text, image_url text, last_trade_price real, best_buy_yes real, best_buy_no real, best_sell_yes real, best_sell_no real, last_close_price real)''')
"""
        # Save (commit) the changes
        conn.commit()
        ########################################################
        contract     = URIRef(cont["URL"])
        name         = Literal(cont["Name"])
        ID           = Literal(cont["ID"])
        short_name   = Literal(cont["ShortName"])
        long_name    = Literal(cont["LongName"])
        ticker       = Literal(cont["TickerSymbol"])
        date_end     = Literal(cont["DateEnd"])
        image        = URIRef(cont["Image"])
        status       = Literal(cont["Status"])
        last_trade_p = Literal(cont["LastTradePrice"])
        best_buy_yes = Literal(cont["BestBuyYesCost"])
        best_buy_no  = Literal(cont["BestBuyNoCost"])
        best_sell_yes= Literal(cont["BestSellYesCost"])
        best_sell_no = Literal(cont["BestSellNoCost"])
        last_close_p = Literal(cont["LastClosePrice"])
        
        g.add( (image, RDF.type, FOAF.Image) )
        g.add( (contract, RDF.type, FOAF.Contract) )
        #for easy traversing both ways, between contracts and events,
        #we draw the arrow both ways:
        
        g.add( (event, FOAF.contract, contract) )
        g.add( (contract, FOAF.event, event) )
        
        g.add( (contract, FOAF.image, image) )
        g.add( (contract, FOAF.category, category) )
        g.add( (contract, FOAF.name, name) )
        g.add( (contract, FOAF.ID, ID) )
        g.add( (contract, FOAF.short_name, short_name) )
        g.add( (contract, FOAF.long_name, long_name) )
        g.add( (contract, FOAF.ticker, ticker) )
        g.add( (contract, FOAF.date_end, date_end) )
        g.add( (contract, FOAF.status, status) )
        g.add( (contract, FOAF.last_trade_price, last_trade_p) )
        g.add( (contract, FOAF.best_buy_yes, best_buy_yes) )
        g.add( (contract, FOAF.best_sell_yes, best_sell_yes) )
        g.add( (contract, FOAF.best_buy_no, best_buy_no) )
        g.add( (contract, FOAF.best_sell_no, best_sell_no) )
        g.add( (contract, FOAF.last_close_price, last_close_p) )
#close the connection to the sqlite database.         
conn.close()
#query all short-names of events (not contracts):
print("Example 1, Queries all short names for events only (not for contracts)")
for s,_,n in g.triples((None, RDF['type'], FOAF.Event)):
    #get all objects of type event
    my_triples= g.triples((s, FOAF['short_name'], None))
    #get all short-names of these events
    for t, _, m in my_triples:
        print(m)

        
print("\n\n\n\nExample 2, Queries all shortnames for events only in the US politics category")

my_triples=[]

for c,_,_ in g.triples((None, FOAF['name'], Literal("us_politics"))):
    
    for d,_, e in g.triples((c, FOAF['includes'], None)):
        
        my_triples.extend(list(g.triples((e, FOAF['short_name'], None))))
        
for _, _, n in my_triples:
    print(n)

print("\n\n\n\nExample 3, Queries all events that refer to Donald Trump")

trump= URIRef(wikidict["Trump"])

my_triples=[]
for e,_,t in g.triples((None, FOAF['refers_to'], trump)):
    my_triples.extend(list(g.triples((e, FOAF['short_name'], None))))

for _, _, n in my_triples:
    print(n)

"""

print("\n\n\n\nExample 4, Queries all events that refer to Hillary Clinton")

clinton = URIRef(wikidict["Clinton"])

my_triples=[]
for e,_,t in g.triples((None, FOAF['refers_to'], clinton)):
    my_triples.extend(list(g.triples((e, FOAF['short_name'], None))))

for _, _, n in my_triples:
    print(n)
                
print("\n\n\n\nExample usage of DBPedia, Donald")
g=rdflib.Graph()
g.load('http://dbpedia.org/resource/Donald_Trump')
for s,p,o in g:
    print((s,p,o))
    

print("\n\n\n\nExample usage of DBPedia, Hillary")
g=rdflib.Graph()
g.load('http://dbpedia.org/resource/Hillary_Clinton')
for s,p,o in g:
    print(p)
"""
