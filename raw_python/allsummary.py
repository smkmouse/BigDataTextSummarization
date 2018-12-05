#from gensim.summarization.summarizer import summarize
from summa import summarizer

data = open("bigsummary.txt").read().splitlines()

data = (' ').join(data)
#print(data)

summary = summarizer.summarize(data, words = 200, scores = True)
sorted_summary = sorted(summary, key = lambda x: x[1], reverse = True)

print(sorted_summary)
