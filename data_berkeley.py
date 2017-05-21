from rdflib.store import Store, VALID_STORE, NO_STORE
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

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username=user_name,password=password)
events = pyredictit_api.search_for_contracts()

#n = Namespace("https://www.collectiwise,com/rdf/")
configString = "user=predictit dbname=predictit"

g = Graph('PostgreSQL', identifier=URIRef("http://example.com/g43"))
# first time create the store:
g.open(configString, create=True)

for evnt in events:
    raw_event = json.loads(evnt)
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
        #print(ref)
        g.add( (reference, FOAF.is_refered_to_by, event) )
        g.add( (event, FOAF.refers_to, reference) )
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


print("\n\n\n\nExample 3, Queries all events that refer to Donald Trump")

trump= URIRef(wikidict["Trump"])

my_triples=[]
for e,_,t in g.triples((None, FOAF['refers_to'], trump)):
    #print(e)
    my_triples.extend(list(g.triples((e, FOAF['short_name'], None))))

for _, _, n in my_triples:
    print(n)

g.close()
