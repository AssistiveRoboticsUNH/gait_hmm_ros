#!/usr/bin/env python
import rospy
import rospkg
import pickle
import numpy as np
import entry_data as ed
import imu_callbacks as iparam
from threespace_ros.msg import dataVec
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import normalize
from entry_data import DataEntry, fullEntry
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from scipy import io as scio

rospy.init_node('dis_class_2')
pref = rospy.get_param('~prefix', "none")
use_quat = rospy.get_param('~use_quat', 0)
use_gyro = rospy.get_param('~use_gyro', 0)
use_accel = rospy.get_param('~use_accel', 0)
use_com = rospy.get_param('~use_com', 0)
use_fsr = rospy.get_param('~use_fsr', 0)
use_ir = rospy.get_param('~use_ir', 0)
use_prox = rospy.get_param('~use_prox', 0)
folds = rospy.get_param('~folds', 10)
batch_train = rospy.get_param('~batch_train', 1)
rospack = rospkg.RosPack()
path = rospack.get_path('gait_hmm_ros') + '/scripts/'

stats = []

names = ['andreas1', 'andreas2', 'andreas3', 'andreas4', 'andreas5']

joint_names = iparam.imu_names

imu_names = iparam.imu_param_names

join_names_full = iparam.imu_names_full

total_sensors = len(imu_names)
total_entries = 0

sum = 0
full_data = []
full_labels = []
class_data = [[] for x in range(0, 2)]
#####################
# Load enabled IMUS #
#####################
for filename in names:
    sensor_data = []
    pref = path + filename
    for name in joint_names:
        full_name = pref + "_" + name + ".mat"
        # print full_name
        if os.path.isfile(full_name):
            rospy.logwarn("Loading" + full_name)
            x = scio.loadmat(full_name)
            x = x.get(name)
            total_entries = len(x)
            data_entry = []
            for i in range(0, len(x)):
                entry = []
                if use_quat == 1:
                    entry = np.concatenate((entry, x[i, 0:4]), axis=0)
                if use_gyro == 1:
                    entry = np.concatenate((entry, x[i, 4:7]), axis=0)
                if use_accel == 1:
                    entry = np.concatenate((entry, x[i, 7:10]), axis=0)
                if use_com == 1:
                    entry = np.concatenate((entry, x[i, 10:13]), axis=0)
                # print(len(entry))
                data_entry.append(entry)
            print len(data_entry)
            if sensor_data == []:
                sensor_data = data_entry
            else:
                sensor_data = np.concatenate((sensor_data, data_entry), axis=1)
                # print total_entries
    x = []
    arduino = scio.loadmat(pref + "_arduino.mat")
    arduino = arduino.get("arduino")
    arduino_data = []
    # print arduino
    # print len(arduino)
    for i in range(0, len(arduino)):
        entry = []
        # print arduino[i]
        if use_fsr == 1:
            # print (arduino[i, 3:6])
            entry = np.concatenate((entry, arduino[i, 3:6]), axis=0)
        if use_ir == 1:
            # print(arduino[i, 7])
            entry = np.concatenate((entry, arduino[i, 6:7]), axis=0)
        if use_prox == 1:
            entry = np.concatenate((entry, arduino[i, 7:8]), axis=0)
        arduino_data.append(entry)
    arduino = []

    # print arduino_data[0]
    # print len(arduino_data)
    # print len(arduino_data[0])

    # print sensor_data[0]
    # print len(sensor_data)
    # print len(sensor_data[0])

    sensor_data = np.concatenate((sensor_data, arduino_data), axis=1)
    # print(sensor_data[0])
    # print(len(sensor_data))
    # print(len(sensor_data[0]))

    labels = scio.loadmat(pref+"_labels_mocap_annotated.mat")
    labels = labels.get("labels")
    labels = labels[0]
    # print labels
    # print len(labels)
    if full_data == []:
        full_data = sensor_data
    else:
        full_data = np.concatenate((full_data, sensor_data), axis=0)
    sum += len(sensor_data)

    if full_labels == []:
        full_labels = labels
    else:
        full_labels = np.concatenate((full_labels, labels), axis=0)

    # if labels[0] == 0:
    #     if class_data[0] == []:
    #         class_data[0] = labels
    #     else:
    #         class_data[0] = np.concatenate((class_data[0], labels), axis = 0)
    # else:
    #     if class_data[1] == []:
    #         class_data[1] = labels
    #     else:
    #         class_data[1] = np.concatenate((class_data[1], labels), axis = 0)

labels = []
sensor_data = []
print len(full_data[0])
print len(full_data)
print sum
print full_data[0]

print len(full_labels)

startprob = [0.5, 0.5]

for i in range(0, len(full_data)):
    if full_labels[i] == 0:
        class_data[0].append(full_data[i])
    else:
        class_data[1].append(full_data[i])
class_means = [[[] for x in range(len(full_data[0]))] for i in range(0, 2)]
class_vars = [[[] for x in range(len(full_data[0]))] for i in range(0, 2)]
class_std = [[[] for x in range(len(full_data[0]))] for i in range(0, 2)]
class_cov = []
classifiers = []


# print class_data[0]
# print class_data[1]
print (len(class_data[0]) + len(class_data[1]))

for i in range(0, 2):
    cov = np.ma.cov(np.array(class_data[i]), rowvar=False)
    class_cov.append(cov)
    for j in range(0, len(full_data[0])):
        class_means[i][j] = np.array(class_data[i][:])[:, [j]].mean(axis=0)
        class_vars[i][j] = np.array(class_data[i][:])[:, [j]].var(axis=0)
        class_std[i][j] = np.array(class_data[i][:])[:, [j]].std(axis=0)

t = np.zeros((2, 2))

#############################
# calculate transition probs#
#############################
sum_ = 0
prev = -1

for i in range(0, len(full_labels)):
    if prev == -1:
        prev = full_labels[i]
    t[prev][full_labels[i]] += 1.0
    prev = full_labels[i]
    sum_ += 1.0

t = t/sum
print t
# print cov
# print class_means
# print class_vars
# print class_std

# for i in range(0, 2):
#     cov = np.ma.cov(np.array(class_data[i]), rowvar=False)
#     class_cov.append(cov)
#     for j in range(0, len(full_data[0])):
#         class_means[i][j] = class_data[i][:][j].mean(axis=0)
#         class_vars[i][j] = class_data[i][:][j].var(axis=0)
#         class_std[i][j] = class_data[i][:][j].std(axis=0)

# print cov
# print class_means
# print class_vars
# print class_std

distros = []
hmm_states = []
state_names = ['swing', 'stance']
hmm_states = []
for i in range(0, 2):
    # print np.array(class_means[i]).shape
    # print np.array(class_cov[i]).shape
    # dis = MultivariateGaussianDistribution(np.array(class_means[i]).transpose(), class_cov[i])
    dis = MGD \
        (np.array(class_means[i]).flatten(),
         np.array(class_cov[i]))
    st = State(dis, name=state_names[i])
    distros.append(dis)
    hmm_states.append(st)
model = HMM(name="Gait")


model.add_states(hmm_states)
model.add_transition(model.start, hmm_states[0], 0.5)
model.add_transition(model.start, hmm_states[1], 0.5)

for i in range(0, 2):
    for j in range(0, 2):
        model.add_transition(hmm_states[i], hmm_states[j], t[i][j])
        # print (states[i].name+"("+str(i)+")-> "+states[j].name+"("+str(j)+") : "+str(t[i][j]))

model.bake()
# print(model)
for s in model.states:
    print s.name
skf = StratifiedKFold(full_labels, n_folds=folds)

for train_index, test_index in skf:
    print("TRAIN:", train_index, "TEST:", test_index)
    train_data = full_data[train_index]
    # print(len(train_data))
    train_class = full_labels[train_index]
    # print(len(train_class))
    test_data = full_data[test_index]
    # print(len(test_data))
    test_class = full_labels[test_index]
    # print(len(test_class))
    seq = []
    if batch_train == 1:
        for s in range(0, len(train_data)):
            k = 0
            seq_entry = []
            while k < 10 and s < len(train_data):
                seq_entry.append(train_data[s])
                k += 1
            seq.append(seq_entry)
    else:
        seq = train_data
    # model.fit(list([train_data]), algorithm='baum-welch', verbose='True')
    # seq = train_data
    model.fit(seq, algorithm='baum-welch', verbose='True')
    # print(model)
    log, path = model.viterbi(test_data)
    print len(path)
    sum_ = 0.0
    for i in range(0, len(path)-1):
        if path[i+1][1].name != 'Gait-start' and path[i+1][1].name != 'Gait-end':
            # print path[i][1].name
            # print test_class[i]
            if path[i+1][1].name == state_names[test_class[i]]:
                sum_ += 1.0
    stats.append(sum_ / float(str(len(test_data))))
    print str(sum_) + "/" + str(len(test_data))
    print sum_ / float(str(len(test_data)))
    print '------------------------------------'
scio.savemat('stats.mat', {'stats': stats})
