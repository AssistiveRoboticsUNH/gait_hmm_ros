#!/usr/bin/env python
import rospy
import rospkg
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
import os.path
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
from hmmlearn import hmm


def create_data(imu, meas):
    indexes_ = []
    d = 0
    for i in range(len(imu)):
        if imu[i] != 0:
            if meas[0] == 1:
                indexes_.append(d*13+0)
                indexes_.append(d*13+1)
                indexes_.append(d*13+2)
                indexes_.append(d*13+3)
            for k in range(1, 4):
                if meas[k] == 1:
                    indexes_.append(d*13 + 3 + k*3)
                    indexes_.append(d*13 + 3 + k*3 + 1)
                    indexes_.append(d*13 + 3 + k*3 + 2)
            d += 1
    return indexes_

rospy.init_node('mocap_train')
pref = rospy.get_param('~prefix', "none")
rospack = rospkg.RosPack()
path = rospack.get_path('gait_hmm_ros')+'/scripts/'
pref = path + pref

imu_names = ['rf', 'rll', 'rul', 'lf', 'lll', 'lua', 'lul', 'm', 'ch', 'rs', 'rua', 'rla',
             'rw', 'ls', 'lua', 'lla', 'lw']
joints_enable = [0 for i in range(0, len(imu_names))]

meas_names = ['quat', 'gyro', 'accel', 'comp']
meas_enable = [0 for i in range(0, len(meas_names))]

imu_names_full = ['Right Foot', 'Right Lower Leg', 'Right Upper Leg',
                  'Left Foot', 'Left Lower Leg', 'Left Upper Leg',
                  'Mid', 'Chest',
                  'Right Shoulder', 'Right Upper Arm', 'Right Lower Arm', 'Right Wrist',
                  'Left Shoulder', 'Left Upper Arm', 'Left Lower Arm', 'Left Wrist']

mocap_labels = ['LHS', 'LTO', 'RHS', 'RTO']
mocap_indexes = [0, 0, 0, 0]
phase_labels = ['swing', 'stance']
phase_indices = [0, 1]

labels = ["FF", "HO", "SW", "HS"]

imu_pickled_data = []
imu_enable = [0 for i in range(0, len(imu_names))]

total_entries = 0
total_sensors = len(imu_names)
vector_sizes = [0 for i in range (0, total_sensors)]

n_classes = len(phase_labels)
n_sensors = len(imu_names)
t = np.zeros((n_classes, n_classes))

for i in range(0, len(meas_names)):
    param = "~use_"+meas_names[i]
    meas_enable[i] = rospy.get_param(param, 0)
rospy.logwarn(meas_enable)

for i in range(0, len(imu_names)):
    param = "~use_"+imu_names[i]
    imu_enable[i] = rospy.get_param(param, 0)
rospy.logwarn(imu_enable)

n = 0

for n in range(0, n_sensors):
    name = imu_names[n]
    fullname = pref+"_"+name+"_annotated.p"
    if os.path.isfile(fullname):
        rospy.logwarn("Loading "+fullname)
        x = pickle.load(open(fullname, "rb"))
        print len(x)
        imu_pickled_data.append(x)
        total_entries = len(x)
        vector_sizes[n] += 1
    else:
        imu_pickled_data.append([])

imu_timestamps = pickle.load(open(pref+"_timestamps.p", "rb"))

rl_timestamps = []
for i in imu_timestamps:
    rl_timestamps.append(abs(i - imu_timestamps[0])/1000000000)

# phase_labels = ['lswing', 'lstance', 'rswing', 'rstance']
# phase_labels = [0, 1, 2, 3]

full_data = [fullEntry() for i in range(0, n_sensors)]

sum_ = 0
sums = [0, 0, 0, 0]
prev = -1
for i in range(0, total_entries):
    for j in range(0, total_sensors):
        inc_ = 0
        if vector_sizes[j] != 0:
            sum_ += 1
            if inc_ == 0:
                inc_ = 1
                if prev == -1:
                    prev = imu_pickled_data[j][i].label
                t[prev][imu_pickled_data[j][i].label] += 1
                sums[prev] += 1
                prev = imu_pickled_data[j][i].label
            full_data[j].add(imu_pickled_data[j][i])
            sum_ += 1

created = 0
for i in range(0, len(full_data)):
    if full_data[i].len() != 0:
        if created == 0:
            print "lel"
            full_features = np.array(full_data[i].features)
            full_labels = np.array(full_data[i].labels)
            created = 1
        else:
            full_features = np.hstack((full_features, np.array(full_data[i].features)))

indexes = create_data(imu_enable, meas_enable)
n_features = len(indexes)
rospy.logwarn(indexes)
full_features = full_features[:, indexes]

skf = StratifiedKFold(full_labels, n_folds=4)
train_index, test_index = next(iter(skf))
limit = int(len(full_features) * (9.0 / 10.0))

# rospy.loginfo(limit)

X_train = full_features[0:limit]
Y_train = full_labels[0:limit]
X_test = full_features[limit:]
Y_test = full_labels[limit:]

# rospy.loginfo(Y_train)

cov_ = np.ma.cov(X_train, rowvar=False)
var_ = np.var(X_train, axis=0)
initialProb = [0.5, 0.5]

sum_ = 0
sums = [0, 0]
prev = -1

t = np.zeros((n_classes, n_classes))
for entry in Y_train:
    if prev == -1:
        prev = entry
        continue
    t[prev][entry] += 1
    sum_ += 1
    sums[prev] += 1
    prev = entry

rospy.loginfo(t)
for i in range(0, n_classes):
    for j in range(0, n_classes):
        t[i][j] /= sums[i]
rospy.loginfo(t)

startprob = [0.5, 0.5]

class_data = [[] for x in range(n_classes)]
for i in range(0, len(full_features)):
    class_data[full_labels[i]].append(full_features[i])

print len(class_data[0])
print len(class_data[1])
print len(class_data[1])+len(class_data[0])
# print np.array(class_data).shape
# print np.array(class_data[0]).shape

print len(class_data[0][1])
exit()
class_means = []
for i in range(n_features):
    class_means.append([[] for x in range(n_features)])

rospy.logerr(len(class_means[0]))
rospy.logerr(len(class_means[1]))

class_vars = []
for i in range(n_features):
    class_vars.append([[] for x in range(n_features)])

print len(class_vars[0])

for i in range(n_classes):
    for j in range(0, n_features):
        class_means[i] = np.mean(class_data[i], axis=0)
        class_vars[i] = np.var(class_data[i], axis=0)

rospy.logwarn(len(class_vars[0]))
rospy.logwarn((class_vars[0][1]))

rospy.loginfo(class_vars)

exit()
model = hmm.GMMHMM(n_components=n_classes, n_mix=n_classes, verbose=True, n_iter=1000, init_params="tcm")
model.startprob_ = startprob
model.transmat_ = t
