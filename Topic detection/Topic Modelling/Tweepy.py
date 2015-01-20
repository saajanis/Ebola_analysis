import tweepy

# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)

API_KEY = "Q1U7mTxPFWwKBQhkjtua3g"
API_SECRET = "GIzajCDvNMCPR9xZPuIgQJUVkJk5NriA5mmC2slgA"
ACCESS_TOKEN = "390753770-sIkR0XBpXZGWrqBeN0GZMa4TvHHFjTbW1U1MAikK"
ACCESS_TOKEN_SECRET = "12ciPkWppjB44L6SeHWNXBhFhUv2KF4RJAUV3AABAk"


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q="test",since="2014-01-01",until="2014-02-01",lang="en").items():
    print tweet