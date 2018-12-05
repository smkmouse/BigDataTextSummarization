import json
import nltk
import pandas
from gensim.summarization.summarizer import summarize
from nltk import sent_tokenize 
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')
custom_stop_words = ['&', '-', ':', 'also', 'could', 'fullscreen', 'photos:', 'reddit', 'subscribe', 'share', 'reserved', 'copyright', 'twitter', 'facebook']

#Open JSON file
with open('fixedBigData.json') as file:
        data = json.load(file)

docs = data['articles']


#Remove noise out of Sentences
noise = ['hurricane-irma', 'hurricane-maria']

sentences_list = ['' if any([word in doc['URL'] for word in noise]) else doc['Sentences'] for doc in docs]


#Remove empty documents
docs = [s for s in sentences_list if len(s) > 0]

#Create DataFrame
df = pandas.DataFrame(docs)
df.columns = ['Document']
df = df.drop_duplicates(keep = 'first')
print(len(df))

#clean data for each document
def clean_each_doc(doc):
	
	#tokenize the document
	sentences = sent_tokenize(doc)
	sents = ['' if any([w for w in sent.split() if w.lower() in custom_stop_words]) else sent for sent in sentences]

	#Remove sentences that having less than 3 words or greater than 21 words
	sents = [s for s in sents if len(s.split(' ')) > 5]
	sents = [s for s in sents if len(s.split(' ')) < 26]
	
	article = (' ').join(sents) 

	return article

clean_doc = [clean_each_doc(doc) for doc in docs]
print(len(sent_tokenize(clean_doc[0])))

clean_doc = [doc for doc in clean_doc if len(sent_tokenize(doc)) > 2]
print('Lenght docs after remove 3: ', len(clean_doc))

#df = pandas.DataFrame(clean_doc)
#df.to_csv("clean_doc.csv", index = False, header = False)

# Remove irrelevant documents
#freq_words = set(open("hurricane.txt").read().splitlines())

freq_words = ['hurricane', 'storm']
relevant_docs = [doc if any([w for w in doc.split() if w.lower() in freq_words]) else '' for doc in clean_doc]
relevant_docs = [doc for doc in relevant_docs if len(doc) > 0]

df = pandas.DataFrame(relevant_docs)
df = df.drop_duplicates(keep = 'first')

print('relevant len', len(df))
df.to_csv("relevant_docs.csv", header = False)

print(len(relevant_docs))


#print(relevant_docs[:10]) 

#start = 0		
#i = 300
#count = 1 
#while i <= len(docs):
#	doc10 = (' ').join(relevant_docs[start: i])
#	summary = summarize(doc10, word_count = 300)
#	df = pandas.DataFrame(summary)
#	filename = "summary" + count + ".csv" 
#	df.to_csv(filename, index = False, header = False)
#	print(summary)
	
#	start = i 
#	temp = i + 300
#	if temp < len(docs):
#		i = temp
#	else:
#		i = len(docs)
	
#	count = count + 1

doc10 = (' ').join(relevant_docs[3600: len(relevant_docs)])
summary = summarize(doc10, word_count = 300)
print(summary)
