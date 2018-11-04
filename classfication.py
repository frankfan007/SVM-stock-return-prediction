import numpy as np
from sklearn import preprocessing, cluster, model_selection, svm


clusterData = np.loadtxt('data/clusterData.txt')
cleanData = preprocessing.scale(clusterData)

kmeans = cluster.KMeans(n_clusters=4, random_state=11).fit(cleanData)

labels = np.array(kmeans.labels_)

appleData = np.loadtxt('data/appleTrainData.txt') 
group1 = appleData[labels==0, :-1]
result1 = appleData[labels==0, -1]
group2 = appleData[labels==1, :-1]
result2 = appleData[labels==1, -1]
group3 = appleData[labels==2, :-1]
result3 = appleData[labels==2, -1]
group4 = appleData[labels==3, :-1]
result4 = appleData[labels==3, -1]


trainRatio = 0.8

XTrain1, XTest1, yTrain1, yTest1 = model_selection.train_test_split(group1, result1,
        train_size=trainRatio, random_state=11)
XTrain2, XTest2, yTrain2, yTest2 = model_selection.train_test_split(group2, result2,
        train_size=trainRatio, random_state=11)
XTrain3, XTest3, yTrain3, yTest3 = model_selection.train_test_split(group3, result3,
        train_size=trainRatio, random_state=11)
XTrain4, XTest4, yTrain4, yTest4 = model_selection.train_test_split(group4, result4,
        train_size=trainRatio, random_state=11)

print np.size(yTrain1)
print np.size(yTrain2)
print np.size(yTrain3)
print np.size(yTrain4)
clf = [svm.SVC(C=0.7) for i in range(4)]
clf[0].fit(XTrain1, yTrain1)
clf[1].fit(XTrain2, yTrain2)
clf[2].fit(XTrain3, yTrain3)
clf[3].fit(XTrain4, yTrain4)

predict1 = clf[0].predict(XTest1)
predict2 = clf[1].predict(XTest2)
predict3 = clf[2].predict(XTest3)
predict4 = clf[3].predict(XTest4)

error1 = sum([i!=j for i,j in zip(predict1, yTest1)])/float(np.size(yTest1))
error2 = sum([i!=j for i,j in zip(predict2, yTest2)])/float(np.size(yTest2))
error3 = sum([i!=j for i,j in zip(predict3, yTest3)])/float(np.size(yTest3))
error4 = sum([i!=j for i,j in zip(predict4, yTest4)])/float(np.size(yTest4))

print error1
print error2
print error3
print error4

print '\n'
trainPred3 = clf[2].predict(XTrain3)
trainPred1 = clf[0].predict(XTrain1)
trainPred2 = clf[1].predict(XTrain2)
trainPred4 = clf[3].predict(XTrain4)
print sum([i!=j for i,j in zip(trainPred1, yTrain1)])/float(np.size(yTrain1))
print sum([i!=j for i,j in zip(trainPred2, yTrain2)])/float(np.size(yTrain2))
print sum([i!=j for i,j in zip(trainPred3, yTrain3)])/float(np.size(yTrain3))
print sum([i!=j for i,j in zip(trainPred4, yTrain4)])/float(np.size(yTrain4))
