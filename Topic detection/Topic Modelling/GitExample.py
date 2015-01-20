# import numpy
# import scipy
# import gensim
# import textblob
# 
# print(gensim.__version__, gensim.__file__)
# print gensim.utils.lemmatize("The quick brown fox jumps over the lazy dog!")
# print textblob.TextBlob("The quick brown fox jumps over the lazy dog!").noun_phrases

import logging
import os
import sys
import re
import tarfile
import itertools
import pickle
import numpy as np
from collections import OrderedDict


import nltk
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures

import gensim
from gensim.parsing.preprocessing import STOPWORDS
from textblob import TextBlob


########################################################
stopset = set(stopwords.words('english'))
def removeStopWords(input):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens=tokenizer.tokenize(input)
    tokens = [w for w in tokens if not w in stopset]
    returnString= ' '.join(tokens)
    returnString = ' '.join(OrderedDict((w,w) for w in returnString.split()).keys())
    return returnString
    

def getTweetStream(tweet_messages):
    for message in tweet_messages[:, 3]:
        yield message
        
def lemmatizeTweets(tweet_stream):
    for tweet in tweet_stream:
        yield gensim.utils.lemmatize(removeStopWords(tweet))
########
def best_ngrams(words, top_n=1000, min_freq=1):
    """
    Extract `top_n` most salient collocations (bigrams and trigrams),
    from a stream of words. Ignore collocations with frequency
    lower than `min_freq`.

    This fnc uses NLTK for the collocation detection itself -- not very scalable!

    Return the detected ngrams as compiled regular expressions, for their faster
    detection later on.

    """
    tcf = TrigramCollocationFinder.from_words(words)
    tcf.apply_freq_filter(min_freq)
    trigrams = [' '.join(w) for w in tcf.nbest(TrigramAssocMeasures.chi_sq, top_n)]
    logging.info("%i trigrams found: %s..." % (len(trigrams), trigrams[:20]))

    bcf = tcf.bigram_finder()
    bcf.apply_freq_filter(min_freq)
    bigrams = [' '.join(w) for w in bcf.nbest(BigramAssocMeasures.pmi, top_n)]
    logging.info("%i bigrams found: %s..." % (len(bigrams), bigrams[:20]))

    pat_gram2 = re.compile('(%s)' % '|'.join(bigrams), re.UNICODE)
    pat_gram3 = re.compile('(%s)' % '|'.join(trigrams), re.UNICODE)

    return pat_gram2, pat_gram3

class Corpus20News_Collocations(object):
    def __init__(self, tweet_stream):
        self.tweet_stream = tweet_stream
        #logging.info("collecting ngrams from %s" % self.fname)
        # generator of documents; one element = list of words
        documents = (self.split_words(text) for text in self.tweet_stream)
        # generator: concatenate (chain) all words into a single sequence, lazily
        words = itertools.chain.from_iterable(documents)
        self.bigrams, self.trigrams = best_ngrams(words)
        
    def split_words(self, text, stopwords=STOPWORDS):
        """
        Break text into a list of single words. Ignore any token that falls into
        the `stopwords` set.

        """
        return [word
                for word in gensim.utils.tokenize(text, lower=True)
                if word not in STOPWORDS and len(word) > 3]

    def tokenize(self, message):
        """
        Break text (string) into a list of Unicode tokens.
        
        The resulting tokens can be longer phrases (collocations) too,
        e.g. `new_york`, `real_estate` etc.

        """
        text = u' '.join(self.split_words(message))
        text = re.sub(self.trigrams, lambda match: match.group(0).replace(u' ', u'_'), text)
        text = re.sub(self.bigrams, lambda match: match.group(0).replace(u' ', u'_'), text)
        return text.split()

    def drive(self):
        tweet_messages = pickle.load(open("../Pickles/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","rb"))
        tweet_messages = np.asarray(tweet_messages)
        #pickle.dump(tweetData,open("Pickles/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","wb"))
        tweet_stream = getTweetStream(tweet_messages);
        print "Entered"
        
        for message in tweet_stream:
            #print "printing: " + str(message)
            yield self.tokenize(message)

      
########################################################




tweet_messages = pickle.load(open("../Pickles/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","rb"))
tweet_messages = np.asarray(tweet_messages)
#pickle.dump(tweetData,open("Pickles/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","wb"))
tweet_stream = getTweetStream(tweet_messages);
#lematized_tweets_stream = lemmatizeTweets(tweet_stream)
##initialize bigrams, trigrams



collocations_corpus = Corpus20News_Collocations(tweet_stream)
print [text for text in collocations_corpus.drive()]
#print(list(itertools.islice(collocations_corpus, None)))  

'''
for lemmatized_tweet in lematized_tweets_stream:
    print lemmatized_tweet
'''    
#print list(tweet_stream)
#print tweet_messages[:, 3]
