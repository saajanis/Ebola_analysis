from bs4 import BeautifulSoup
import requests
import os
import operator
from datetime import datetime
import pickle

# html_doc = requests.get('https://twitter.com/search?q=ebola%20sierra%20leone%20since%3A2014-01-01%20until%3A2014-04-30&src=typd')
# html_doc = html_doc.text
        
html_doc = open ("HTMLDumps/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.html", "rb") 
soup = BeautifulSoup(html_doc)
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
        #break
        #print "----------------\n\n\n\n\n\n\n\n\n"

print len(tweetData)

#pickle.load(open("TransformedTweetsArray.p","rb"))
pickle.dump(tweetData,open("Pickles/ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","wb"))

