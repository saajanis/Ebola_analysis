import nltk
import nltk.tokenize as tokenize
from textblob import TextBlob

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



print createChunk("Saajan shridhar is going to fly towards california.")