import numpy as np
from sklearn import preprocessing, cluster, model_selection, svm
from sys import exit

class stockPrediction:
    def __init__(self, stockDataLoc, clusterNum=3, clusterDataLoc="data/clusterData.txt"):
        self.stockDataLoc = stockDataLoc
        self.clusterNum = clusterNum
        self.clusterDataLoc = clusterDataLoc

    def cluster(self):
        data = np.loadtxt(self.clusterDataLoc)
        cleanData = preprocessing.scale(data)
        self.kmeans = cluster.KMeans(n_clusters=self.clusterNum, random_state=11).fit(cleanData)
        groupNum = np.array(self.kmeans.labels_)
        return groupNum

    def clusterStockPrice(self):
        self.group, self.label = [], []
        groupNum = self.cluster()
        data = np.loadtxt(self.stockDataLoc)
        for i in range(self.clusterNum):
            self.group.append(data[groupNum==i, :-1])
            self.label.append(data[groupNum==i, -1])
        return (self.group, self.label)

    def trainTestSplit(self):
        self.train, self.trainLabel = [], []
        self.test, self.testLabel = [], []
        for i in range(self.clusterNum):
            train, test, trainLabel, testLabel = model_selection.train_test_split(self.group[i],
                    self.label[i], test_size=0.2, random_state=11)
            self.train.append(train)
            self.test.append(test)
            self.trainLabel.append(trainLabel)
            self.testLabel.append(testLabel)
        return (self.train, self.test, self.trainLabel, self.testLabel)
            
    def train(self):
        self.clusterStockPrice()
        self.trainTestSplit()
        self.clf = [svm.SVC() for i in range(self.clusterNum)]
        for i in range(self.clusterNum):
            self.clf[i].fit(self.train[i], self.trainLabel[i])
        return self.clf

    def test(self):
        self.train()
        self.error = []
        for i in range(self.clusterNum):
            pred = (self.clf[i].predict(self.test[i]) == 1)
            error = sum([i != j for (i,j) in zip(self.testLabel[i], pred)])
            self.error.append(error/len(pred))
            print "test size is"
            print len(pred)
        return self.error

    def reportResult(self):
        self.test()
        for i in range(self.clusterNum):
            print "group NO." + str(i+1) + " error rate"
            print self.error[i].mean()
        return self.error





            
if __name__ == "__main__":

    # for the case when cluster = 3
    apple = stockPrediction("data/appleTrainData.txt")
    apple.reportResult()
        
    # Case when 2 clusters
    apple = stockPrediction("data/appleTrainData.txt")
    apple.reportResult()
       
    # Case when 4 clusters
    apple = stockPrediction("data/appleTrainData.txt")
    apple.reportResult()


    
    # for the case when cluster = 3
    att = stockPrediction("data/attTrainData.txt")
    att.reportResult()
        
    # Case when 2 clusters
    att = stockPrediction("data/attTrainData.txt")
    att.reportResult()
       
    # Case when 4 clusters
    att = stockPrediction("data/attTrainData.txt")
    att.reportResult()
