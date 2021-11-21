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
                found_entities.append([wikiID, original_label, label])
                break
    else:
        # For each entity
        for entityLocalId, entity in entities.items():
            found = 0
            disambiguate_rankings = {}

            # For each candidate of the entity
            for wikiID, label, score, original_label in entity:
                if label not in disambiguate_rankings:
                    disambiguate_rankings[label] = {
                        "popularity": 0,
                        "relations": 0,
                        "info": [wikiID, label, score, original_label]
                    }

                if len(found_entities) > 0:
                    for wikiID_tmp, label_tmp in found_entities:
                        # Same context assumption
                        if (wikiID_tmp == wikiID):
                            found_entities.append([wikiID, original_label, label])
                            found = 1
                            break
                    if found == 1:
                        break

                    for wikiID_tmp, label_tmp in found_entities:
                        local_connections = get_connections(wikiID, wikiID_tmp)
                        n_local_connections = len(local_connections)
                        disambiguate_rankings[label]["relations"] += n_local_connections
            
                entity_popularity = get_popularity(wikiID)
                disambiguate_rankings[label] = entity_popularity
            if (method == "popularity"):
                sort_ranking = dict(sorted(disambiguate_rankings.items(), key=lambda item: item[1]["popularity"])).values()
                print(sort_ranking)
                best_ranked_entity = sort_ranking[0]["info"]
                print(best_ranked_entity)
                found_entities.append([best_ranked_entity[0], best_ranked_entity[-1], best_ranked_entity[1]])
    return found_entities