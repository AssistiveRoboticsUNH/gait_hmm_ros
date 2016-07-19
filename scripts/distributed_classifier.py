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
from std_msgs.msg import Int32
from threespace_ros.msg import dataVec
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import normalize
from entry_data import DataEntry, fullEntry
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD


def create_training_data(data_, imu, meas):
    ff_ = []
    for k in range(0, len(data_)):
        f_ = []
        for jj in range(0, len(imu)):
            if imu[jj] == 1:
                for ii in range(0, len(meas)):
                    if meas[ii] == 1:
                        if ii == 0:
                            f_.append(data_[k][jj*13])
                            f_.append(data_[k][jj*13 + 1])
                            f_.append(data_[k][jj*13 + 2])
                            f_.append(data_[k][jj*13 + 3])
                        else: 
                            f_.append(data_[k][jj*13 + ii*3 + 1])
                            f_.append(data_[k][jj*13 + ii*3 + 2])
                            f_.append(data_[k][jj*13 + ii*3 + 3])
        ff_.append(f_)
    return ff_

# rul_vec = np.zeros(13)
# rll_vec = np.zeros(13)
# rf_vec = np.zeros(13)

rul_vec = [0 for i in range(0, 13)]
rll_vec = [0 for i in range(0, 13)]
rf_vec = [0 for i in range(0, 13)]


def foot_cb(data):
    rul_vec[0] = data.quat.quaternion.x
    rul_vec[1] = data.quat.quaternion.y
    rul_vec[2] = data.quat.quaternion.z
    rul_vec[3] = data.quat.quaternion.w
    rul_vec[4] = data.gyroX
    rul_vec[5] = data.gyroY
    rul_vec[6] = data.gyroZ
    rul_vec[7] = data.accX
    rul_vec[8] = data.accY
    rul_vec[9] = data.accZ
    rul_vec[10] = data.quat.comX
    rul_vec[11] = data.quat.comY
    rul_vec[12] = data.qcomZ


def lower_leg_cb(data):
    rll_vec[0] = data.quat.quaternion.x
    rll_vec[1] = data.quat.quaternion.y
    rll_vec[2] = data.quat.quaternion.z
    rll_vec[3] = data.quat.quaternion.w
    rll_vec[4] = data.gyroX
    rll_vec[5] = data.gyroY
    rll_vec[6] = data.gyroZ
    rll_vec[7] = data.accX
    rll_vec[8] = data.accY
    rll_vec[9] = data.accZ
    rll_vec[10] = data.quat.comX
    rll_vec[11] = data.quat.comY
    rll_vec[12] = data.comZ


def upper_leg_cb(data):
    rf_vec[0] = data.quat.quaternion.x
    rf_vec[1] = data.quat.quaternion.y
    rf_vec[2] = data.quat.quaternion.z
    rf_vec[3] = data.quat.quaternion.w
    rf_vec[4] = data.gyroX
    rf_vec[5] = data.gyroY
    rf_vec[6] = data.gyroZ
    rf_vec[7] = data.accX
    rf_vec[8] = data.accY
    rf_vec[9] = data.accZ
    rf_vec[10] = data.quat.comX
    rf_vec[11] = data.quat.comY
    rf_vec[12] = data.comZ

rospy.init_node('hmm_trainer')
param_vec = []
rospack = rospkg.RosPack()
prefix = rospy.get_param('~prefix', 'None')
use_imu = np.zeros(3)
use_measurements = np.zeros(4)

if prefix == 'None':
    rospy.logerr("No filename given ,exiting")
    exit()

rospy.Subscriber(rospy.get_param('~foot_topic', 'l_upper_arm_data_vec'), dataVec, foot_cb)
rospy.Subscriber(rospy.get_param('~l_leg_topic', 'l_hand_data_vec'), dataVec, lower_leg_cb)
rospy.Subscriber(rospy.get_param('~u_leg_topic', 'r_hand_data_vec'), dataVec, upper_leg_cb)
phase_pub = rospy.Publisher('/phase', std_msgs.msg.Int32, queue_size=10)
use_imu[0] = rospy.get_param('~use_foot', 1)
use_imu[1] = rospy.get_param('~use_lower_leg', 0)
use_imu[2] = rospy.get_param('~use_upper_leg', 0)
use_measurements[0] = rospy.get_param('~use_quat', 0)
use_measurements[1] = rospy.get_param('~use_gyro', 0)
use_measurements[2] = rospy.get_param('~use_accel', 0)
use_measurements[3] = rospy.get_param('~use_comp', 0)
data = pickle.load(open(rospack.get_path('gait_hmm_ros')+'/scripts/'+prefix + "_foot_annotated.p", "rb"))
data3 = pickle.load(open(rospack.get_path('gait_hmm_ros')+'/scripts/'+prefix + "_upper_leg_annotated.p", "rb"))
data2 = pickle.load(open(rospack.get_path('gait_hmm_ros')+'/scripts/'+prefix + "_lower_leg_annotated.p", "rb"))
invalid_data = ed.classData(label=-1)
rospy.logwarn("Training %s", prefix)
rospy.logwarn(use_imu)
rospy.logwarn(use_measurements)
upper_leg_data = fullEntry()
lower_leg_data = fullEntry()
foot_data = fullEntry()
t = np.zeros((4, 4))
prev = -1

alphabet = ['HO', 'FF', 'HS', 'SW']
correct_mapping = [1, 0, 2, 3]

sum_ = 0
for i in range(0, len(data)):
    if data[i].label != -1:
        # data[i]._replace(label = correct_mapping[data[i].label])
        if prev == -1:
            prev = data[i].label
        t[prev][data[i].label] += 1.0
        prev = data[i].label
        foot_data.add(data[i])
        lower_leg_data.add(data2[i])
        upper_leg_data.add(data3[i])
        sum_ += 1.0

skf = StratifiedKFold(foot_data.labels, n_folds=4)
train_index, test_index = next(iter(skf))

t = normalize(t, axis=1, norm='l1')
f1 = np.array(foot_data.features)
f2 = np.array(lower_leg_data.features)
f3 = np.array(upper_leg_data.features)
labels = foot_data.labels

f1 = np.hstack((f1, f2))
f1 = np.hstack((f1, f3))
# print f1.shape
n_classes = 4

limit = int(len(f1)*(9.5/10.0))
# print limit

class_data = [[] for x in range(4)]

ff = np.array(create_training_data(f1, use_imu, use_measurements))
n_signals = len(ff[0])

print n_signals == ff.shape[1]

for i in range(0, len(ff)):
    class_data[labels[i]].append(ff[i])

class_means = [[[] for x in range(n_signals)] for i in range(n_classes)]
class_vars = [[[] for x in range(n_signals)] for i in range(n_classes)]
class_std = [[[] for x in range(n_signals)] for i in range(n_classes)]
class_cov = []
classifiers = []

for i in range(0, n_classes):
    cov = np.ma.cov(np.array(class_data[i]), rowvar=False)
    class_cov.append(cov)
    for j in range(0, n_signals):
        class_means[i][j] = np.array(class_data[i][:])[:, [j]].mean(axis=0)
        class_vars[i][j] = np.array(class_data[i][:])[:, [j]].var(axis=0)
        class_std[i][j] = np.array(class_data[i][:])[:, [j]].std(axis=0)

startprob = [0.25, 0.25, 0.25, 0.25]

# t = [[0.7, 0.3, 0.0, 0.0],\
#        [0.0, 0.7, 0.3, 0.0],\
#        [0.0, 0.0, 0.7, 0.3],\
#        [0.3, 0.0, 0.0, 0.7]]


distros = []
hmm_states = []
state_names = ['ff', 'ho', 'sw', 'hs']
hmm_states = []
for i in range(0, n_classes):
    # print np.array(class_means[i]).shape
    # print np.array(class_cov[i]).shape
    # dis = MultivariateGaussianDistribution(np.array(class_means[i]).transpose(), class_cov[i])
    dis = MGD\
        (np.array(class_means[i]).flatten(),
         np.array(class_cov[i]))
    st = State(dis, name=state_names[i])
    distros.append(dis)
    hmm_states.append(st)
model = HMM(name="Gait")
# print hmm_states
# print distros
print t

model.add_states(hmm_states)
model.add_transition(model.start, hmm_states[0], 1.00)
model.add_transition(model.start, hmm_states[1], 0.0)
model.add_transition(model.start, hmm_states[2], 0.0)
model.add_transition(model.start, hmm_states[3], 0.0)
# model.add_transition(model.start, hmm_states[0], 0.25)
# model.add_transition(model.start, hmm_states[1], 0.25)
# model.add_transition(model.start, hmm_states[2], 0.25)
# model.add_transition(model.start, hmm_states[3], 0.25)

for i in range(0, n_classes):
    for j in range(0, n_classes):
        model.add_transition(hmm_states[i], hmm_states[j], t[i][j])
        # print (states[i].name+"("+str(i)+")-> "+states[j].name+"("+str(j)+") : "+str(t[i][j]))

model.bake()

seq = list([ff[:limit]])
print model.name
print model.d
print model.edges
print model.silent_start

# print model
model.fit(seq, algorithm='baum-welch', verbose='True')
# model.fit(seq, algorithm='viterbi', verbose='True')

logp, path = model.viterbi(list(ff[limit:]))
print len(path)
sum_ = 0.0
for i in range(0, len(path)):
    if path[i][1].name != 'Gait-start':
        # print path[i][1].name + " " + state_names[labels[i+limit - 1]]
        if path[i][1].name == state_names[labels[i+limit - 1]]:
            sum_ += 1.0
print str(sum_) + "/" + str(len(list(ff[limit:limit])))
print sum_/float(len(list(ff[limit:])))
print '------------------------------------'

counter = 0
stream = []
while not rospy.is_shutdown():
    rospy.logwarn("Spinning")
    counter += 1
    stream.append(rul_vec + rll_vec + rf_vec)
    if counter == 10:
        rospy.logerr("New entry")
        counter = 0
        sw_cnt = 0
        st_cnt = 0
        print stream[0]
        online_batch = create_training_data(stream, use_imu, use_measurements)
        logp, path = model.viterbi(list(ff[limit:]))
        for i in range(0, len(path)):
            if path[i][1].name != 'Gait-start':
                if path[i][1].name == 'swing':
                    sw_cnt += 1
                else:
                    st_cnt += 1
        if sw_cnt > st_cnt:
            phase_pub.publish(1)
        else:
            phase_pub.publish(0)
        stream = []
    # rospy.spin()
exit()
# print model2.states
# print path[i][1].name + " " + str(path[i][0]) + " " +\
#  str(state_names.index(path[i][1].name)) + " " + str(labels[i+limit])
