import urllib, json, requests

"""
This file demonstrates how to make a simple SPARQL query against the public
WikiData graph endpoint for the WDPS course.

Additional information:
- Simple SPARQL editor: http://fs0.das5.cs.vu.nl:10011/sparql
- Additional information http://fs0.das5.cs.vu.nl:10011/sparql/?help=intro
- Prefixes in the dataset: http://fs0.das5.cs.vu.nl:10011/sparql/?help=nsdecl
"""

HOST = "http://fs0.das5.cs.vu.nl:10011/sparql"

def sparqlQuery(query, format="application/json"):
    resp = requests.get(HOST + "?" + urllib.parse.urlencode({
        "default-graph": "",
        "should-sponge": "soft",
        "query": query,
        "debug": "on",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": ""
    }))
    print (resp.content.decode("utf-8"))
    return json.loads(resp.content.decode("utf-8"))


def get_popularity(wikiID):
    return ""

def get_connections(wikiID1, wikiID2):
    return ""

def disambiguate_entities(raw_text, entities):
    found_entities = []
    for label, wikiID in entities:
        disambiguate_rankings = {}
        if label not in disambiguate_rankings:
            disambiguate_rankings[label] = {
                "popularity": 0,
                "relations": 0
            }