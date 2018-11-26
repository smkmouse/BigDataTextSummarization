import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import json
from multiprocessing import Pool, Lock

printLock = Lock()

def namedEntityExtract(article):
    global printLock
    outString = ""
    doc=nlp(article['Sentences'])
    for X in doc:
        isEnt = False
        for y in doc.ents:
            if X.i >= y.start and X.i < y.end:
                isEnt = True
                if X.i == y.start:
                    outString = outString + y.text + " " + y.label_ + '\n'
        if not isEnt:
            outString = outString + X.text + " " + X.tag_ + '\n'
    printLock.acquire()
    print(outString)
    printLock.release()

json = json.loads(open('lda_filtered_docs_big_fixed.json').read())
with Pool(40) as p:
    p.map(namedEntityExtract, json['articles'])
