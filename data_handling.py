from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, FOAF
import rdflib
from pyredictit import pyredictit
import json
import sys, os
sys.path.append(os.path.abspath("../vars"))
from env_vars import *

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username=user_name,password=password)
events = pyredictit_api.search_for_contracts()

n = Namespace("https://www.predictit.org/Market/")
g = Graph()

for evnt in events:
    """
    this is where the dbpedia parser goes, and each entity that will be discovered
    will have a type associated with it, like so:
    g.add( (entity, RDF.type, type) )
    and it will be related to the event, as such:

    g.add( (event, FOAF.refers_to, entity) )
    """
    raw_event = json.loads(evnt)
    #print(raw_contract.keys())
    
    event        = URIRef(raw_event["URL"])
    name         = Literal(raw_event["Name"])
    ID           = Literal(raw_event["ID"])
    ticker       = Literal(raw_event["TickerSymbol"])
    short_name   = Literal(raw_event["ShortName"])
    time_stamp   = Literal(raw_event["TimeStamp"])
    status       = Literal(raw_event["Status"])
    image        = URIRef(raw_event["Image"])
    
    g.add( (event, RDF.type, FOAF.Event) )
    g.add( (image, RDF.type, FOAF.Image) )
    g.add( (event, FOAF.image, image) )
    g.add( (event, FOAF.name, name) )
    g.add( (event, FOAF.ID, ID) )
    g.add( (event, FOAF.ticker, ticker) )
    g.add( (event, FOAF.short_name, short_name) )
    g.add( (event, FOAF.time_stamp, time_stamp) )
    g.add( (event, FOAF.status, status) )
    for cont in raw_event["Contracts"]:
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

#query all short-names of events (not contracts):
for s,_,n in g.triples((None, RDF['type'], FOAF.Event)):
    #get all objects of type event
    my_triples= g.triples((s, FOAF['short_name'], None))
    #get all short-names of these events
    for t, _, m in my_triples:
        print(m)

