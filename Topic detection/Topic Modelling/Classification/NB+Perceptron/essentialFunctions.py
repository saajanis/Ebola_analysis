from collections import OrderedDict

from topia.termextract import extract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from textblob import TextBlob
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
import enchant
english_dict = enchant.Dict("en_US")


from bs4 import BeautifulSoup
import requests
import os
import operator
from datetime import datetime
import pickle

###########################

def cleanTweet (string):
    string = strip_non_ascii(string) 
    string = removeHashTags(string)
    string = removeStopWords (string)
    string = returnNounsVerbsIn(string)
    string = removeCommonWords(string)
    string = lemmatize(string)
    #string = removeNonEnglish(string)
    string = checkLengthandCase(string)
    
    return string




###########################
def removeHashTags(sentence_string):
    returnString = " ".join([word.lower().replace("#", "") for word in sentence_string.split() if len(word)>2])
    
    return returnString

def checkLengthandCase(sentence_string):
    returnString = " ".join([word.lower() for word in sentence_string.split() if len(word)>2])
    
    return returnString

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)
stopset = set(stopwords.words('english'))

def removeStopWords(input):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens=tokenizer.tokenize(input)
    tokens = [w for w in tokens if not w in STOPWORDS]
    returnString= ' '.join(tokens)
    returnString = ' '.join(OrderedDict((w,w) for w in returnString.split()).keys())
    return returnString

def returnNounsVerbsIn (sentence_string):
    blob = TextBlob(sentence_string)
    tagged_sentence_dict = blob.tags
    final_string = ""
    last_tag = ''
    string_so_far = ''
    for item in tagged_sentence_dict:
        word = item[0]
        tag = item[1][:2]
        if (tag=="NN" or tag=="VB" or tag=="IN"):
        #if (tag=="NN" or tag=="NNP"):
            final_string+=word + " "
    return final_string 

def removeCommonWords (sentence_string):
    remove_list = ['http', 'fb', 'ly', 'com', 'bit', 'www', 'goo', 'org'
                   'sierra', 'guinea', 'liberia', 'west', 'africa', 'mali', 'suspected', 'outbreak', 'death', 'deaths', 'spread' ]
#     remove_list = ['http', 'fb', 'ly', 'com', 'bit', 'www', 'goo', 'org'
#                    'ebola', 'sierra', 'guinea', 'liberia', 'west', 'africa', 'mali', 'suspected', 'cases', 'case', 'outbreak', 'death', 'deaths', 'spread' ]
#     
    word_list = sentence_string.split()
    sentence_string = ' '.join([word for word in word_list if word.lower() not in remove_list])
    return sentence_string 

def lemmatize (sentence_string):
    wnl = WordNetLemmatizer()
    returnString = " ".join([wnl.lemmatize(i) for i in sentence_string.split()])
    return returnString

def removeNonEnglish(sentence_string):
    returnString = " ".join([word for word in sentence_string.split() if english_dict.check(word)])
    
    return returnString
######################################

def getTweetDatafromHTML(path):
    html_doc = open (path, "rb") 
    print "HTML opened"
    soup = BeautifulSoup(html_doc)
    print "soup created"
    #print(soup.prettify())

    tweetData = []
    
    for div in soup.find_all('div', {"class": "content"}):
          #if (div['class'] == "contet")
            #print div.prettify()
            for username in (div.find_all('span', {"class": "username js-action-profile-name"})):
                username_string = str(reduce(operator.add,(username.findAll(text=True))))
                #print "Username: " + username_string
            for uid in (div.find_all('a', {"class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})):
                uid_string = str(uid['data-user-id'])
                #print "User ID: " + uid_string
            for time in (div.find_all('a', {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})):
                time_string = str(time['title'])
                #print "Time found: " + str(datetime.strptime(time_string, '%I:%M %p - %d %b %Y') )
            for tweet_text in (div.find_all('p', {"class": "js-tweet-text tweet-text"})):
                tweet_text_string = str(reduce(operator.add,tweet_text.findAll(text=True)))
                #print "Tweet: " + tweet_text_string
            
                tweetData.append ([username_string, uid_string, time_string, tweet_text_string])
                print [username_string, uid_string, time_string, tweet_text_string]
            #break
            #print "----------------\n\n\n\n\n\n\n\n\n"
    
    return tweetData
