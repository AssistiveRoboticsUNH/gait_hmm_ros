#!/usr/bin/env python
import rospy
import rospkg
import pickle
import numpy as np
# from sklearn.cross_validation import StratifiedKFold
from sklearn.model_selection import StratifiedKFold
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from scipy import io as scio


class DisClassifier:

    def prepare_data(self):
        self.class_data = [[[] for x_ in range(0, 2)] for y in]
        rospy.logwarn("Normalized data : "+str(self.normalized))
        rospy.logwarn("Folds : "+str(self.folds))
        rospy.logwarn("Datafile : "+str(self.datafile))
        rospy.logwarn("Batch Training : "+str(self.batch_train))
        rospy.logwarn("Batch Testing : "+str(self.batch_test))

        if self.normalized == 0:
            rospy.logwarn(self.datafile+"full_data.mat")
            self.full_data = scio.loadmat(self.datafile+"full_data.mat")
            self.full_data = self.full_data.get("data")
        else:
            rospy.logwarn(self.datafile + "full_data_normalized.mat")
            self.full_data = scio.loadmat(self.datafile + "full_data_normalized.mat")
            self.full_data = self.full_data.get("data")

        if(self.full_data is None) or (self.full_data == []):
            rospy.logerr("No data found, exiting")
            rospy.shutdown()
            exit()

        self.full_labels = scio.loadmat(self.labelfile)
        self.full_labels = self.full_labels.get("labels")
        self.full_labels = self.full_labels[0]
        print self.full_labels
        for i in range(0, len(self.full_data)):
            if self.full_labels[i] == 0:
                self.class_data[0].append((self.full_data[i]))
            else:
                self.class_data[0].append((self.full_data[i]))

        print np.array(self.class_data[0]).shape
        print np.array(self.class_data[1]).shape
        self.t = np.zeros((2, 2))
        sum_ = 0
        prev = -1

        for i in range(0, len(self.full_labels)):
            if prev == -1:
                prev = self.full_labels[i]
            self.t[prev][self.full_labels[i]] += 1.0
            prev = self.full_labels[i]
            sum_ += 1.0

        self.t = self.t/sum_
        print("Transition probabilities")
        print self.t

    def build_dis_classifier(self):
        skf = StratifiedKFold(self.full_labels, n_folds=self.folds)
        classifier_array = []
        stats_array = []
        num_class = len(self.full_data[0])
        print num_class
        exit()
        for cl in range(0, num_class):
            lel = -1
            tp_total = 0.0
            tn_total = 0.0
            fp_total = 0.0
            fn_total = 0.0
            tests = 0
            for train_index, test_index in skf:
                if lel > 0:
                    lel -= 1
                    continue
                stats = []
                distros = []
                hmm_states = []
                state_names = ['swing', 'stance']
                swings = 0
                stances = 0
                for i in range(0, 2):
                    dis = MGD.from_samples(self.class_data[i])
                    st = State(dis, name=state_names[i])
                    distros.append(dis)
                    hmm_states.append(st)

                model = HMM()
                print(model.states)
                model.add_states(hmm_states)
                model.add_transition(model.start, hmm_states[0], 0.5)
                model.add_transition(model.start, hmm_states[1], 0.5)
                model.add_transition(hmm_states[1], model.end, 0.000000000000000001)
                model.add_transition(hmm_states[0], model.end, 0.000000000000000001)

                for i in range(0, 2):
                    for j in range(0, 2):
                        model.add_transition(hmm_states[i], hmm_states[j], self.t[i][j])
                model.bake()

                tp = 0.0
                tn = 0.0
                fp = 0.0
                fn = 0.0

                train_data = self.full_data[train_index, cl]
                train_class = self.full_labels[train_index, cl]
                test_data = self.full_data[test_index]
                test_class = self.full_labels[test_index]

                print(np.isfinite(train_data).all())
                print(np.isfinite(test_data).all())
                print(np.isnan(train_data.any()))
                print(np.isinf(train_data.any()))
                print(np.isnan(test_data.any()))
                print(np.isinf(test_data.any()))

                if (not np.isfinite(train_data.any())) or (not np.isfinite(test_data.any())) \
                        or (not np.isfinite(train_class.any())) or (not np.isfinite(test_data.any())):
                    rospy.logerr("NaN or Inf Detected")
                    exit()

                try:
                    rospy.logwarn("Training model #"+str(cl)+", fold #" + str(tests))
                    seq = np.array(train_data)
                    model.fit(seq, algorithm='baum-welch', verbose='True', n_jobs=8, max_iterations=150)

                except ValueError:
                    rospy.logwarn("Something went wrong, exiting")
                    rospy.shutdown()
                    exit()

                seq = []
                if self.batch_test == 1:
                    s = 0
                    # for s in range(0, len(test_data)):
                    while s < len(test_data):
                        k = 0
                        seq_entry = []
                        while k < 20 and s < len(test_data):
                            seq_entry.append(test_data[s])
                            k += 1
                            s += 1
                        seq.append(seq_entry)
                else:
                    seq = np.array(test_data)

                if seq == [] or test_data == []:
                    rospy.logerr("Empty testing sequence")
                    continue

                log, path = model.viterbi(test_data)
                if (len(path) - 2) != len(test_data):
                    rospy.logerr(len(path))
                    rospy.logerr(path[0][1].name)
                    rospy.logerr(path[len(path) - 1][1].name)
                    rospy.logerr(len(test_data))
                    exit()

                tests += 1
                for i in range(0, len(path) - 2):
                    if path[i + 1][1].name != 'Gait-start' and path[i + 1][1].name != 'Gait-end':
                        if path[i + 1][1].name == 'swing':  # prediction is 0
                            swings += 1
                            if test_class[i] == 0:  # class is 0
                                tn += 1.0
                            elif test_class[i] == 1:
                                fn += 1.0  # class is 1

                        elif path[i + 1][1].name == 'stance':  # prediction is 1
                            stances += 1
                            if test_class[i] == 1:  # class is 1
                                tp += 1.0
                            elif test_class[i] == 0:  # class is 0
                                fp += 1.0
                print swings
                print stances
                if (tp + fn) != 0.0:
                    rospy.logwarn("Sensitivity : " + str(tp / (tp + fn)))
                    # sensitivity = tp / (tp + fn)
                else:
                    rospy.logwarn("Sensitivity : 0.0")
                    # sensitivity = 0.0
                if (tn + fp) != 0.0:
                    rospy.logwarn("Specificity : " + str(tn / (tn + fp)))
                    # specificity = tn_total / (tn_total + fp_total)
                else:
                    rospy.logwarn("Specificity : 0.0")
                    # specificity = 0.0
                if (tn + tp + fn + fp) != 0.0:
                    rospy.logwarn("Accuracy : " + str((tn + tp) / (tn + tp + fn + fp)))
                    # accuracy = (tn + tp) / (tn + tp + fn + fp)
                else:
                    rospy.logwarn("Accuracy : 0.0")
                    # accuracy = 0.0

                tn_total += tn
                tp_total += tp
                fn_total += fn
                fp_total += fp

            tp_total /= tests
            tn_total /= tests
            fp_total /= tests
            fn_total /= tests
            rospy.logerr("TP :" + str(tp_total))
            rospy.logerr("TN :" + str(tn_total))
            rospy.logerr("FP :" + str(fp_total))
            rospy.logerr("FN :" + str(fn_total))
            rospy.logerr("Tests :" + str(tests))
            if (tp_total + fn_total) != 0.0:
                sensitivity = tp_total / (tp_total + fn_total)
            else:
                sensitivity = 0.0
            if (tn_total + fp_total) != 0.0:
                specificity = tn_total / (tn_total + fp_total)
            else:
                specificity = 0.0
            if (tn_total + tp_total + fn_total + fp_total) != 0.0:
                accuracy = (tn_total + tp_total) / (tn_total + tp_total + fn_total + fp_total)
            else:
                accuracy = 0.0

            rospy.logwarn("----------------------------------------------------------")
            rospy.logerr("Total accuracy: " + str(accuracy))
            rospy.logerr("Total sensitivity: " + str(sensitivity))
            rospy.logerr("Total specificity: " + str(specificity))
            stats = [tn_total * tests, fn_total * tests, fp_total * tests, fn_total * tests, tests,
                     accuracy, sensitivity, specificity]
            # pickle.dump(model, open(datafile + "classifier.p", 'wb'))
            # pickle.dump(stats, open(datafile + "stats.p", 'wb'))
            # scio.savemat(datafile + "stats.mat", {'stats': stats})
            rospy.logwarn("-------------------DONE-------------------------")
            classifier_array.append(model)
            stats_array.append(stats)

        pickle.dump(classifier_array, open(datafile + "distributed_classifiers.p", 'wb'))
        pickle.dump(stats_array, open(datafile + "distributed_stats.p", 'wb'))
        scio.savemat(datafile + "distributed_stats.mat", {'stats': stats_array})

    def __init__(self, _normalized=0, _folds=10, _datafile="", _labelfile="", _prefix="",
                 _bte=0, _btr=0, prep_data=prepare_data, build_class=build_dis_classifier):
        self.normalized = _normalized
        self.folds = _folds
        self.datafile = _datafile
        self.labelfile = _labelfile
        self.prefix = _prefix
        self.batch_test = _bte
        self.batch_train = _btr
        self.full_data = []
        self.full_labels = []
        self.t = []
        self.class_data = []
        prep_data(self)
        build_class(self)
        pass

if __name__ == "main":
    rospy.init_node('distributed_classifier')
    rospack = rospkg.RosPack()
    normalized = rospy.get_param("~norm", 0)
    folds = rospy.get_param("~folds", 10)
    datafile = "quat_gyro_accel_com_fsr_ir_prox_btr_bte_rf_rll_rul_m_"
    prefix = rospy.get_param("~prefix", "")
    if prefix == "":
        rospy.logerr("No prefix found, exiting")
        exit()

    labelfile = rospack.get_path('gait_hmm_ros') + '/scripts/new_bags/datasets/' + prefix + '_labels.mat'
    fpath = rospack.get_path('gait_hmm_ros') + '/scripts/new_bags/datasets/' + prefix + '_'
    datafile = fpath + datafile
    if datafile == "":
        rospy.logerr("No input file given, exiting")
        exit()

    if "bte" in datafile:
        batch_test = 1
    else:
        batch_test = 0

    if "btr" in datafile:
        batch_train = 1
    else:
        batch_train = 0
    x = DisClassifier(normalized, folds, datafile, labelfile, prefix, batch_test, batch_train)


