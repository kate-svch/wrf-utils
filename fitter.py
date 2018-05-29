#!/usr/bin/env python3
import pandas as pd
import numpy as np
import datetime
import sys

from sklearn.externals import joblib
from sklearn import cross_validation
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import * 
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

#       load train data 
data=pd.read_csv('traindata.csv', index_col=0)
data=data.dropna().drop_duplicates()
data=data.reset_index(drop=True)
#       select target colomn
target=data['TGE']      
#nnlls=data['nnlls']

del data['t2']
#del data['s_wind']
del data['date']
del data['TGE']
del data['fulltime']

print(data.head())
print(target.head())
#test

folds=5         # how many folds
kf=cross_validation.KFold(len(data.axes[0]), n_folds=folds, shuffle=True)

scaler = StandardScaler()
#clf = MLPClassifier(hidden_layer_sizes=(3,), shuffle=True,verbose=False)
#clf = RandomForestClassifier(n_estimators=50, class_weight={1:1/4})
#clf = LogisticRegression(penalty='l2')
clf = LogisticRegression(penalty='l2', C=10, class_weight={1: 1})
#clf = SVC()
metric = 0
accur = 0
recall = 0 
f1 = 0
matrix = np.zeros([2,2])
coefs = np.empty([1,data.shape[1]])

for train_index, test_index in kf:
    X_train, X_test = data.iloc[train_index], data.iloc[test_index]
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    y_train, y_test = target[train_index], target[test_index]

    clf.fit(X_train_scaled, y_train)
    coefs += clf.coef_
    predict = clf.predict(X_test_scaled)
#    metric += roc_auc_score(y_test, clf.predict_proba(X_test)[:,1])
    accur += precision_score(y_test, predict)
    recall += recall_score(y_test, predict)
    f1 += f1_score(y_test, predict)    
    matrix += confusion_matrix(y_test, predict)
    print (f1)


print (pd.DataFrame((coefs/folds)/np.max(np.abs(coefs/folds))).loc[0,:])
#print (data.loc[119, :])
print ('accur', accur/folds)
print ('recall', recall/folds)
print ('f1', f1/folds)
print (matrix)


#clf.fit(data, wwlln)
#joblib.dump(clf, 'Classifier_1-2June2015.pkl')

