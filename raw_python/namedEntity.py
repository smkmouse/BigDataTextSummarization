import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

def xstr(s):
    return '' if s is None else str(s)

import json
json = json.loads(open('fixedJSON.json').read())
for article in json['articles']:
    doc=nlp(article['Sentences'])
    for X in doc:
        isEnt = False
        for y in doc.ents:
            if X.i >= y.start and X.i < y.end:
                isEnt = True
                if X.i == y.start:
                    print(y.text, y.label_)
        if not isEnt:
            print(X.text, X.tag_)
