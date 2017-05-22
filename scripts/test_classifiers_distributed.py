#!/usr/bin/env python
import rospy
import rospkg
import pickle
import glob
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from pomegranate import *
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from pomegranate import NormalDistribution as ND
from pomegranate import UniformDistribution as UD

rospy.init_node('classifier_test_distributed')
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
    fpath = rospack.get_path('gait_hmm_ros') + '/scripts/trained_classifiers/' + method + 'classifier.p'
    models = [fpath]

for s in models:
    rospy.logwarn(s)

for model in models:

    TP = 0.0
    TN = 0.0
    FP = 0.0
    FN = 0.0
    model = "/home/lydakis-local/ros_ws/src/" \
            "gait_hmm_ros/scripts/trained_classifiers" \
            "/quat_gyro_accel_bte_rf_rll_rul_m_classifier.p"
    rospy.logwarn(model)
    if "btr" not in model:
        batch_training = 0
    else:
        batch_training = 1
    rospy.logwarn("Batch Training :" + str(batch_training))
    if "bte" not in model:
        batch_test = 0
    else:
        batch_test = 1
    rospy.logwarn("Batch Testing :" + str(batch_test))

    full_data = model[:len(model) - 12] + "full_data.p"
    full_labels = model[:len(model) - 12] + "full_labels.p"
    stats = model[:len(model) - 12] + "stats_dis.p"
    model_dis = model[:len(model) - 12] + "classifier_dis.p"

    fd = np.array(pickle.load(open(full_data, 'rb')))
    fd = fd / fd.max(axis=0)
    print('Loaded : ' + full_data)
    fl = np.array(pickle.load(open(full_labels, 'rb')))
    print('Loaded : ' + full_labels)

    #############################
    # calculate transition probs#
    #############################
    sum_ = 0
    prev = -1
    t = np.zeros((2, 2))
    for i in range(0, len(fl)):
        if prev == -1:
            prev = fl[i]
        t[prev][fl[i]] += 1.0
        prev = fl[i]
        sum_ += 1.0

    t = t / sum_
    print t

    ########################################

    f = 0
    skf = StratifiedKFold(fl, n_folds=folds, shuffle=False, random_state=None)
    tests = 0
    for train_index, test_index in skf:
        state_names = ['swing', 'stance']
        positive_data = []
        negative_data = []
        for i in range(0, len(fl)):
            if fl[i] == 1:
                positive_data.append(fd[i])
            else:
                negative_data.append(fd[i])

        negative_data = np.array(negative_data).transpose()
        positive_data = np.array(positive_data).transpose()

        positive_distributions = []
        negative_distributions = []
        classifiers = []
        distros_dis = [[] for i in range(len(positive_data))]
        hmm_states_dis = [[] for i in range(len(positive_data))]
        TP_dis = [[] for i in range(len(positive_data))]
        FP_dis = [[] for i in range(len(positive_data))]
        TN_dis = [[] for i in range(len(positive_data))]
        FN_dis = [[] for i in range(len(positive_data))]
        paths_dis = [[] for i in range(len(positive_data))]

        # CREATE ONE CLASSIFIER FOR EVERY INPUT
        for i in range(0, len(positive_data)):
            classifiers.append(HMM(name="gait_" + str(i)))
        # CREATE THE POSITIVE DISTRIBUTIONS FOR EVERY INPUT
        for i in range(0, len(positive_data)):
            posdis = ND.from_samples(positive_data[:, [i]])
            st = State(posdis, name="swing")
            distros_dis[i].append(st)
            hmm_states_dis[i].append(st)

        # CREATE THE NEGATIVE DISTRIBUTIONS FOR EVERY INPUT
        for i in range(0, len(negative_data)):
            # print (negative_data[i][:])
            negdis = ND.from_samples(negative_data[:, [i]])
            st = State(negdis, name="stance")
            distros_dis[i].append(st)
            hmm_states_dis[i].append(st)

        # ADD STATES AND TRANSITION PROBABILITIES TO THE HMMs)
        for i in range(0, len(classifiers)):
            classifiers[i].add_states(hmm_states_dis[i])
            classifiers[i].add_transition(classifiers[i].start, hmm_states_dis[i][0], 0.5)
            classifiers[i].add_transition(classifiers[i].start, hmm_states_dis[i][1], 0.5)
            for j in range(0, 2):
                for k in range(0, 2):
                    classifiers[i].add_transition(hmm_states_dis[i][j], hmm_states_dis[i][k], t[j][k])
                    classifiers[i].bake()
                    # print classifiers[i]

        f += 1
        # CREATE TESTING AND TRAINING DATA
        train_data = fd[train_index]
        train_class = fl[train_index]
        test_data = fd[test_index]
        test_class = fl[test_index]
        # FIT AND TEST MODEL
        print (len(train_data))
        print (len(test_data))
        for i in range(0, len(classifiers)):
            seq = []
            if batch_training == 1:
                s = 0
                while s < len(train_data):
                    k = 0
                    seq_entry = []
                    while k < 20 and s < len(train_data):
                        seq_entry.append(train_data[s][i])
                        k += 1
                        s += 1
                        print k
                    seq.append(seq_entry)
            else:
                seq = np.array(train_data[:, [i]])

            if seq == []:
                rospy.logerr("Empty fitting sequence")
                continue

            seq2 = []
            if batch_test == 1:
                s = 0
                while s < len(test_data):
                    k = 0
                    seq_entry2 = []
                    while k < 20 and s < len(test_data):
                        # print s
                        seq_entry2.append(test_data[s][i])
                        k += 1
                        s += 1
                    seq2.append(seq_entry2)
            else:
                # seq2 = test_data[:][i]
                seq2 = np.array(test_data[:, [i]])

            print (np.array(seq).shape)
            # print np.array(seq)
            print (np.array(seq2).shape)
            # print np.array(seq2)

            if seq2 == [] or test_data == []:
                rospy.logerr("Empty testing sequence")
                continue

            # rospy.logwarn(seq)
            classifiers[i].fit(seq, algorithm='baum-welch', verbose='True')

            rospy.logwarn("Start Viterbi for classifier %d/%d, fold %d", i + 1, len(classifiers), tests + 1)
            log, path = classifiers[i].viterbi(seq2)
            rospy.logwarn("Viterbi Done")
            # rospy.logwarn(len(path))
            sum_ = 0.0

            if (len(path) - 1) != len(test_data):
                print (len(path))
                print (path[0][1].name)
                print (path[len(path) - 1][1].name)
                print (len(test_data))
                exit()

            paths_dis[i] = path

        tests += 1
        # GET THE MAJORITY DECISION FOR THE CLASSIFIERS

        for p in range(0, len(path) - 1):
            if path[p + 1][1].name != 'Gait-start' and path[p + 1][1].name != 'Gait-end':
                sum_ = 0
                for i in range(0, len(classifiers)):
                    if paths_dis[i][p + 1][1].name == 'stance':
                        sum_ += 1
                if sum_ < len(classifiers) / 2:
                    pred = 0
                else:
                    pred = 1
                if pred == 0:  # prediction is 0
                    if test_class[i] == 0:  # class is 0
                        TN += 1.0
                    elif test_class[i] == 1:
                        FN += 1.0  # class is 1
                elif pred == 1:  # prediction is 1
                    if test_class[i] == 1:  # class is 1
                        TP += 1.0
                    elif test_class[i] == 0:  # class is 0
                        FP += 1.0
    TP /= tests
    TN /= tests
    FP /= tests
    FN /= tests
    rospy.logwarn("TP :" + str(TP))
    rospy.logwarn("TN :" + str(TN))
    rospy.logwarn("FP :" + str(FP))
    rospy.logwarn("FN :" + str(FN))
    rospy.logwarn("Tests :" + str(tests))
    if (TP + FN) != 0.0:
        sensitivity = TP / (TP + FN)
    else:
        sensitivity = 0.0
    if (TN + FP) != 0.0:
        specificity = TN / (TN + FP)
    else:
        specificity = 0.0
    if (TN + TP + FN + FP) != 0.0:
        accuracy = (TN + TP) / (TN + TP + FN + FP)
    else:
        accuracy = 0.0

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
    rospy.logwarn("----------------------------------------------------------")
    rospy.logwarn(accuracy)
    rospy.logwarn(sensitivity)
    rospy.logwarn(specificity)
    cl = []
    for i in range(0, len(classifiers)):
        cl.append(classifiers[i])
    pickle.dump(cl, open(model_dis, 'wb'))
    pickle.dump([TP * tests, TN * tests, FP * tests, FN * tests, tests, accuracy, sensitivity, specificity],
                open(stats, 'wb'))

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
