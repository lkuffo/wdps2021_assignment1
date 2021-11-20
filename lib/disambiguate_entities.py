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

def disambiguate_entities(raw_text, entities, method = "naive"):
    found_entities = []
    if method == "naive":
        for original_label, entity in entities.items():
            for wikiID, label, score in entities:
                found_entities.append([wikiID, label])
                break
    else:
        for original_label, entity in entities.items():
            for wikiID, label, score in entities:
                disambiguate_rankings = {}
                if label not in disambiguate_rankings:
                    disambiguate_rankings[label] = {
                        "popularity": 0,
                        "relations": 0
                    }
                if len(found_entities) > 0:
                    for label_tmp, wikiID_tmp in found_entities:
                        local_connections = get_connections(wikiID, wikiID_tmp)
                        n_local_connections = len(local_connections)
                        disambiguate_rankings[label]["relations"] += n_local_connections
                entity_popularity = get_popularity(wikiID)
                disambiguate_rankings[label] = entity_popularity
    return found_entities