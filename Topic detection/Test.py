


with open ("Tweets_sorted_by_location.txt", "rb") as f:
    i=0
    for line in f:
        i+=1 
        
        if (len(line.split("|")) ==10):
            print line.split("|")[2]
        
        if (i>100):
            break