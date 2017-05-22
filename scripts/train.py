#!/usr/bin/env python
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import time
import math
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
from entry_data import DataEntry, FullEntry
from hmmlearn import hmm

rhvec = np.zeros(13)
lhvec = np.zeros(13)
luavec = np.zeros(13)

def rhandcb(data):
    rhvec[0] = data.quat.quaternion.x
    rhvec[1] = data.quat.quaternion.y
    rhvec[2] = data.quat.quaternion.z
    rhvec[3] = data.quat.quaternion.w
    rhvec[4] = data.gyroX
    rhvec[5] = data.gyroY
    rhvec[6] = data.gyroZ
    rhvec[7] = data.accX
    rhvec[8] = data.accY
    rhvec[9] = data.accZ
    rhvec[10] = data.comX
    rhvec[11] = data.comY
    rhvec[12] = data.comZ

def lhandcb(data):
    lhvec[0] = data.quat.quaternion.x
    lhvec[1] = data.quat.quaternion.y
    lhvec[2] = data.quat.quaternion.z
    lhvec[3] = data.quat.quaternion.w
    lhvec[4] = data.gyroX
    lhvec[5] = data.gyroY
    lhvec[6] = data.gyroZ
    lhvec[7] = data.accX
    lhvec[8] = data.accY
    lhvec[9] = data.accZ
    lhvec[10] = data.comX
    lhvec[11] = data.comY
    lhvec[12] = data.comZ

def luacb(data):
    luavec[0] = data.quat.quaternion.x
    luavec[1] = data.quat.quaternion.y
    luavec[2] = data.quat.quaternion.z
    luavec[3] = data.quat.quaternion.w
    luavec[4] = data.gyroX
    luavec[5] = data.gyroY
    luavec[6] = data.gyroZ
    luavec[7] = data.accX
    luavec[8] = data.accY
    luavec[9] = data.accZ
    luavec[10] = data.comX
    luavec[11] = data.comY
    luavec[12] = data.comZ

rospy.init_node('hmm_trainer')
alphabet = ['HO','FF','HS','SW']
correct_mapping = [1, 0, 2, 3]
data = []
if(len(sys.argv)<2):
    exit()
else:
    prefix=sys.argv[1]
#print prefix+"_foot.p"
data = pickle.load(open(prefix+"_foot_annotated.p","rb"))
data2 = pickle.load(open(prefix+"_upper_leg_annotated.p","rb"))
data3 = pickle.load(open(prefix+"_lower_leg_annotated.p","rb"))

#print data
ho_data = ed.ClassData(label = 0)
ff_data = ed.ClassData(label = 1)
hs_data = ed.ClassData(label = 2)
sw_data = ed.ClassData(label = 3)
invalid_data = ed.ClassData(label = -1)
full_data = FullEntry()
full_data2 = FullEntry()
full_data3 = FullEntry()
t = np.zeros((4,4))
prev = -1
sum = 0 
#for entry in data:
for i in range(0, len(data)):
    #rospy.logwarn("%f %f %f %d %d",entry.gyrox, entry.gyroy, entry.gyroz, entry.label, entry.sequence)
    if data[i].label != -1:
        #idata[i] = data[i]._replace(label = correct_mapping[data[i].label])
        data[i] = data[i]._replace(label = correct_mapping[data[i].label])
        if (prev == -1):
            prev = data[i].label
        #print entry.label
        #if data[i].label == 1:
        #    ho_data.add(entry)
        #elif entry.label == 0:
        #    ff_data.add(entry)
        #elif entry.label == 2:
        #    hs_data.add(entry)
        #elif entry.label == 3 :
        #    sw_data.add(entry)
        t[prev][data[i].label]+=1
        prev = data[i].label
        full_data.add(data[i])
        full_data2.add(data2[i])
        full_data3.add(data3[i])
        sum += 1
    else:
        invalid_data.add(data[i])
t = t/ sum
#print t
#ho_data.calcParams()
#ff_data.calcParams()
#hs_data.calcParams()
#sw_data.calcParams()

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
f1 = np.array(full_data.features)
f2 = np.array(full_data2.features)
f3 = np.array(full_data3.features)
#f1l = np.array(full_data.labels)
#f2l = np.array(full_data2.labels)
#f3l = np.array(full_data3.labels)
#print f1.shape
#print f2.shape
#print f3.shape

f1 = np.hstack((f1,f2))
f1 = np.hstack((f1,f3))
print f1.shape

#X_train = np.array(np.array(full_data.features)[:,7:10])[0:limit]
#Y_train = np.array(full_data.labels)[0:limit]
#X_test = np.array(np.array(full_data.features)[:,7:10])[limit:]
#Y_test = np.array(full_data.labels)[limit:]
X_train = np.hstack((np.hstack((f1[:,7:10], f1[:,20:23])),f1[:,33:36]))[0:limit]
Y_train = full_data.labels[0:limit]
X_test = np.hstack((np.hstack((f1[:,7:10], f1[:,20:23])),f1[:,33:36]))[limit:]
Y_test = full_data.labels[limit:]
#print X_train

n_classes = len(np.unique(Y_train))
#print n_classes

classifier = GMM(n_components = 4, covariance_type = 'diag', init_params = 'wc', n_iter = 20)

#classifier.means_ = np.array([X_train[Y_train == i].mean(axis=0)for i in xrange(4)])
#print classifier.means_

classifier.fit(X_train)
y_train_pred = classifier.predict(X_train)
#Y_test = np.array(full_data.labels)[limit:]
train_accuracy = np.mean(y_train_pred.ravel() == np.array(Y_train).ravel()) * 100
print train_accuracy

y_test_pred = classifier.predict(X_test)
test_accuracy = np.mean(y_test_pred.ravel() == np.array(Y_test).ravel()) * 100
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
#print cov
#print cov.shape
var_1 = np.var(X_train, axis = 0)

trellis = np.zeros((4, len(X_test)))
backpt = np.ones((4, len(X_test)))
initialProb = [0.25, 0.25, 0.25, 0.25]
print t
#model = hmm.GMMHMM(n_components = 4, n_mix = 4, verbose = True)
model = hmm.GMMHMM(n_components = 4, n_mix = 4, verbose = False)
model.transmat_ = t
model.startprob_ = np.array([0.25, 0.25, 0.25, 0.25])
model.means_ = means
model.fit(X_train)
print model
y_train_pred = model.predict(X_train)
train_accuracy = np.mean(y_train_pred.ravel() == np.array(Y_train).ravel()) * 100

print train_accuracy

y_test_pred = model.predict(X_test)
test_accuracy = np.mean(y_test_pred.ravel() == np.array(Y_test).ravel()) * 100
print test_accuracy

rospy.Subscriber("l_hand_datavec", dataVec, lhandcb)
rospy.Subscriber("r_hand_datavec", dataVec, rhandcb)
rospy.Subscriber("l_upper_arm_datavec", dataVec, luacb)
while not rospy.is_shutdown():
    rospy.spin()
