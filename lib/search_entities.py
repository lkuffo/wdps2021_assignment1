import requests
import json

from elasticsearch import Elasticsearch

e = Elasticsearch()
ENTITIES_TO_IGNORE = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']


def search_entities(query):
    wikidata_entities = {}
    for entity in query.values():
        label = entity[0]
        label_type = entity[1]
        if label_type in ENTITIES_TO_IGNORE:
            continue
        p = {
            "query": {
                "query_string": {
                    "query": label
                }
            }
        }
        response = e.search(index="wikidata_en", body=json.dumps(p))
        wikidata_entities[label] = []
        if response and response['hits'] and response['hits']['hits']:
            for hit in response['hits']['hits']:
                label_es = hit['_source']['schema_name']
                id_es = hit['_id']
                wikidata_entities[label].append([id_es, label_es])
                #id_labels.setdefault(id_es, set()).add(label_es)
        #wikidata_entities.append(id_labels)
    return wikidata_entities
