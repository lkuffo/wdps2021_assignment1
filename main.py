#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import gzip
from lib.parse_entities import parse_entities
from lib.search_entities import search_entities
from lib.disambiguate_entities import disambiguate_entities
from lib.parse_warc import get_html_warc, text_extract

OUTPUT_FILE = "sample_predictions.tsv"

def _parse_warc(_input):
    return parse_warc(_input)

def _parse_entities(raw_text):
    return parse_entities(raw_text)

def _search_entities(entities):
    return search_entities(entities)

def _disambiguate_entities(raw_text, wiki_entities, method = "naive"):
    return disambiguate_entities(raw_text, wiki_entities, method)

def write_result(file_pointer, entities):
    for wikiID, label in entities:
        file_pointer.write('\t' + wikiID + '\t' + label + '\n')

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)

    f = open(OUTPUT_FILE, 'w')

    for html_prase, page_id in get_html_warc(INPUT):
        print(page_id)
        try: 
            raw_text = text_extract(html_prase)
            #print (raw_text)
            entities = _parse_entities(raw_text)
            if (entities == None or len(entities) < 1):
                continue
            wiki_entities = _search_entities(entities)
            #print (wiki_entities)
            final_entities = _disambiguate_entities(raw_text, wiki_entities, "naive")
            #print(final_entities)
            write_result(f, final_entities)
        except Exception as e:
            print (e)
    f.close()