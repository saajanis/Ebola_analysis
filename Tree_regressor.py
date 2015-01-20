from crossValidation import CrossValidation

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.utils import column_or_1d
import numpy as np
import operator
import matplotlib.pyplot as plt


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

with open ("Location_Keyword_Pattern.txt", "rb") as f:
    lines = [word.strip() for word in f]

infn_lines = [] 
labelled_data = []  
for group in chunker(lines, 5):
    infn_lines.append( [group[1].split("\t")[0], group[1].split("\t")[1], group[2], group[3].split("\t")[0], group[3].split("\t")[1], group[3].split("\t")[2], group[4].split("\t")[0], group[4].split("\t")[1], group[4].split("\t")[2]] )
    
X = []
Y = []   
for infn_line in  infn_lines:
    
    labelled_data.append( [infn_line[0] ,  str(infn_line[3])+ "|" + str(infn_line[4])+ "|" + str(infn_line[5])  ])
  
 
 
CrossValidation = CrossValidation() 
##################
averageTP = 0
averageFP = 0

averageAccuracy = 0

 
RESOLUTION = 2.6
NUM_SPLITS = 10
 
np.random.shuffle(labelled_data)
 
for line in labelled_data:
    print line
ResultSet = CrossValidation.get9010Splits( labelled_data, NUM_SPLITS)

 
for splits9010Instance in ResultSet:
     
    labelledMessageArrayTrain = np.asarray(splits9010Instance[0])
    labelledMessageArray10PercentTest = np.asarray(splits9010Instance[1])
     
    #print labelledMessageArrayTrain
    #print labelledMessageArray10PercentTest
  
    X_train = np.asarray([x[1].split("|") for x in labelledMessageArrayTrain], dtype=float)
    Y_train = np.asarray([x[0] for x in labelledMessageArrayTrain], dtype=float)
 
    X_test = np.asarray([x[1].split("|") for x in labelledMessageArray10PercentTest], dtype=float)
    Y_test = np.asarray([x[0] for x in labelledMessageArray10PercentTest], dtype=float)
 
    est = GradientBoostingRegressor (n_estimators=2000, max_depth=1).fit(X_train,Y_train)
    
    Y_results = []
    for x in X_test.tolist():
        Y_results.append( est.predict (np.array(x)) )
    
    truth = Y_test
    results = Y_results
    
    TrueFalsePositives = CrossValidation.getTrueFalsePositives(results, truth, RESOLUTION)

    TP = TrueFalsePositives[0]
    FP = TrueFalsePositives [1]
    
    
    
    print "Truth: " + str(truth)       
    print "Final result: " + str(results)
    print "True positives: " + str(TP)
    print "False positives: " + str(FP)
    
    print "Accuracy: " + str(CrossValidation.getAccuracy(TP, FP) * 100) + "%"
    
     
     
     
    averageTP += TP
    averageFP += FP
    
    averageAccuracy += CrossValidation.getAccuracy(TP, FP)
      
    #break
    
print "\n\nAverage Correct: " + str(averageTP/NUM_SPLITS)  
print "Average Incorrect: " + str(averageFP/NUM_SPLITS)  
print "Average Accuracy: " + str( (averageAccuracy/NUM_SPLITS) * 100) + "%"  

##################

# test_score = np.empty(len (est.estimators_))
# for i, pred in enumerate (est.staged_predict(X)):
#     test_score[i] = est.loss_(Y, pred)
# plt.plot (np.arange(2000) + 1, test_score, label='Test')
# plt.plot (np.arange(2000) + 1, est.train_score_, label='Train')
    

plt.show()



