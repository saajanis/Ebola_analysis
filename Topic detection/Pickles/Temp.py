import pickle
import numpy as np

tweet_messages = pickle.load(open("ebola sierra leone since 2014-01-01 until 2014-04-30 - Twitter Search.p","rb"))
tweet_messages = np.asarray(tweet_messages)

print tweet_messages

write_messages = tweet_messages[:, 3]

with open ("testing.txt", "w") as f:
    for message in write_messages:
        f.write(str(message) + "\n")
    
    