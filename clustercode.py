#!/usr/bin/env python

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)

import spacy
import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')
nltk.download('punkt')

path = "/user/cs4984cs5984f18_team3/*.json"
htmlDF = spark.read.json(path)

htmlDF.printSchema()  # show data schema
htmlDF.show()

text = htmlDF.select("Sentences")
text.count()

data = htmlDF.select('Sentences').rdd

# cleaning data
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

# remove null element from data (MapPartitionsRDD)
data_remove_null = data.filter(lambda e: len(e) > 0)
#.collect()

#tokenize words and filter out stop_words and not alpha and length is between 3 and 16
word_filter = data_remove_null.map(lambda line: re.split(' ', line[0])).map(lambda txt: [w.lower() for w in txt if w.lower().isalpha()]).map(lambda txt: [w for w in txt if w not in stop_words]).map(lambda txt: [w for w in txt if len(w) > 2 and len(w) < 17]).map(lambda txt: [WordNetLemmatizer().lemmatize(w) for w in txt])
#sc.parallelize(data_remove_null).map(lambda line: re.split(' ', line[0]))
#.filter(lambda word: word.lower().isalpha())
#.filter(lambda word: word.lower() not in stop_words).filter(lambda word: len(word) > 2).filter(lambda word: len(word) < 17)

# word count
word_count = word_filter.flatMap(lambda x: x).map(lambda word: (word.lower(), 1)).reduceByKey(lambda v1, v2: v1 + v2).map(lambda x: (x[1], x[0])).sortByKey(ascending = False)
word_count.coalesce(1, shuffle = True).saveAsTextFile("wordCount")

#Named entity extraction

# remove blank lines
sentences_remove_null = data.filter(lambda x: len(x[0]) > 0).collect()

def sentence_splitter(article):
    return nltk.sent_tokenize(article)

# --------------------------------------------------------------------------
# An alternative way to fix the conflict between PySpark and Spacy
# --------------------------------------------------------------------------
# Spacy isn't serializable but loading it is semi-expensive
class SpacyMagic(object):
    """
    Simple Spacy Magic to minimize loading time.
    >>> SpacyMagic.get("en")
    <spacy.en.English ...
    """
    _spacys = {}

    @classmethod
    def get(cls, lang):
        if lang not in cls._spacys:
            import spacy
            cls._spacys[lang] = spacy.load(lang)
        return cls._spacys[lang]
# --------------------------------------------------------------------------


def name_tagger(sentence):
    
    nlp = SpacyMagic.get('en_core_web_sm')
    
    ne_list = []
    doc = nlp(sentence)
    for ent in doc.ents:
        ne_list.append([ent.text, ent.label_])
    return ne_list

print "1"
sentence_list = sc.parallelize(sentences_remove_null, 1000).flatMap(lambda line: sentence_splitter(line['Sentences']))

print "2"
ne_list = sentence_list.flatMap(lambda sentence: name_tagger(sentence)).map(lambda ne: (' '.join(ne), 1)).reduceByKey(lambda v1, v2: v1 + v2).map(lambda x: (x[1], x[0])).sortByKey(ascending = False)
ne_list.coalesce(1, shuffle = True).saveAsTextFile("namedEntity")

