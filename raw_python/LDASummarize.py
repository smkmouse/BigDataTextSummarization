import json
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
from pprint import pprint

stop_words = stopwords.words('english')

json = json.loads(open('lda_filtered_docs_big_fixed.json').read())
articles = json['articles']
fulltextstringlist = [doc['Sentences'] for doc in articles]
fullidstringlist = [doc['URL'] for doc in articles]
fulltextstringlist = list(filter(lambda x: x != None, fulltextstringlist))
fullidstringlist = list(filter(lambda x: x != None, fullidstringlist))

filtered_text_list = []
filtered_id_list = []
dupe_check = {}

for i in range(0,len(fulltextstringlist)):
    if len(fulltextstringlist[i])>0 and not fulltextstringlist[i] in dupe_check:
        filtered_text_list.append(fulltextstringlist[i])
        filtered_id_list.append(fullidstringlist[i])
        dupe_check[fulltextstringlist[i]] = "Duplicate"

clean_text_list = []        
for i in range(0,len(filtered_text_list)):
    clean_text_list.append([WordNetLemmatizer().lemmatize(w.lower()) for w in nltk.word_tokenize(filtered_text_list[i]) if w.lower().isalpha() and w.lower() not in stop_words and len(w.lower())>2 and len(w.lower())<17])

id2word = corpora.Dictionary(clean_text_list)
texts = clean_text_list
corpus = [id2word.doc2bow(text) for text in texts]

#input number of topics:
print("How many topics to make summary for?")
best_topics = raw_input('Enter your input:')
best_topics = int(best_topics)

lda_model_best = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=best_topics, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=20,
                                           alpha='auto',
                                           per_word_topics=True)

filtered_sentence_list = [nltk.sent_tokenize(text) for text in filtered_text_list]
filtered_sentence_list = [item for doc in filtered_sentence_list for item in doc]
bestsent = {}
bestscore = {}
for i in range(0,17):
    bestsent[i] = ""
    bestscore[i] = 0
for sent in filtered_sentence_list:
    cleandoc = [WordNetLemmatizer().lemmatize(w.lower()) for w in nltk.word_tokenize(sent) if w.lower().isalpha() and w.lower() not in stop_words and len(w.lower())>2 and len(w.lower())<17]
    if len(cleandoc) > 4 and len(cleandoc) < 26:
        bowdoc = id2word.doc2bow(cleandoc)
        for (x,y) in lda_model_17[bowdoc][0]:
            if y > bestscore[x]:
                bestscore[x] = y
                bestsent[x] = sent

for i in range(0,int(best_topics)):
    print(bestsent[i])
