import requests
import json

from elasticsearch import Elasticsearch

e = Elasticsearch()
ENTITIES_TO_IGNORE = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']


def search_entities(query):
    wikidata_entities = {}
    for entityId, entity in query.items():
        label = entity[0]
        label_type = entity[1]
        if label_type in ENTITIES_TO_IGNORE: # Ignore entities from certain categories
            continue
        if len(label) < 2: # Do not take into account single characters entities
            continue
        p = {
            "query": {
                "query_string": {
                    "query": label
                }
            }
        }
        response = e.search(index="wikidata_en", body=json.dumps(p))
        wikidata_entities[entityId] = []
        if response and response['hits'] and response['hits']['hits']:
            for hit in response['hits']['hits']:
                score_es = hit['_score']
                if ('schema_name' in hit['_source']):
                    label_es = hit['_source']['schema_name']
                else:
                    label_es = label
                id_es = hit['_id']
                wikidata_entities[entityId].append([id_es, label_es, score_es, label])
    return wikidata_entities
