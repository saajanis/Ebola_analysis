import pickle
import numpy as np

from textblob import TextBlob
import gensim
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from gensim.parsing.preprocessing import STOPWORDS
import nltk
import nltk.tokenize as tokenize

from itertools import izip
import itertools
from collections import Counter


#################################
def split_words(text, stopwords=STOPWORDS):
        """
        Break text into a list of single words. Ignore any token that falls into
        the `stopwords` set.

        """
        return [word
                for word in gensim.utils.tokenize(text, lower=True)
                if word not in STOPWORDS and len(word) > 3]

def createChunk (sentence_string):
    blob = TextBlob(sentence_string)
    tagged_sentence_dict = blob.tags
    final_string = []
    last_tag = ''
    string_so_far = ''
    for item in tagged_sentence_dict:
        word = item[0]
        tag = item[1][:2]
        print word
        print tag
        if (tag==last_tag):
            string_so_far+= " " + word
        else:
            if (string_so_far!=''):
                final_string.append(string_so_far.strip())
            string_so_far = word
        
            
        
        last_word = word
        last_tag=tag
    return final_string  
        

#################################

tweet_messages = pickle.load(open("../Pickles/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","rb"))
tweet_messages = np.asarray(tweet_messages)

documents = [tweet_messages[:, 3][0]]


texts = [ createChunk(" ".join([word.strip("\\") for word in split_words(document.lower()) if word not in STOPWORDS]) )
         for document in documents]
print texts

'''
texts = sum(texts, [])
totalString = ""
for word in texts:
    totalString+= " " + word   
print totalString

print Counter(totalString.split()).most_common()
'''



# monty = TextBlob(totalString)
# 
# print monty.word_counts['sierra']

# dictionary = corpora.Dictionary(texts)
# corpus = [dictionary.doc2bow(text) for text in texts]
# 
# print corpus
# print dictionary
# 
# # I can print out the topics for LSA
# tfidf = models.TfidfModel(corpus)
# corpus_tfidf = tfidf[corpus]
# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
# corpus_lsi = lsi[corpus]
# 
# for l,t in izip(corpus_lsi,corpus):
#   print l,"#",t
# print
# for top in lsi.print_topics(2):
#   print top
# 
# # I can print out the documents and which is the most probable topics for each doc.
# lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=50)
# corpus_lda = lda[corpus]
# 
# for l,t in izip(corpus_lda,corpus):
#   print l,"#",t
# print
# print "################"
# 
# # But I am unable to print out the topics, how should i do it?
# # for top in lda.show_topics():
# #   print top
# 
# for i in range(0, lda.num_topics-1):
#     print lda.print_topic(i)