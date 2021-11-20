import requests
import json
from elasticsearch import Elasticsearch
import trident
import json

print("Loading db...")
db = trident.Db("assets/wikidata-20200203-truthy-uri-tridentdb")
print("Done")

def search(query):
    e = Elasticsearch(["localhost:9200"])
    p = { "query" : { "query_string" : { "query" : query }}}
    response = e.search(index="wikidata_en", body=json.dumps(p))
    id_labels = {}
    if response:
        for hit in response['hits']['hits']:
            label = hit['_source']['schema_name']
            id = hit['_id']
            id_labels.setdefault(id, set()).add(label)
    return id_labels

def searchTrident(term):
    term_id = db.lookup_id(term)
    print(db.po(term_id))

    results = db.sparql(term_id)
    json_results = json.loads(results)
    return json_results


if __name__ == '__main__':
    import sys
    try:
        _, QUERY = sys.argv
    except Exception as e:
        QUERY = 'Vrije Universiteit Amsterdam'

    for entity, labels in search(QUERY).items()[:1]:
        print(entity, labels)
        result = searchTrident(entity)
        print (result)
