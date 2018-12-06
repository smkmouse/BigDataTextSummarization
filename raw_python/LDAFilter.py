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

json = json.loads(open('fixedBigData.json').read())
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
print("How many topics to make model for?")
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

pprint(lda_model_best.print_topics())

#input which topics to keep:
keeptopics = range(0, best_topics)
for i in range(0, best_topics):
    keeptopics[i] = raw_input("Keep topic " +str(i) + "? (1 yes, 0 no) ")

strong_matthew_ids = []
for i in range(0 , len(corpus)):
    for (topic, strength) in lda_model_best[corpus[i]][0]:
        if (topic in [index(keep) for keep in keeptopics if keep == '1']) and strength > 0.3:
            strong_matthew_ids.append(i)
f = open("/share_dir/lda_filtered_docs_big_03.json","w")
for index in strong_matthew_ids:
    f.write("{\"URL\":\""+ filtered_id_list[index] + "\",\"Timestamp\":\"000000000000\",\"Sentences\":\"" + filtered_text_list[index] + "\"}\n")
