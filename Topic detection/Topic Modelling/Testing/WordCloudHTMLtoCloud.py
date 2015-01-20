from essentialFunctions import *

import pickle
import numpy as np
from collections import Counter


################################

###############essentialFunctions

#################################

#HTMLPath = "../../HTMLDumps/HTML guinea ebola 03-19 until 03-23.html"
HTMLPath = "../../HTMLDumps/HTML guinea ebola 03-24 until 03-27.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 03-23 until 03-27.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 03-27 until 04-03.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 04-03 until 04-13.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 04-13 until 04-23.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 10-30 until 11-10.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 11-10 until 11-20.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 11-20 until 11-30.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 11-30 until 12-09.html"

'''
tweet_messages = getTweetDatafromHTML(HTMLPath)
pickle.dump(tweet_messages,open(HTMLPath.replace("../../HTMLDumps", "../../Pickles").replace("/HTML", "/PICKLE").replace(".html", ".p"),"wb"))
'''

tweet_messages = pickle.load(open(HTMLPath.replace("../../HTMLDumps", "../../Pickles").replace("/HTML", "/PICKLE").replace(".html", ".p"),"rb"))


for tweet in tweet_messages:
    print tweet
print len(tweet_messages)

tweet_messages = np.asarray(tweet_messages)


documents = [tweet_messages[:, 3]]
#documents = np.take(documents, [i for i in range(25)])

tweet_list = []
for item in documents:
    for message in item:       
        tweet_list.append (cleanTweet (message))    
    

text = ' '.join(tweet_list)
print text
print Counter(text.split()).most_common()



with open ("testing.txt", "w") as f:
    f.write (text)
         


'''
# with open("temp.txt", "w") as f:
#     f.write(text)
# 
# 
# #print TextBlob(text).noun_phrases
# 
# ###############################
# #text = "saajan shridhar is going to california"
#  
# extractor = extract.TermExtractor()
# print sorted(extractor(text))
'''
   
   
    
#######CREATE CLOUD WITH http://www.wordle.net/