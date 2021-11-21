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
    # Get number of triplets of entity
    entityId = wikiID.replace('>', '').split('/')[-1]
    query = """
        PREFIX wd: <http://www.wikidata.org/entity/>  
        SELECT (COUNT(*) as ?Triples) 
        WHERE {
            VALUES ?s {  wd:""" + entityId + """ }
            ?s ?p ?o
        }
    """
    try:
        results = sparqlQuery(query)["results"]["bindings"][0]["Triples"]["value"]
    except Exception as e:
        print (e)
        return 0

def get_connections(wikiID1, wikiID2):
    entityId1 = wikiID1.replace('>', '').split('/')[-1]
    entityId2 = wikiID2.replace('>', '').split('/')[-1]
    query = """
        PREFIX wd: <http://www.wikidata.org/entity/>  
        SELECT (COUNT(*) as ?Triples) 
        WHERE {
            VALUES ?s {  wd:""" + entityId1 + """ }
            VALUES ?o {  wd:""" + entityId2 + """ }
            ?s ?p ?o
        }
    """
    try:
        results = sparqlQuery(query)["results"]["bindings"][0]["Triples"]["value"]
    except Exception as e:
        print (e)
        return 0

def disambiguate_entities(raw_text, entities, method = "naive"):
    found_entities = []
    if method == "naive":
        for entityLocalId, entity in entities.items():
            for wikiID, label, score, original_label in entity:
                found_entities.append([wikiID, original_label])
                break
    else:
        for entityLocalId, entity in entities.items():
            for wikiID, label, score, original_label in entity:
                disambiguate_rankings = {}
                if label not in disambiguate_rankings:
                    disambiguate_rankings[label] = {
                        "popularity": 0,
                        "relations": 0
                    }
                if len(found_entities) > 0:
                    for wikiID_tmp, label_tmp in found_entities:
                        # Same context assumption
                        if (wikiID_tmp == wikiID):
                            found_entities.append([wikiID, original_label])
                            break
                    for wikiID_tmp, label_tmp in found_entities:
                        local_connections = get_connections(wikiID, wikiID_tmp)
                        n_local_connections = len(local_connections)
                        disambiguate_rankings[label]["relations"] += n_local_connections
                entity_popularity = get_popularity(wikiID)
                disambiguate_rankings[label] = entity_popularity
            #sort_ranking = dict(sorted(disambiguate_rankings.items(), key=lambda item: item[1]["popularity"]))
    return found_entities