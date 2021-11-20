import requests
import json

from elasticsearch import Elasticsearch

e = Elasticsearch()
ENTITIES_TO_IGNORE = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']


def search_entities(query):
    wikidata_entities = []
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
        id_labels = {}
        if response and response['hits'] and response['hits']['hits']:
            for hit in response['hits']['hits']:
                label = hit['_source']['schema_name']
                id = hit['_id']
                id_labels.setdefault(id, set()).add(label)
        wikidata_entities.append(id_labels)
    return wikidata_entities
