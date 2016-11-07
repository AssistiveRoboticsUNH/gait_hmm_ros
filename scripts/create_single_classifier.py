#!/usr/bin/env python
import rospy
import rospkg
import pickle
import numpy as np
import matlab.engine
from sklearn.cross_validation import StratifiedKFold
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from scipy import io as scio

rospy.init_node('single_classifier')

normalized = rospy.get_param("~norm", 0)
folds = rospy.get_param("~folds", 10)
datafile = rospy.get_param("~datafile", "")
prefix = rospy.get_param("~prefix", "")

if datafile == "":
    rospy.logerr("No datafile found, exiting")
    exit()
if prefix == "":
    rospy.logerr("No prefix found, exiting")
    exit()


rospack = rospkg.RosPack()
fpath = rospack.get_path('gait_hmm_ros') + '/scripts/new_bags/datasets/' + prefix + '_'
datafile = fpath+datafile
full_data = []
full_labels = []
class_data = [[] for x in range(0, 2)]
stats = []

if "bte" in datafile:
    batch_test = 1
else:
    batch_test = 0

if "btr" in datafile:
    batch_train = 1
else:
    batch_train = 0

if datafile == "":
    rospy.warn("No input file given, exiting")
    exit()

rospy.logwarn("Normalized data : "+str(normalized))
rospy.logwarn("Folds : "+str(folds))
rospy.logwarn("Datafile : "+datafile)
rospy.logwarn("Batch Training : " + str(batch_train))
rospy.logwarn("Batch Testing : " + str(batch_test))

if normalized == 0:
    full_data = scio.loadmat(datafile + "full_data.mat")
    full_data = full_data.get("full_data")
else:
    full_data = scio.loadmat(datafile + "full_data_normalized.mat")
    full_data = full_data.get("full_data_normalized")

full_labels = scio.loadmat(datafile + "annotation_labels.mat")
full_labels = full_labels.get("labels")

t = np.zeros((2, 2))

for i in range(0, len(full_data)):
    if full_labels[i] == 0:
        class_data[0].append(full_data[i])
    else:
        class_data[1].append(full_data[i])

t = np.zeros((2, 2))
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


skf = StratifiedKFold(full_labels, n_folds=folds)

TP = 0.0
TN = 0.0
FP = 0.0
FN = 0.0

tests = 0
for train_index, test_index in skf:

    classifier = HMM(name="Gait")
    hmm_states = []

    for i in range(0, 2):
        # dis = MGD(np.array(class_means[i]).flatten(), np.array(class_cov[i]))
        dis = MGD.from_samples(class_data[i])
        st = State(dis, name=state_names[i])
        distros.append(dis)
        hmm_states.append(st)

    classifier.add_states(hmm_states)
    classifier.add_transition(classifier.start, hmm_states[0], 0.5)
    classifier.add_transition(classifier.start, hmm_states[1], 0.5)

    for i in range(0, 2):
        for j in range(0, 2):
            classifier.add_transition(hmm_states[i], hmm_states[j], t[i][j])

    classifier.bake()
    rospy.logwarn("Baked model")
    print("TRAIN:", train_index, "TEST:", test_index)
    train_data = full_data[train_index]
    train_class = full_labels[train_index]
    test_data = full_data[test_index]
    test_class = full_labels[test_index]
    seq = []

    if batch_train == 1:
        for s in range(0, len(test_data)):
            k = 0
            seq_entry = []
            while k < 20 and s < len(train_data):
                seq_entry.append(train_data[s])
                k += 1
                s += 1
            seq.append(seq_entry)
    else:
        seq = train_data

    # Check for empty seq
    if seq == []:
        rospy.logerr("Empty fitting sequence")
        continue

    classifier.fit(seq, algorithm='baum-welch', verbose='True')

    seq = []
    if batch_test == 1:
        for s in range(0, len(test_data)):
            k = 0
            seq_entry = []
            while k < 20 and s < len(test_data):
                seq_entry.append(test_data[s])
                k += 1
                s += 1
            seq.append(seq_entry)
    else:
        seq = test_data

    if seq == [] or test_data == []:
        rospy.logerr("Empty testing sequence")
        continue

    rospy.logwarn("Start Viterbi")
    log, path = classifier.viterbi(seq)
    rospy.logwarn("Viterbi Done")
    # rospy.logwarn(len(path))
    if (len(path) - 1) != len(test_data):
        rospy.logerr(len(path))
        rospy.logerr(path[0][1].name)
        rospy.logerr(path[len(path) - 1][1].name)
        rospy.logerr(len(test_data))
        exit()

    tests += 1
    sum_ = 0.0
    for i in range(0, len(path) - 1):
        if path[i + 1][1].name != 'Gait-start' and path[i + 1][1].name != 'Gait-end':
            if path[i + 1][1].name == 'swing':  # prediction is 0
                if test_class[i] == 0:  # class is 0
                    TN += 1.0
                elif test_class[i] == 1:
                    FN += 1.0  # class is 1
            elif path[i + 1][1].name == 'stance':  # prediction is 1
                if test_class[i] == 1:  # class is 1
                    TP += 1.0
                elif test_class[i] == 0:  # class is 0
                    FP += 1.0
    # print str(sum_) + "/" + str(len(test_data))
    # print sum_ / float(str(len(test_data)))
    # print '------------------------------------'

TP /= tests
TN /= tests
FP /= tests
FN /= tests
rospy.logwarn("TP :" + str(TP))
rospy.logwarn("TN :" + str(TN))
rospy.logwarn("FP :" + str(FP))
rospy.logwarn("FN :" + str(FN))
rospy.logwarn("Tests :" + str(tests))
if (TP+FN) != 0.0:
    sensitivity = TP/(TP + FN)
else:
    sensitivity = 0.0
if (TN + FP) != 0.0:
    specificity = TN/(TN + FP)
else:
    specificity = 0.0
if (TN + TP + FN + FP) != 0.0:
    accuracy = (TN + TP)/(TN + TP + FN + FP)
else:
    accuracy = 0.0

rospy.logwarn("----------------------------------------------------------")
rospy.logwarn(accuracy)
rospy.logwarn(sensitivity)
rospy.logwarn(specificity)
stats = [TP*tests, TN*tests, FP*tests, FN*tests, tests, accuracy, sensitivity, specificity]
pickle.dump(classifier, open(datafile+"classifier.p", 'wb'))
pickle.dump(stats, open(datafile+"stats.p", 'wb'))
scio.savemat(datafile+"stats.mat", {'stats': stats})
