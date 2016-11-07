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

for s in models:
    rospy.logwarn(s)

for model in models:

    TP = 0.0
    TN = 0.0
    FP = 0.0
    FN = 0.0
    rospy.logwarn(model)
    if "btr" not in model:
        batch_training = 0
    else:
        batch_training = 1
    rospy.logwarn("Batch Training :"+str(batch_training))
    if "bte" not in model:
        batch_test = 0
    else:
        batch_test = 1
    rospy.logwarn("Batch Testing :" + str(batch_test))

    full_data = model[:len(model)-12]+"full_data.p"
    full_labels = model[:len(model)-12]+"full_labels.p"
    stats = model[:len(model)-12]+"stats.p"

    fd = np.array(pickle.load(open(full_data, 'rb')))
    fd = fd / fd.max(axis=0)
    print('Loaded : '+full_data)
    fl = np.array(pickle.load(open(full_labels, 'rb')))
    print('Loaded : ' + full_labels)


    # try:
    #     cl = pickle.load(open(model, 'rb'))
    # except ValueError:
    #     rospy.logerr("Error loading " + model)
    #     continue
    # except numpy.linalg.linalg.LinAlgError as err:
    #     rospy.logerr("LinAlgError "+str(err))
    # print('Loaded : ' + model)

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
    tests = 0
    skf = StratifiedKFold(fl, n_folds=folds, shuffle=False, random_state=None)
    for train_index, test_index in skf:

        cl = HMM(name="Gait")
        distros = []
        hmm_states = []
        state_names = ['swing', 'stance']

        positive_data = []
        negative_data = []
        for i in range(0, len(fl)):
            if fl[i] == 1:
                positive_data.append(fd[i])
            else:
                negative_data.append(fd[i])

        posdis = MGD.from_samples(positive_data)
        st = State(posdis, name='swing')
        distros.append(st)
        hmm_states.append(st)
        negdis = MGD.from_samples(negative_data)
        st2 = State(negdis, name='stance')
        distros.append(st2)
        hmm_states.append(st2)

        cl.add_states(hmm_states)
        cl.add_transition(cl.start, hmm_states[0], 0.5)
        cl.add_transition(cl.start, hmm_states[1], 0.5)

        for i in range(0, 2):
            for j in range(0, 2):
                cl.add_transition(hmm_states[i], hmm_states[j], t[i][j])
        cl.bake()


        # print("TRAIN:", train_index, "TEST:", test_index)
        # rospy.logwarn("Fold #"+str(f))
        f += 1
        train_data = fd[train_index]
        train_class = fl[train_index]
        test_data = fd[test_index]
        test_class = fl[test_index]
        seq = []
        if batch_training == 1:
            s = 0
            while s < len(train_data):
                k = 0
                seq_entry = []
                while k < 20 and s < len(train_data):
                    seq_entry.append(train_data[s])
                    k += 1
                    s += 1
                seq.append(seq_entry)
        else:
            seq = train_data

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
                    seq_entry2.append(test_data[s])
                    k += 1
                    s += 1
                seq2.append(seq_entry2)
        else:
            seq2 = test_data

        if seq2 == [] or test_data == []:
            rospy.logerr("Empty testing sequence")
            continue

        print np.array(seq).shape
        print np.array(seq[0]).shape
        # print np.array(seq)
        print np.array(seq2).shape
        print np.array(seq2[0]).shape
        # print np.array(seq2)
        # seq = np.array(seq)
        seq2 = np.array(seq2)
        # rospy.logwarn(seq)
        cl.fit(seq, algorithm='baum-welch', verbose='True')
        # print(model)


        rospy.logwarn("Start Viterbi")
        log, path = cl.viterbi(seq)
        rospy.logwarn("Viterbi Done")
        # rospy.logwarn(len(path))
        sum_ = 0.0

        if (len(path)-1) != len(test_data):
            print len(path)
            print path[0][1].name
            print path[len(path) - 1][1].name
            print len(test_data)
            exit()

        tests += 1
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
    pickle.dump(cl, open(model, 'wb'))
    pickle.dump([TP*tests, TN*tests, FP*tests, FN*tests, tests, accuracy, sensitivity, specificity], open(stats, 'wb'))

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
