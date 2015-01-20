from crossValidation import CrossValidation

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn import svm
from sklearn.utils import column_or_1d
import numpy as np
import operator
import matplotlib.pyplot as plt
import math


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

with open ("Using_in_keyword_RT_SP2.txt", "rb") as f:
    lines = [word.strip() for word in f]
    

infn_lines = [] 
labelled_data = []  
for group in chunker(lines, 5):
    infn_lines.append( [group[1].split("\t")[0], group[1].split("\t")[3], group[2], group[3].split("\t")[0], group[3].split("\t")[1], group[3].split("\t")[2], group[3].split("\t")[3], group[4].split("\t")[0], group[4].split("\t")[1], group[4].split("\t")[2], group[4].split("\t")[3]] )
    
X = []
Y = []   
for infn_line in  infn_lines:
    
    labelled_data.append( [infn_line[0] ,infn_line[1],  str(infn_line[2])+ "|" + str(infn_line[3])+ "|" + str(infn_line[4])+ "|" + str(infn_line[5])+ "|" + str(infn_line[6])  ])
print "labelled data: " + str(labelled_data  )
#####MAKE Changes here 
 
CrossValidation = CrossValidation() 
NUM_SPLITS = 19
THRESHOLD = 2.0
X = []
Y = [] 
prediction_counter = []

########

# labelled_data = np.asarray(labelled_data)
# print labelled_data[:, 0]
# labels = np.asarray(labelled_data[:, 0], dtype=float)
# SD = np.std(labels)
# MEAN = np.mean (labels)
# 
# print [x for x in labels]
# normalized_labels = [math.log10(x+1) for x in labels]
# 
# for i in range(len(normalized_labels)):
#     labelled_data[i][0] = normalized_labels[i]
# 

labelled_data = np.asarray(labelled_data)
labels = np.asarray(labelled_data[:, 0], dtype=float)
MIN = math.log(np.min(labels) +1 )
MAX = math.log(np.max(labels) +1 )
print [x for x in labels]
 
normalized_labels = [( ((10-0)*(math.log(x+1)-MIN)/(MAX-MIN) ) + 0 ) for x in labels]
print normalized_labels
 
for i in range(len(normalized_labels)):
    labelled_data[i][0] = normalized_labels[i]

########


ResultSet = CrossValidation.get9010Splits( labelled_data, NUM_SPLITS)


   
for x in range(len(ResultSet)-1):
    
    splits33_1Instance = ResultSet[x]
    labelledMessageArray33PartTrain = np.asarray(splits33_1Instance[0])
    labelledMessageArray1PartTest = np.asarray(splits33_1Instance[1])

    #print labelledMessageArray1PartTest[0]
    
    X_train = np.asarray([x[2].split("|") for x in labelledMessageArray33PartTrain], dtype=float)
    Y_train = np.asarray([x[0] for x in labelledMessageArray33PartTrain], dtype=float)
 
    X_test = np.asarray([x[2].split("|") for x in labelledMessageArray1PartTest], dtype=float)
    Y_test = np.asarray([x[0] for x in labelledMessageArray1PartTest], dtype=float)
    
    #'''gradient boosting
    classifier = GradientBoostingRegressor (n_estimators=2000, max_depth=1).fit(X_train,Y_train)
    #'''
    
    
    Y_results = []
    for x in X_test.tolist():
        Y_results.append( classifier.predict (np.array(x)) )
        
    truth = Y_test
    results = Y_results
    
    if (len(labelledMessageArray1PartTest)==0):
        continue
    #print labelledMessageArray1PartTest
    print "Location: " + str(labelledMessageArray1PartTest[0][1]) + " | Truth: " + str(truth) + " | Result: " + str(results) + " | Difference: " + str(math.fabs(results-truth)) 
    
    if ( math.fabs(results-truth)<= THRESHOLD ):
        prediction_counter.append(1)
    else:
        prediction_counter.append(0)
        
print prediction_counter
count=0
for x in prediction_counter:
    if (x==1):
        count+=1
        
print count
total = len(prediction_counter)
print total
print "Percentage: " + str ( (float(count)/float(total))*100 )