import numpy as np
from sklearn import preprocessing, cluster, model_selection, svm
from classifier import Classifier

# Object that for svm with clustering 
class svmStockPred(Classifier):
    def __init__(self, microDataLoc, clusterNum=1, macroDataLoc="data/clusterData.txt"):
        Classifier.__init__(self, microDataLoc, clusterNum=1, macroDataLoc="data/clusterData.txt")

    def train(self):
        train, test, trainLabel, testLabel = self.trainTestSplit()
        clf = [svm.SVC() for i in range(self.clusterNum)]
        cvScore = []
        for i in range(self.clusterNum):
            score = model_selection.cross_val_score(clf[i], train[i], trainLabel[i], cv = 10) 
            cvScore.append(score.mean()) 
        for i in range(self.clusterNum):
            clf[i].fit(train[i], trainLabel[i])
        return (clf, test, testLabel, cvScore) # return test and testLabel to self.test() so no need to
                                      # recompute the testing data again


# StockPredNoClassification class is a class to classify the stock price direction 
# without using clustering. The macro data used for clustering now was combined with
# micro data for classification
class svmNoCluster(svmStockPred):
    def __init__(self, microDataLoc):
        svmStockPred.__init__(self, microDataLoc)

    def prepareData(self):
        group, label = [], []
        microData = np.loadtxt(self.microDataLoc)
        macroData = np.loadtxt(self.macroDataLoc)
        data = np.concatenate((macroData, microData), axis=1)
        for i in range(self.clusterNum):
            group.append(data[: , :-1])
            label.append(data[: , -1])
        return (group, label)

    def reportResult(self):
        error, cv = self.test()
        print "the cross validation error is " 
        print cv
        print "Without Clustering, the correct classification rate is"
        print 1-error[0]
        print '\n'
        return error

            
if __name__ == "__main__":

    # without clustering
    apple = svmNoCluster("data/appleTrainData.txt")
    apple.reportResult()

    # for the case when cluster = 3
    apple = svmStockPred("data/appleTrainData.txt", clusterNum=3)
    apple.reportResult()
        
    # Case when 2 clusters
    apple = svmStockPred("data/appleTrainData.txt", clusterNum=2)
    apple.reportResult()
       
    # Case when 4 clusters
    apple = svmStockPred("data/appleTrainData.txt", clusterNum=4)
    apple.reportResult()

    # Case when 1 cluster
    apple = svmStockPred("data/appleTrainData.txt", clusterNum=1)
    apple.reportResult()


    
    # without clustering
    att = svmStockPred("data/attTrainData.txt")
    att.reportResult()

    # for the case when cluster = 3
    att = svmStockPred("data/attTrainData.txt", clusterNum=3)
    att.reportResult()
        
    # Case when 2 clusters
    att = svmStockPred("data/attTrainData.txt", clusterNum=2)
    att.reportResult()
       
    # Case when 4 clusters
    att = svmStockPred("data/attTrainData.txt", clusterNum=4)
    att.reportResult()

    # Case when 1 cluster
    att = svmStockPred("data/attTrainData.txt", clusterNum=1)
    att.reportResult()
