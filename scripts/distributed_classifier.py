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
from sklearn.cross_validation import StratifiedKFold
from entry_data import DataEntry, fullEntry
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD

def create_training_data(data, imu, meas):
    ff = []
    for k in range(0, len(data)):
        f =[]
        for j in range(0, len(imu)):
            if imu[j] == 1:
                for i in range(0, len(meas)):
                    if meas[i]==1:
                        if i == 0:
                            f.append(data[k][j*13])
                            f.append(data[k][j*13 + 1])
                            f.append(data[k][j*13 + 2])
                            f.append(data[k][j*13 + 3])
                        else: 
                            f.append(data[k][j*13 + i*3 + 1])
                            f.append(data[k][j*13 + i*3 + 2])
                            f.append(data[k][j*13 + i*3 + 3])
        ff.append(f)
    return ff

rul_vec = np.zeros(13)
rll_vec = np.zeros(13)
rf_vec = np.zeros(13)

def upper_leg_cb(data):
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
    rul_vec[12] = data.comZ

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
t = np.zeros((4,4))
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

f1 = np.array(foot_data.features)
f2 = np.array(lower_leg_data.features)
f3 = np.array(upper_leg_data.features)
labels = foot_data.labels

f1 = np.hstack((f1, f2))
f1 = np.hstack((f1, f3))
# print f1.shape
n_classes = 4

limit = int(len(f1)*(8/10.0))
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



t = [[0.8, 0.2, 0.0, 0.0], \
      [0.0, 0.8, 0.2, 0.0], \
      [0.0, 0.0, 0.8, 0.2], \
      [0.2, 0.0, 0.0, 0.8]]

startprob = [0.25, 0.25, 0.25, 0.25]

# t = [[0.9, 0.1, 0.0, 0.0],\
#        [0.0, 0.9, 0.1, 0.0],\
#        [0.0, 0.0, 0.9, 0.1],\
#        [0.1, 0.0, 0.0, 0.9]]

model = HMM(name="Gait")
distros = []
hmm_states = []
state_names = ['ff', 'ho', 'sw', 'hs']
hmm_states = []
for i in range(0, n_classes):
    # print np.array(class_means[i]).shape
    # print np.array(class_cov[i]).shape
    # dis = MultivariateGaussianDistribution(np.array(class_means[i]).transpose(), class_cov[i])
    dis = MGD\
        (np.array(class_means[i]).flatten().reshape(7, 1),\
         np.array(class_cov[i]))
    st = State(dis, name=state_names[i])
    distros.append(dis)
    print dis
    # exit()
    hmm_states.append(st)

print hmm_states
print distros
# exit()


model.add_transition(model.start, hmm_states[0], 0.25)
model.add_transition(model.start, hmm_states[1], 0.25)
model.add_transition(model.start, hmm_states[2], 0.25)
model.add_transition(model.start, hmm_states[3], 0.25)
for i in range(0, n_classes):
    for j in range(0, n_classes):
        model.add_transition(hmm_states[i], hmm_states[j], t[i][j])
        # print (states[i].name+"("+str(i)+")-> "+states[j].name+"("+str(j)+") : "+str(t[i][j]))
model.bake(verbose=True)


seq = np.array(ff[:limit][0]).flatten()
print distros[0].log_probability(seq)
print distros[1].log_probability(seq)
print distros[2].log_probability(seq)
print distros[3].log_probability(seq)
seq = np.array(ff[:2][:])
seq = [[4, 2, 1, 1, 1, 1, 1],[1]]
print seq
# print model.sample()
# print model.states
# print np.array(seq).shape
# print seq
# print model.log_probability([0.3])
# model.fit(seq, algorithm='baum-welch')
# print model
model.fit(seq, algorithm='viterbi')
# trans, ems = model.forward_backward( sequence )
# print model
print '------------------------------------'
exit()
# dis_0 = NormalDistribution.from_samples(np.array(class_data[0][:])[:,[0]])
# dis_1 = NormalDistribution.from_samples(np.array(class_data[1][:])[:,[0]])
# dis_2 = NormalDistribution.from_samples(np.array(class_data[2][:])[:,[0]])
# dis_3 = NormalDistribution.from_samples(np.array(class_data[3][:])[:,[0]])
# ff_ = State(dis_0, name="ff")
# ho_ = State(dis_1, name="ho")
# sw_ = State(dis_2, name="sw")
# hs_ = State(dis_3, name="hs")
# states = [ff_, ho_, sw_, hs_]
# print model.states
# model.fit(sequence, algorithm = 'viterbi')
# trans, ems = model.forward_backward( sequence )

# model2 = HiddenMarkovModel(name = "GMM_Gait_")

# is_0_0 = NormalDistribution.from_samples(np.array(class_data[0][:])[:,[0]])
# dis_0_1 = NormalDistribution.from_samples(np.array(class_data[0][:])[:,[1]])
# dis_0_2 = NormalDistribution.from_samples(np.array(class_data[0][:])[:,[2]])
# mixture_a = MixtureDistribution([dis_0_0, dis_0_1, dis_0_2])
# mgd_0 = MultivariateGaussianDistribution(dis_0_0, dis_0_1, dis_0_2)

# dis_1_0 = NormalDistribution.from_samples(np.array(class_data[1][:])[:,[0]])
# dis_1_1 = NormalDistribution.from_samples(np.array(class_data[1][:])[:,[1]])
# dis_1_2 = NormalDistribution.from_samples(np.array(class_data[1][:])[:,[2]])
# mixture_b = MixtureDistribution([dis_1_0, dis_1_1, dis_1_2])

# dis_2_0 = NormalDistribution.from_samples(np.array(class_data[2][:])[:,[0]])
# dis_2_1 = NormalDistribution.from_samples(np.array(class_data[2][:])[:,[1]])
# dis_2_2 = NormalDistribution.from_samples(np.array(class_data[2][:])[:,[2]])
# mixture_c = MixtureDistribution([dis_2_0, dis_2_1, dis_2_2])

# dis_3_0 = NormalDistribution.from_samples(np.array(class_data[3][:])[:,[0]])
# dis_3_1 = NormalDistribution.from_samples(np.array(class_data[3][:])[:,[1]])
# dis_3_2 = NormalDistribution.from_samples(np.array(class_data[3][:])[:,[2]])
# mixture_d = MixtureDistribution([dis_3_0, dis_3_1, dis_3_2])

# ff_ = State(mixture_a, name="ff")
# ho_ = State(mixture_b, name="ho")
# sw_ = State(mixture_c, name="sw")
# hs_ = State(mixture_d, name="hs")

# model2.add_transition(model2.start, ff_, 0.25)
# model2.add_transition(model2.start, ho_, 0.25)
# model2.add_transition(model2.start, sw_, 0.25)
# model2.add_transition(model2.start, hs_, 0.25)
# states = [ff_, ho_, sw_, hs_]
# for i in range(0, n_classes):
#   for j in range(0, n_classes):
#       model2.add_transition(states[i], states[j], t[i][j])
#       print (states[i].name+"("+str(i)+")-> "+states[j].name+"("+str(j)+") : "+str(t[i][j]))
# model2.bake(verbose = True)

# trans, ems = model.forward_backward( sequence )
# print trans
# print model2.states
