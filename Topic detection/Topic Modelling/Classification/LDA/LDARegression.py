from crossValidation import *

from sklearn.ensemble import GradientBoostingRegressor
import csv
import numpy as np
import ast

with open ("MaliDump.csv", "rb") as CSVfile:
     TweetAnnotation = csv.reader(CSVfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
     
     TweetAnnotation = list(TweetAnnotation)
     numLines = len(TweetAnnotation)
     print numLines
     RegressionArray = np.zeros((numLines, 50))
     
     x=0
     for line in TweetAnnotation:
         if(x==0): 
             x+=1
             continue##skip 1st details line
         i=2
         print line
        
         while (i<=(len(line)-2)):
             RegressionArray[int(line[0])-1,    int(line[i])-1] = line[i+1]
             i+=2
         
      
#      for line in RegressionArray: 
#          print line

     targetLabels = []
     with open ("Mali Combined.txt", "r") as f:
        for line in f.readlines():
            targetLabels.append(line.split()[0])
            
    
     #targetLabels += [1,1,1,1,1,1,1,1]    
     print targetLabels
     targetLabels = np.asarray(targetLabels)
     print RegressionArray.shape
     print targetLabels.shape
     CrossValidation = CrossValidation() 
      
     labelledRegressionArray = [] 
     for i in range(targetLabels.shape[0])  :
          labelledRegressionArray.append([targetLabels[i], (str(list(RegressionArray[i])))])
         
     averageTP = 0
     averageFP = 0
     averageTN = 0
     averageFN = 0
     averageAccuracy = 0
     averagePrecision = 0
     averageRecall = 0
     
     
     np.random.shuffle(labelledRegressionArray)
     for line in labelledRegressionArray:
         print line
     ResultSet = CrossValidation.get9010Splits( labelledRegressionArray)


     for splits9010Instance in ResultSet:
        
        labelledMessageArrayTrain = np.asarray(splits9010Instance[0])
        labelledMessageArray10PercentTest = np.asarray(splits9010Instance[1])
        
        
        trainingLabels = np.asarray(labelledMessageArrayTrain[:, 0], dtype=int )
        trainingMessages =  np.asarray(labelledMessageArrayTrain[:, 1] )
        
        trainingMessages2 = []
        for message in trainingMessages:
            trainingMessages2.append (ast.literal_eval(message))
        trainingMessages2 = np.asarray(trainingMessages2, dtype=float)
        
        classifier = GradientBoostingRegressor (n_estimators=2000, max_depth=1).fit(trainingMessages2,trainingLabels)
        
        testingLabels = np.asanyarray(labelledMessageArray10PercentTest[:, 0], dtype=int)
        testingMessages =  np.asarray( labelledMessageArray10PercentTest[:, 1] )
        testingMessages2 = []
        for message in testingMessages:
            testingMessages2.append (ast.literal_eval(message))
        testingMessages2 = np.asarray(testingMessages2, dtype=float)
        
        
        truth = testingLabels
        result = []
        
        
        for test_msg in testingMessages2:
            print test_msg
            
            prediction = classifier.predict(np.array(test_msg))
            print prediction
            result.append(int( round(prediction[0])) )   
         
        result = np.asarray(result, dtype=int)
        
        TrueFalsePositives = CrossValidation.getTrueFalsePositives(result, truth)
        TrueFalseNegatives = CrossValidation.getTrueFalseNegatives(result, truth)
        TP = TrueFalsePositives[0]
        FP = TrueFalsePositives [1]
        TN = TrueFalseNegatives[0]
        FN = TrueFalseNegatives[1]
        
        
        print "Truth: " + str(truth)       
        print "Final result: " + str(result)
        print "True positives: " + str(TP)
        print "False positives: " + str(FP)
        print "True Negatives: " + str(TN)
        print "False Negatives: " + str(FN)
        print "Accuracy: " + str(CrossValidation.getAccuracy(TP, FP, TN, FN) * 100) + "%"
        print "Precision: " + str(CrossValidation.getPrecision(TP, FP, TN, FN) * 100) + "%"
        print "Recall: " + str(CrossValidation.getRecall(TP, FP, TN, FN) * 100) + "%"
         
         
         
         
        averageTP += TP
        averageFP += FP
        averageTN += TN
        averageFN += FN
        averageAccuracy += CrossValidation.getAccuracy(TP, FP, TN, FN)
        averagePrecision += CrossValidation.getPrecision(TP, FP, TN, FN)
        averageRecall += CrossValidation.getRecall(TP, FP, TN, FN)     
        #break
        
     print "\n\nAverage True Positives: " + str(averageTP/10)  
     print "Average False positives: " + str(averageFP/10)  
     print "Average True Negatives: " + str(averageTN/10)  
     print "Average False Negatives: " + str(averageFN/10)  
     print "Average Accuracy: " + str( (averageAccuracy/10) * 100) + "%"  
     print "Average Precision: " + str( (averagePrecision/10) * 100) + "%"
     print "Average Recall: " + str( (averageRecall/10)   * 100) + "%"  
    
     ##################
