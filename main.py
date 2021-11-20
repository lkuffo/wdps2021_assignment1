#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import gzip
from lib.parse_entities import parse_entities

KEYNAME = "WARC-TREC-ID"

def parse_webpage(location):
    return """
        The fate of Lehman Brothers, the beleaguered investment bank, hung in the balance on Sunday as Federal Reserve officials and the leaders of major financial institutions continued to gather in emergency meetings trying to complete a plan to rescue the stricken bank.  Several possible plans emerged from the talks, held at the Federal Reserve Bank of New York and led by Timothy R. Geithner, the president of the New York Fed,and Treasury Secretary Henry M. Paulson Jr. I earned 10 million
        dollars today. Leonardo Kuffo is a handsome guy with 10 or more ex girlfriends all over the Ecuador and Amsterdam. When Sebastian Thrun started working on self-driving cars at, Google in 2007, few people outside of the company took him seriously. I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn’t worth talking to, said Thrun, in an interview with Recode earlier this week.
    """

def _parse_entities(raw_text):
    return parse_entities(raw_text)

def search_entities(entities):
    return []

def disambiguate_entities(raw_text, entities):
    return []

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)

    raw_text = parse_webpage(INPUT)
    entities = _parse_entities(raw_text)

    print(entities)

    # with gzip.open(INPUT, 'rt', errors='ignore') as fo:
    #     for record in split_records(fo):
    #         for key, label, wikidata_id in find_labels(record):
    #             print(key + '\t' + label + '\t' + wikidata_id)