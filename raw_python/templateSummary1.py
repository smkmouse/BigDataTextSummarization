#!/usr/bin/env python3
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import json
import multiprocessing
from multiprocessing import Manager, Pool

#README: Specify input file at inputFile var below, output goes to standard out and should be redirected
inputFile = "lda_filtered_docs_big_fixed.json" #expects valid json, not spark json (use listify.py)
def runSpacy(article):
    outString = ""
    doc=nlp(article['Sentences'])
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for money in filter(lambda w: w.ent_type_ == 'MONEY', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))

    for money in filter(lambda w: w.ent_type_ == 'DATE', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))

    for money in filter(lambda w: w.ent_type_ == 'GPE', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))

    for money in filter(lambda w: w.ent_type_ == 'CARDINAL', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))

    for money in filter(lambda w: w.ent_type_ == 'ORG', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))

    for x in relations:
        print(str(x[0]) + "|" + str(x[1]))

jsonload = json.loads(open(inputFile).read())
with Pool(multiprocessing.cpu_count()) as p:
    p.map(runSpacy, jsonload['articles'])
