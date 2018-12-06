import json
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
from collections import Counter
import operator

stop_words = stopwords.words('english')
customStopwords = {'news', 'mobile', 'app', 'search', 'iphone', 'apps', 'email', 'var', 'function', 'true', 'false', 'terms', 'service', 'privacy', 'policy', 'contact', 'copyright', 'fullscreen', 'gnewswp', 'return'}


json = json.loads(open('lda_filtered_docs_big_fixed.json').read())
articles = json['articles']
fulltextstringlist = [doc['Sentences'] for doc in articles]
fullidstringlist = [doc['URL'] for doc in articles]
fulltextstringlist = list(filter(lambda x: x != None, fulltextstringlist))
fullidstringlist = list(filter(lambda x: x != None, fullidstringlist))

pos_tagged_list = [nltk.pos_tag(nltk.word_tokenize(doc)) for doc in fulltextstringlist]
pos_tagged_full = [item for doc in pos_tagged_list for item in doc]

pos_noun_string_list = [WordNetLemmatizer().lemmatize(w.lower())+" "+y for (w,y) in pos_tagged_full if y[0] == "N" and w.lower() not in stop_words and w.lower() not in customStopwords and w.lower().isalpha() and len(w) > 2 and len(w) < 17]
pos_verb_string_list = [WordNetLemmatizer().lemmatize(w.lower())+" "+y for (w,y) in pos_tagged_full if y[0] == "V" and w.lower() not in stop_words and w.lower() not in customStopwords and w.lower().isalpha() and len(w) > 2 and len(w) < 17]
noun_count = dict(Counter(pos_noun_string_list))


sorted_noun_count = sorted(noun_count.items(), key=operator.itemgetter(1))
sorted_noun_count.reverse()


verb_count = dict(Counter(pos_verb_string_list))


sorted_verb_count = sorted(verb_count.items(), key=operator.itemgetter(1))
sorted_verb_count.reverse()

print(sorted_verb_count[0:10])

print(sorted_noun_count[0:10])
