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
X_train = np.array(np.array(full_data.features)[:,7:10])[train_index]
Y_train = np.array(full_data.labels)[train_index]
X_test = np.array(np.array(full_data.features)[:,7:10])[test_index]
Y_test = np.array(full_data.labels)[test_index]

print X_train

n_classes = len(np.unique(Y_train))
#print n_classes

classifier = GMM(n_components = 4, covariance_type = 'diag', init_params = 'wc', n_iter = 20)

classifier.means_ = np.array([X_train[Y_train == i].mean(axis=0)for i in xrange(4)])
print classifier.means_

classifier.fit(X_train)
y_train_pred = classifier.predict(X_train)
train_accuracy = np.mean(y_train_pred.ravel() == Y_train.ravel()) * 100
print train_accuracy

y_test_pred = classifier.predict(X_test)
test_accuracy = np.mean(y_test_pred.ravel() == Y_test.ravel()) * 100
print test_accuracy

#limit = int(full_data.len()*(2.0/3.0))
#print full_data
#print limit
#obs = []
#labels = []
#for i in range (0, limit):
#    obs.append([ho_data.gyrox.data[i], ho_data.gyroy.data[i], ho_data.gyroz.data[i]])
#    labels.append[]
#for i in range (0, limit):
#    obs.append([ff_data.gyrox.data[i], ff_data.gyroy.data[i], ff_data.gyroz.data[i]])
#for i in range (0, limit):
#    obs.append([hs_data.gyrox.data[i], hs_data.gyroy.data[i], hs_data.gyroz.data[i]])
#for i in range (0, limit):
#    obs.append([sw_data.gyrox.data[i], sw_data.gyroy.datap[i], sw_data.gyroz.data[i]])
#obs = ho_data.gyrox.data[0:limit]
#obs.append(ho_data.gyroy.data[0:limit])
#obs.append(ho_data.gyroz.data[0:limit])
#print obs
#g.fit(obs)
#print g
