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
best_coh_score = 0
best_topics = 0
for i in range(8,30):
    lda_model_loop = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=i, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=20,
                                           alpha='auto',
                                           per_word_topics=True)
    coherence_model_lda = CoherenceModel(model = lda_model_loop, texts = texts, dictionary = id2word, coherence = 'c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    if coherence_lda > best_coh_score:
        best_coh_score = coherence_lda
        best_topics = i
    print('Topics:',i)
    print('Conherence score: ', coherence_lda)
print(best_coh_score)
print(best_topics)
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
