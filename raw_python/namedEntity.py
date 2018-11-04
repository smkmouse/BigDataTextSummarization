import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

import json
json = json.loads(open('fixedJSON.json').read())
for article in json['articles']:
    doc=nlp(article['Sentences'])
    print([(X.text, X.label_) for X in doc.ents])
