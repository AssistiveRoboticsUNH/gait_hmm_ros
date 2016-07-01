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
import numpy as np
import entry_data as ed
from threespace_ros.msg import dataVec
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import normalize
from entry_data import DataEntry, fullEntry
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD


def create_data(imu, meas):
    indexes_ = []
    d = 0
    for i in range(len(imu)):
        if imu[i] != 0:
            if meas[0] == 1:
                indexes_.append(d * 13 + 0)
                indexes_.append(d * 13 + 1)
                indexes_.append(d * 13 + 2)
                indexes_.append(d * 13 + 3)
            for k in range(1, 4):
                if meas[k] == 1:
                    indexes_.append(d * 13 + k * 3 + 1)
                    indexes_.append(d * 13 + k * 3 + 2)
                    indexes_.append(d * 13 + k * 3 + 3)
            d += 1
    print indexes_
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

# X_train = full_features[0:limit]
# Y_train = full_labels[0:limit]
# X_test = full_features[limit:]
# Y_test = full_labels[limit:]

X_train = full_features[train_index]
Y_train = full_labels[train_index]
X_test = full_features[test_index]
Y_test = full_labels[test_index]

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

class_means = []
for i in range(n_classes):
    class_means.append([[] for x in range(n_features)])

class_vars = []
for i in range(n_classes):
    class_vars.append([[] for x in range(n_features)])

class_std = []
for i in range(n_classes):
    class_std.append([[] for x in range(n_features)])

class_cov = []
classifiers = []
# FILL IN VALUES
for i in range(n_classes):
    cov = np.ma.cov(np.array(class_data[i]), rowvar=False)
    class_cov.append(cov)
    for j in range(0, n_features):
        # class_means[i][j] = np.mean(class_data[i], axis=0)
        # class_vars[i][j] = np.var(class_data[i], axis=0)
        class_means[i][j] = np.array(class_data[i][:])[:, [j]].mean(axis=0)
        class_vars[i][j] = np.array(class_data[i][:])[:, [j]].var(axis=0)
        class_std[i][j] = np.array(class_data[i][:])[:, [j]].std(axis=0)

# rospy.logerr("#######################################")
rospy.logwarn("Class means shape :"+str(np.array(class_means).shape))
# rospy.logwarn(class_means)
rospy.logwarn("Class variances shape :"+str(np.array(class_vars).shape))
# rospy.logwarn(class_vars)
rospy.logwarn("Class covariances shape :" + str(np.array(class_cov).shape))

distros = []
hmm_states = []

for i in range(0, n_classes):
    dis = MGD(np.array(class_means[i]).flatten(), np.array(class_cov[i]))
    st = State(dis, name=phase_labels[i])
    distros.append(dis)
    hmm_states.append(st)
model = HMM(name="Gait")

model.add_states(hmm_states)
model.add_transition(model.start, hmm_states[0], 0.5)
model.add_transition(model.start, hmm_states[1], 0.5)

# t = [[0.3, 0.7],
#      [0.7, 0.3]]

t = normalize(t, axis=1, norm='l1')

for i in range(0, n_classes):
    for j in range(0, n_classes):
        model.add_transition(hmm_states[i], hmm_states[j], t[i][j])
        print (hmm_states[i].name+"("+str(i)+")-> "+hmm_states[j].name+"("+str(j)+") : "+str(t[i][j]))

model.bake()

# seq = list([full_features[:limit]])
skf = StratifiedKFold(list(full_labels), n_folds=10, shuffle=True)
# print skf[2]

for train_index, test_index in skf:
    X_train = full_features[train_index]
    Y_train = full_labels[train_index]
    X_test = full_features[test_index]
    Y_test = full_labels[test_index]

    model.fit(list([X_train]), algorithm='viterbi', verbose='False')

    logp, path = model.viterbi(list(X_test))
    sum_ = 0.0
    path = path[1:]

    for i in range(0, len(path)):
        # print path[i][1].name + " " + phase_labels[Y_test[i]]
        if path[i][1].name == phase_labels[Y_test[i]]:
            sum_ += 1.0
    print str(sum_) + "/" + str(len(Y_test))
    print sum_/float(len(Y_test))
    print '------------------------------------'
exit()
seq = list([full_features[train_index]])
test = list([full_features[test_index]])
test_labels = full_labels[test_index]
# print model
# model.fit(seq, algorithm='baum-welch', verbose='True')
model.fit(seq, algorithm='viterbi', verbose='True')

# logp, path = model.viterbi(list(full_features[limit:]))
logp, path = model.viterbi(list(full_features[test_index]))
sum_ = 0.0
# print class_cov[0]
# print class_cov[1]
path = path[1:]
for i in range(0, len(path)):
    # print path[i][1].name
    # print test_labels[i]
    if path[i][1].name != 'Gait-start' :
        # print path[i][1].name + " " + phase_labels[full_labels[i+limit - 1]]
        # print i+limit - 1
        # if path[i][1].name == phase_labels[full_labels[i+limit - 1]]:
        if path[i][1].name == phase_labels[test_labels[i]]:
            sum_ += 1.0
# print str(sum_) + "/" + str(len(list(full_labels[limit:])))
print str(sum_) + "/" + str(len(test_labels))
print sum_/float(len(test_labels))
print '------------------------------------'
exit()
