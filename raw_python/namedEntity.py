import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import json
from multiprocessing import Pool

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
                    outString += y.text+", "+y.label_+'\n'
        if not isEnt:
            outString += X.text+", "+X.tag_+'\n'
    return outString

json = json.loads(open('fixedJSON.json').read())
with Pool(40) as p:
    print(p.map(namedEntityExtract, json['articles']))
    
