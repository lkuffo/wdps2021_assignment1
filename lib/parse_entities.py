#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
@author Group 17-Tong Wu(t3.wu@student.vu.nl 2734542)
@Create 11-14-2021 16:00 PM
This is a NER Candidate used in wdps assignment1 Entity linker
Spacy NER
"""
import spacy
spacy.cli.download("en")

"""
PERSON:      People, including fictional.
NORP:        Nationalities or religious or political groups.
FAC:         Buildings, airports, highways, bridges, etc.
ORG:         Companies, agencies, institutions, etc.
GPE:         Countries, cities, states.
LOC:         Non-GPE locations, mountain ranges, bodies of water.
PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
EVENT:       Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART: Titles of books, songs, etc.
LAW:         Named documents made into laws.
LANGUAGE:    Any named language.
DATE:        Absolute or relative dates or periods.
TIME:        Times smaller than a day.
PERCENT:     Percentage, including ”%“.
MONEY:       Monetary values, including unit.
QUANTITY:    Measurements, as of weight or distance.
ORDINAL:     “first”, “second”, etc.
CARDINAL:    Numerals that do not fall under another type.
"""
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")


# Process whole documents
def spacy_ner_from_file(file_location):
    with open(file_location) as sample:
        doc = nlp(sample.read())
        # Noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        # Verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        entities_list = doc.ents
    return entities_list

def spacy_ner_from_text(raw_text):
    doc = nlp(raw_text)
    # Noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    # Verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    entities_list = doc.ents
    return entities_list

def spacy_dictionary(entities_list):
    dic = {}
    i = 0
    for entity in entities_list:
        i += 1
        dic['Entity {}'.format(i)] = (entity.text, entity.label_)
    return dic

def parse_entities(raw_text):
    entities_list = spacy_ner_from_text(raw_text)
    return spacy_dictionary(entities_list).items()
