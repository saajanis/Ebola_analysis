import pickle
import numpy as np


#HTMLPath = "../../HTMLDumps/HTML liberia ebola 03-23 until 03-27.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 03-27 until 04-03.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 04-03 until 04-13.html"
#HTMLPath = "../../HTMLDumps/HTML liberia ebola 04-13 until 04-23.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 10-30 until 11-10.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 11-10 until 11-20.html"
HTMLPath = "../../HTMLDumps/HTML mali ebola 11-20 until 11-30.html"
#HTMLPath = "../../HTMLDumps/HTML mali ebola 11-30 until 12-09.html"
tweet_messages = pickle.load(open(HTMLPath.replace("../../HTMLDumps", "../../Pickles").replace("/HTML", "/PICKLE").replace(".html", ".p"),"rb"))


tweet_messages = np.asarray(tweet_messages)
documents = [tweet_messages[:, 3]]


with open ("mali ebola 11-20 until 11-30.txt", "w") as f:
    for item in documents:
        for message in item: 
            if (len (message.replace("\\", "") ) >3):
                f.write("1" + "\t" + message.replace("\\", "").replace("\n", "").strip() + "\n")