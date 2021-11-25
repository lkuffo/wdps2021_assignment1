import requests
import json
import spacy
from scipy import spatial

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_lg")

from elasticsearch import Elasticsearch

e = Elasticsearch()
ENTITIES_TO_IGNORE = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

#
# query: Dictionary of lists containing the entities from the entity recognition process
#
def search_entities(query):
    wikidata_entities = {}
    for entityId, entity in query.items():
        label = entity[0]
        label_type = entity[1]
        label_vector = entity[2]
        if label_type in ENTITIES_TO_IGNORE: # Ignore entities from certain categories
            continue
        if len(label) < 2: # Do not take into account single characters entities
            continue
        p = {
            "query": {
                "query_string": {
                    "query": label
                }
            },
            "size": 10
        }
        # Query candidates to elasticsearch
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

                # We obtain the word embeddings vector of the out of context term
                vector_es = nlp(label_es).vector
                # We calculate cosime similarity of the entity with the candidate
                cosine_similarity = 1 - spatial.distance.cosine(vector_es, label_vector)
                print(label, label_es, cosine_similarity, score_es)

                # Treshhold to be considered as a candidate
                if cosine_similarity < 0.40:
                    continue

                wikidata_entities[entityId].append([id_es, label_es, score_es, label, label_type])
    return wikidata_entities
