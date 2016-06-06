#!/usr/bin/env python
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import time
import math
import UnfairCasino
import pickle
import sys
import operator
import numpy as np
import entry_data as ed
from sklearn import datasets
from sklearn import mixture
from sklearn.cross_validation import StratifiedKFold
from sklearn.externals.six.moves import xrange
from sklearn.mixture import GMM
from sklearn.mixture import VBGMM
from collections import namedtuple
from threespace_ros.msg import dataVec
from matplotlib import pyplot as plt
from entry_data import DataEntry, fullEntry


rospy.init_node('hmm_trainer')
alphabet = ['HO','FF','HS','SW']

data = []
if(len(sys.argv)<2):
    exit()
else:
    prefix=sys.argv[1]
#print prefix+"_foot.p"
data = pickle.load(open(prefix+"_foot_annotated.p","rb"))
#print data
ho_data = ed.classData(label = 0)
ff_data = ed.classData(label = 1)
hs_data = ed.classData(label = 2)
sw_data = ed.classData(label = 3)
invalid_data = ed.classData(label = -1)
full_data = fullEntry()
t = np.zeros((4,4))
prev = -1
sum = 0 
for entry in data:
    #rospy.logwarn("%f %f %f %d %d",entry.gyrox, entry.gyroy, entry.gyroz, entry.label, entry.sequence)
    if entry.label != -1:
        if prev == -1:
            prev = entry.label
        #print entry.label
        if entry.label == 0:
            ho_data.add(entry)
        elif entry.label == 1:
            ff_data.add(entry)
        elif entry.label == 2:
            hs_data.add(entry)
        elif entry.label == 3 :
            sw_data.add(entry)
        t[prev][entry.label]+=1
        prev = entry.label
        full_data.add(entry)
        sum += 1
    else:
        invalid_data.add(entry)
t = t/ sum
#print t
ho_data.calcParams()
ff_data.calcParams()
hs_data.calcParams()
sw_data.calcParams()

skf = StratifiedKFold(full_data.labels, n_folds = 4)
train_index, test_index = next(iter(skf))
#print train_index
#print test_index
#print full_data.features[0]

limit = int(len(full_data.features)*(9.0/10.0))
print limit
#X_train = np.array(np.array(full_data.features)[:,7:10])[train_index]
#Y_train = np.array(full_data.labels)[train_index]
#X_test = np.array(np.array(full_data.features)[:,7:10])[test_index]
#Y_test = np.array(full_data.labels)[test_index]

X_train = np.array(np.array(full_data.features)[:,7:10])[0:limit]
Y_train = np.array(full_data.labels)[0:limit]
X_test = np.array(np.array(full_data.features)[:,7:10])[limit:]
Y_test = np.array(full_data.labels)[limit:]
#print X_train

n_classes = len(np.unique(Y_train))
#print n_classes

classifier = GMM(n_components = 4, covariance_type = 'diag', init_params = 'wc', n_iter = 20)

classifier.means_ = np.array([X_train[Y_train == i].mean(axis=0)for i in xrange(4)])
#print classifier.means_

classifier.fit(X_train)
y_train_pred = classifier.predict(X_train)
train_accuracy = np.mean(y_train_pred.ravel() == Y_train.ravel()) * 100
print train_accuracy

y_test_pred = classifier.predict(X_test)
test_accuracy = np.mean(y_test_pred.ravel() == Y_test.ravel()) * 100
print test_accuracy


prob1 = classifier.predict_proba(X_test)
#print prob1[0]
#print np.sum(prob1[0])
#print prob1
#prob2 = classifier.predict_proba(Y_test)
#print prob2

t = np.zeros((4,4))
sum = 0
prev = -1
for entry in Y_train:
	if(prev == -1):
		prev = entry
	t[prev][entry]+=1
	prev = entry
	sum += 1
t = t/sum
#transition probabilities
#print t
#print np.sum(t)
#means
means = classifier.means_
#print means
#means vector
mean_vec = np.zeros(3)
sum = 0
for entry in X_train:
	mean_vec[0] += entry[0]
	mean_vec[1] += entry[1]
	mean_vec[2] += entry[2]
	sum += 1
mean_vec = mean_vec/sum
#print mean_vec

cov = np.ma.cov(X_train, rowvar = False)
print cov
print cov.shape
var_1 = np.var(X_train, axis = 0)
print var_1
#var_2 = np.var(X_train, axis = 1)
#print var_2



