import json
import nltk
import gensim
import pandas
import numpy

from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

custom_stop_words = ['&', '-', 'also', 'could', 'would', 'fullscreen']


#Open JSON file
with open('fixedBigData.json') as file:
	data = json.load(file)

docs = data['articles']


#Remove noise out of Sentences 
noise = ['photos', 'SUBSCRIBE', 'Subscribe', 'More:', 'Share', 'Fullscreen']

sentences_list = ['' if any([word in doc['Sentences'] for word in noise]) else doc['Sentences'] for doc in docs]


#Remove empty documents
docs = [s for s in sentences_list if len(s) > 0]

#Create DataFrame
df = pandas.DataFrame(docs)
df.columns = ['Document']

#Remove duplicates
df = df.drop_duplicates(keep = 'first')
print(len(df))

#Working on new data frame
docs = df['Document']

docs = docs.apply(lambda t: [w.lower() for w in t.split() if w.isalpha() and w.lower() not in stop_words]).apply(lambda words: [w for w in words if w.lower() not in custom_stop_words])

#Compute TF matrix, NaNs in empty cells
TF = docs.apply(lambda bag: pandas.Series(bag).value_counts())

TF = TF.loc[:, TF.sum() > 5]
IDF = numpy.log( float(len(TF))/TF.count())
TFIDF = TF * IDF


print(TFIDF)


#Print word frequency
word_freq = TF.sum().sort_values(ascending=False)
print(word_freq[:300])

#Print the most important words
most_important_words = TFIDF.sum().sort_values(ascending=False)
print(most_important_words[:300])

#Create DataFrame
words_df = pandas.DataFrame(most_important_words[300])
words_df.columns = ['Words', 'TF-IDF']


words_df.to_csv("output.csv")

#sentences = (' ').join(docs)

#Split words and remove stopwords
#words = sentences.split(' ')
#print(len(words))


#Remove stopwords
#words_filter  = [w.lower() for w in words if w.lower() not in stop_words]
#words_filter = [w.lower() for w in words_filter if w.lower() not in custom_stop_words]
#words_filter = [WordNetLemmatizer().lemmatize(w) for w in words_filter]

#print(words[0])
#print(len(words_filter))

#Frequency Words 
#freq = nltk.FreqDist(words_filter)
#most_freq = freq.most_common(500)
#most_freq_words = [w for (w, f) in most_freq]
#print(most_freq_words)

