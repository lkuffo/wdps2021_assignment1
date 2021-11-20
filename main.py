#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import gzip
from lib.parse_entities import parse_entities
from lib.search_entities import search_entities
from lib.disambiguate_entities import disambiguate_entities

KEYNAME = "WARC-TREC-ID"
OUTPUT_FILE = "sample_predictions.tsv"

def _parse_webpage(webpage):
    return """
        The fate of Lehman Brothers, the beleaguered investment bank, hung in the balance on Sunday as Federal Reserve officials and the leaders of major financial institutions continued to gather in emergency meetings trying to complete a plan to rescue the stricken bank.  Several possible plans emerged from the talks, held at the Federal Reserve Bank of New York and led by Timothy R. Geithner, the president of the New York Fed,and Treasury Secretary Henry M. Paulson Jr. I earned 10 million
        dollars today. Leonardo Kuffo is a handsome guy with 10 or more ex girlfriends all over the Ecuador and Amsterdam. When Sebastian Thrun started working on self-driving cars at, Google in 2007, few people outside of the company took him seriously. I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn’t worth talking to, said Thrun, in an interview with Recode earlier this week.
    """

def _parse_entities(raw_text):
    return parse_entities(raw_text)

def _search_entities(entities):
    return search_entities(entities)

def _disambiguate_entities(raw_text, wiki_entities, method = "naive"):
    return disambiguate_entities(raw_text, wiki_entities, method)

def write_result(file_pointer, entities):
    for website, wikiID, label in entities:
        f.write(website + '\t' + wikiID + '\t' + label + '\n')
    f.close()

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)

    f = open(OUTPUT_FILE, 'w')
    for webpage in webpages:
        raw_text = _parse_webpage(INPUT)
        entities = _parse_entities(raw_text)
        wiki_entities = _search_entities(entities)
        final_entities = _disambiguate_entities(raw_text, wiki_entities, "naive")
        print(final_entities)

        write_result(f, final_entities)
    f.close()