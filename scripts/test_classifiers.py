#!/usr/bin/env python
import rospy
import rospkg
import pickle
import glob
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD

rospy.init_node('classifier_test')
rospack = rospkg.RosPack()
method = rospy.get_param('~method', "batch")
folds = 10
max_sensitivity = 0.0
max_sensitivity_model = ''
max_sensitivity_model_accuracy = 0.0
max_sensitivity_model_sensitivity = 0.0
max_sensitivity_model_specificity = 0.0

max_specificity = 0.0
max_specificity_model = 0.0
max_specificity_model_accuracy = 0.0
max_specificity_model_sensitivity = 0.0
max_specificity_model_specificity = 0.0

max_accuracy = 0.0
max_accuracy_model = ''
max_accuracy_model_accuracy = 0.0
max_accuracy_model_sensitivity = 0.0
max_accuracy_model_specificity = 0.0

if method == "batch":
    fpath = rospack.get_path('gait_hmm_ros') + '/scripts/trained_classifiers/*classifier.p'
    models = glob.glob(fpath)
else:
    fpath = rospack.get_path('gait_hmm_ros') + '/scripts/trained_classifiers/'+method+'classifier.p'
    models = [fpath]

for model in models:

    TP = 0.0
    TN = 0.0
    FP = 0.0
    FN = 0.0

    full_data = model[:len(model)-12]+"full_data.p"
    full_labels = model[:len(model)-12]+"full_labels.p"

    fd = pickle.load(open(full_data, 'rb'))
    print('Loaded : '+full_data)
    fl = pickle.load(open(full_labels, 'rb'))
    print('Loaded : ' + full_labels)
    try:
        cl = pickle.load(open(model, 'rb'))
    except ValueError:
        rospy.logerr("Error loading " + model)
        continue
    print('Loaded : ' + model)
    f = 0
    skf = StratifiedKFold(fl, n_folds=folds, shuffle=False, random_state=None)
    for train_index, test_index in skf:
        # print("TRAIN:", train_index, "TEST:", test_index)
        # rospy.logwarn("Fold #"+str(f))
        f += 1
        train_data = fd[train_index]
        train_class = fl[train_index]
        test_data = fd[test_index]
        test_class = fl[test_index]
        seq = []
        for s in range(0, len(test_data)):
            k = 0
            seq_entry = []
            while k < 20 and s < len(test_data):
                seq_entry.append(test_data[s])
                k += 1
            seq.append(seq_entry)
        log, path = cl.viterbi(test_data)
        if (len(path)-1) != len(test_data):
            print len(path)
            print path[0][1].name
            print path[len(path) - 1][1].name
            print len(test_data)
            exit()
        for i in range(0, len(path) - 1):
            if path[i + 1][1].name != 'Gait-start' and path[i + 1][1].name != 'Gait-end':
                if path[i + 1][1].name == 'swing':
                    if test_class[i] == 0:
                        TN += 1.0
                    else:
                        FP += 1.0
                else:
                    if test_class[i] == 0:
                        FN += 1.0
                    else:
                        TP += 1.0
    if (TP+FN) != 0:
        sensitivity = TP/(TP + FN)
    if (TN + FP) != 0:
        specificity = TN/(TN + FP)
    if (TN + TP + FN + FP) != 0:
        accuracy = (TN + TP)/(TN + TP + FN + FP)

    if specificity > max_specificity:
        max_specificity = specificity
        max_specificity_model = model
        max_specificity_model_accuracy = accuracy
        max_specificity_model_sensitivity = sensitivity
        max_specificity_model_specificity = specificity
    if sensitivity > max_sensitivity:
        max_sensitivity = sensitivity
        max_sensitivity_model = model
        max_sensitivity_model_accuracy = accuracy
        max_sensitivity_model_sensitivity = sensitivity
        max_sensitivity_model_specificity = specificity
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        max_accuracy_model = model
        max_accuracy_model_accuracy = accuracy
        max_accuracy_model_sensitivity = sensitivity
        max_accuracy_model_specificity = specificity

print("------------------------------------------------------------------------")
rospy.logwarn("Max Accuracy : " + str(max_accuracy) + " from " + max_accuracy_model)
rospy.logwarn("Accuracy : " + str(max_accuracy_model_accuracy))
rospy.logwarn("Sensitivity : " + str(max_accuracy_model_sensitivity))
rospy.logwarn("Specificity : " + str(max_accuracy_model_specificity))
print("------------------------------------------------------------------------")
rospy.logwarn("Max Sensitivity : " + str(max_sensitivity) + " from " + max_sensitivity_model)
rospy.logwarn("Accuracy : " + str(max_sensitivity_model_accuracy))
rospy.logwarn("Sensitivity : " + str(max_sensitivity_model_sensitivity))
rospy.logwarn("Specificity : " + str(max_sensitivity_model_specificity))
print("------------------------------------------------------------------------")
rospy.logwarn("Max Specificity: " + str(max_specificity) + " from " + max_specificity_model)
rospy.logwarn("Accuracy : " + str(max_specificity_model_accuracy))
rospy.logwarn("Sensitivity : " + str(max_specificity_model_sensitivity))
rospy.logwarn("Specificity : " + str(max_specificity_model_specificity))
