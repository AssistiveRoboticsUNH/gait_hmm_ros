#!/usr/bin/env python
import rospy
import rospkg
import pickle
import numpy as np
import imu_callbacks as iparam
import matlab.engine
from threespace_ros.msg import dataVec
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import normalize
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from scipy import io as scio

rospy.init_node('dis_class_2')
input_names = []
device_names = []
imus_used = ""
joint_names = []
pref = rospy.get_param('~prefix', "none")
use_quat = rospy.get_param('~use_quat', 0)
if use_quat == 1:
    input_names.append("quat")
    imus_used += "quat_"
use_gyro = rospy.get_param('~use_gyro', 0)
if use_gyro == 1:
    input_names.append("gyro")
    imus_used += "gyro_"
use_accel = rospy.get_param('~use_accel', 0)
if use_accel == 1:
    input_names.append("accel")
    imus_used += "accel_"
use_com = rospy.get_param('~use_com', 0)
if use_com == 1:
    input_names.append("com")
    imus_used += "com_"
use_fsr = rospy.get_param('~use_fsr', 0)
if use_fsr == 1:
    input_names.append("fsr")
    imus_used += "fsr_"
use_ir = rospy.get_param('~use_ir', 0)
if use_ir == 1:
    input_names.append("ir")
    imus_used += "ir_"
use_prox = rospy.get_param('~use_prox', 0)
if use_prox == 1:
    input_names.append("prox")
    imus_used += "prox_"
folds = rospy.get_param('~folds', 10)
batch_train = rospy.get_param('~batch_train', 1)
if batch_train == 1:
    imus_used += "btr_"
batch_test = rospy.get_param('~batch_test', 1)
if batch_test == 1:
    imus_used += "bte_"

rf = rospy.get_param('~rf', "")
if rf != "":
    joint_names.append("rf")

rll = rospy.get_param('~rll', "")
if rll != "":
    joint_names.append("rll")

rul = rospy.get_param('~rll', "")
if rul != "":
    joint_names.append("rul")

m = rospy.get_param('~m', "")
if m != "":
    joint_names.append("m")

rospack = rospkg.RosPack()
fpath = rospack.get_path('gait_hmm_ros') + '/scripts/'
stats = []
print("Use quat: "+str(use_quat))
print("Use gyro: "+str(use_gyro))
print("Use accel: "+str(use_accel))
print("Use com: "+str(use_com))
print("Use fsr: "+str(use_fsr))
print("Use ir: "+str(use_ir))
print("Use prox: "+str(use_prox))
print("Folds: "+str(folds))
print("Batch train: "+str(batch_train))
print("Batch test: "+str(batch_test))
print("Right Foot Topic: "+rf)
print("Right Lower Leg Topic: "+rll)
print("Right Upper Leg Foot Topic: "+rul)
print("Waist Foot Topic: "+m)
print joint_names

names = ['andreas1', 'andreas2', 'andreas3', 'andreas4', 'andreas5']

imu_names = iparam.imu_param_names

total_sensors = len(imu_names)
total_entries = 0

max_acc = 0.0

sum = 0

full_data = []
full_labels = []
class_data = [[] for x in range(0, 2)]

# eng = matlab.engine.start_matlab()
# eng.sqrt(2.0)
# eng.evalfis([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], eng.workspace['an1'], nargout=0)
# anfis = eng.workspace['an1']
# fis = eng.test_anfis_2('fsr_anfis_with_ir_prox_chk.mat', 0.4, 20, 1, 20, 0.9, nargout=0)
# exit()

#####################
# Load enabled IMUS #
#####################
for filename in names:
    sensor_data = []
    pref = fpath + filename
    for name in joint_names:
        full_name = pref + "_" + name + ".mat"
        # rospy.logwarn(full_name)
        if os.path.isfile(full_name):
            if name not in imus_used:
                imus_used += (name + "_")
            # rospy.logwarn("Loading" + full_name)
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
                # rospy.logwarn(len(entry))
                data_entry.append(entry)
            # rospy.logwarn(len(data_entry))
            if sensor_data == []:
                sensor_data = data_entry
            else:
                sensor_data = np.concatenate((sensor_data, data_entry), axis=1)
                rospy.logwarn(total_entries)
    x = []
    arduino = scio.loadmat(pref + "_arduino.mat")
    arduino = arduino.get("arduino")
    arduino_data = []
    # rospy.logwarn(arduino)
    # rospy.logwarn(len(arduino))
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
    sensor_data = np.concatenate((sensor_data, arduino_data), axis=1)
    labels = scio.loadmat(pref+"_labels_mocap_annotated.mat")
    labels = labels.get("labels")
    labels = labels[0]
    if full_data == []:
        full_data = sensor_data
    else:
        full_data = np.concatenate((full_data, sensor_data), axis=0)
    sum += len(sensor_data)

    if full_labels == []:
        full_labels = labels
    else:
        full_labels = np.concatenate((full_labels, labels), axis=0)

rospy.logwarn(full_name)
rospy.logwarn(imus_used)

labels = []
sensor_data = []

startprob = [0.5, 0.5]

for i in range(0, len(full_data)):
    if full_labels[i] == 0:
        class_data[0].append(full_data[i])
    else:
        class_data[1].append(full_data[i])

# class_means = [[[] for x in range(len(full_data[0]))] for i in range(0, 2)]
# class_vars = [[[] for x in range(len(full_data[0]))] for i in range(0, 2)]
# class_std = [[[] for x in range(len(full_data[0]))] for i in range(0, 2)]
# class_cov = []
# classifiers = []

pickle.dump(full_data, open(fpath+"/trained_classifiers/"+imus_used+"full_data.p", 'wb'))
pickle.dump(full_labels, open(fpath+"/trained_classifiers/"+imus_used+"full_labels.p", 'wb'))

# for i in range(0, 2):
#     cov = np.ma.cov(np.array(class_data[i]), rowvar=False)
#     class_cov.append(cov)
#     for j in range(0, len(full_data[0])):
#         class_means[i][j] = np.array(class_data[i][:])[:, [j]].mean(axis=0)
#         class_vars[i][j] = np.array(class_data[i][:])[:, [j]].var(axis=0)
#         class_std[i][j] = np.array(class_data[i][:])[:, [j]].std(axis=0)
#         if np.isnan(np.sum(class_means[i][j])) or np.isnan(np.sum(class_vars[i][j])) or np.isnan(np.sum(class_std[i][j])):
#             rospy.logerr("NAN OR inf values")
#             exit()

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

distros = []
hmm_states = []
state_names = ['swing', 'stance']
hmm_states = []
for i in range(0, 2):
    # print np.array(class_means[i]).shape
    # print np.array(class_cov[i]).shape
    # dis = MultivariateGaussianDistribution(np.array(class_means[i]).transpose(), class_cov[i])
    # dis = MGD(np.array(class_means[i]).flatten(), np.array(class_cov[i]))
    dis = MGD.from_samples(class_data[i])
    st = State(dis, name=state_names[i])
    distros.append(dis)
    hmm_states.append(st)

    # print (states[i].name+"("+str(i)+")-> "+states[j].name+"("+str(j)+") : "+str(t[i][j]))

# model.bake()
# print(model)
# for s in model.states:
#    print s.name

skf = StratifiedKFold(full_labels, n_folds=folds)

for train_index, test_index in skf:

    model = HMM(name="Gait")
    hmm_states = []
    
    for i in range(0, 2):
        # dis = MGD(np.array(class_means[i]).flatten(), np.array(class_cov[i]))
        dis = MGD.from_samples(class_data[i])
        st = State(dis, name=state_names[i])
        distros.append(dis)
        hmm_states.append(st)

    model.add_states(hmm_states)
    model.add_transition(model.start, hmm_states[0], 0.5)
    model.add_transition(model.start, hmm_states[1], 0.5)

    for i in range(0, 2):
        for j in range(0, 2):
            model.add_transition(hmm_states[i], hmm_states[j], t[i][j])

    model.bake()
    rospy.logwarn("Baked model")
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
            while k < 20 and s < len(train_data):
                seq_entry.append(train_data[s])
                k += 1
            seq.append(seq_entry)
    else:
        seq = train_data
    # model.fit(list([train_data]), algorithm='baum-welch', verbose='True')
    # seq = train_data

    # Check for empty seq
    if seq == []:
        rospy.logerr("Empty fitting sequence")
        continue

    model.fit(seq, algorithm='baum-welch', verbose='True')
    # print(model)

    seq = []
    if batch_test == 1:
        for s in range(0, len(test_data)):
            k = 0
            seq_entry = []
            while k < 20 and s < len(test_data):
                seq_entry.append(test_data[s])
                k += 1
            seq.append(seq_entry)
    else:
        seq = test_data

    if seq == [] or test_data == []:
        rospy.logerr("Empty testing sequence")
        continue

    rospy.logwarn("Start Viterbi")
    log, path = model.viterbi(seq)
    rospy.logwarn("Viterbi Done")
    # rospy.logwarn(len(path))
    sum_ = 0.0
    for i in range(0, len(path)-1):
        if path[i+1][1].name != 'Gait-start' and path[i+1][1].name != 'Gait-end':
            # print path[i][1].name
            # print test_class[i]
            if path[i+1][1].name == state_names[test_class[i]]:
                sum_ += 1.0
    acc = sum_ / float(str(len(test_data)))
    if acc > max_acc:
        max_acc = acc
        classifier = model
    stats.append(sum_ / float(str(len(test_data))))
    # print str(sum_) + "/" + str(len(test_data))
    # print sum_ / float(str(len(test_data)))
    # print '------------------------------------'
    pickle.dump(classifier, open(fpath+"/trained_classifiers/"+imus_used+"classifier.p", 'wb'))
pickle.dump(classifier, open(fpath+"/trained_classifiers/"+imus_used+"classifier.p", 'wb'))
scio.savemat('stats.mat', {'stats': stats})
