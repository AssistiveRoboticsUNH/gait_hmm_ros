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


class SingleClassifier:

    def prepare_data(self):
        self.full_data = []
        self.full_labels = []
        class_data = [[] for x in range(0, 2)]
        rospy.logwarn("Normalized data : " + str(self.normalized))
        rospy.logwarn("Folds : " + str(self.folds))
        rospy.logwarn("Datafile : " + self.datafile)
        rospy.logwarn("Batch Training : " + str(self.batch_train))
        rospy.logwarn("Batch Testing : " + str(self.batch_test))

        if normalized == 0:
            self.full_data = scio.loadmat(self.datafile + "full_data.mat")
            self.full_data = self.full_data.get("full_data")
        else:
            self.full_data = scio.loadmat(self.datafile + "full_data_normalized.mat")
            self.full_data = self.full_data.get("full_data_normalized")

        self.full_labels = scio.loadmat(self.datafile + "labels_annotated.mat")
        self.full_labels = self.full_labels.get("labels")

        for i in range(0, len(self.full_data)):
            if self.full_labels[i] == 0:
                class_data[0].append(self.full_data[i])
            else:
                class_data[1].append(self.full_data[i])

        self.t = np.zeros((2, 2))
        sum_ = 0
        prev = -1

        for i in range(0, len(self.full_labels)):
            if prev == -1:
                prev = self.full_labels[i]
            self.t[prev][self.full_labels[i]] += 1.0
            prev = self.full_labels[i]
            sum_ += 1.0

        self.t = self.t / sum
        print self.t
        self.class_data = [[] for x_ in range(0, 2)]

    def build_single_classifier(self):
        stats = []
        distros = []
        hmm_states = []
        state_names = ['swing', 'stance']

        skf = StratifiedKFold(self.full_labels, n_folds=self.folds)

        tp = 0.0
        tn = 0.0
        fp = 0.0
        fn = 0.0

        tests = 0
        for train_index, test_index in skf:

            classifier = HMM(name="Gait")
            hmm_states = []

            for i in range(0, 2):
                # dis = MGD(np.array(class_means[i]).flatten(), np.array(class_cov[i]))
                dis = MGD.from_samples(self.class_data[i])
                st = State(dis, name=state_names[i])
                distros.append(dis)
                hmm_states.append(st)

            classifier.add_states(hmm_states)
            classifier.add_transition(classifier.start, hmm_states[0], 0.5)
            classifier.add_transition(classifier.start, hmm_states[1], 0.5)

            for i in range(0, 2):
                for j in range(0, 2):
                    classifier.add_transition(hmm_states[i], hmm_states[j], self.t[i][j])

            classifier.bake()
            rospy.logwarn("Baked model")
            print("TRAIN:", train_index, "TEST:", test_index)
            train_data = self.full_data[train_index]
            train_class = self.full_labels[train_index]
            test_data = self.full_data[test_index]
            test_class = self.full_labels[test_index]
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
            if self.batch_test == 1:
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
                            tn += 1.0
                        elif test_class[i] == 1:
                            fn += 1.0  # class is 1
                    elif path[i + 1][1].name == 'stance':  # prediction is 1
                        if test_class[i] == 1:  # class is 1
                            tp += 1.0
                        elif test_class[i] == 0:  # class is 0
                            fp += 1.0
                            # print str(sum_) + "/" + str(len(test_data))
                            # print sum_ / float(str(len(test_data)))
                            # print '------------------------------------'

        tp /= tests
        tn /= tests
        fp /= tests
        fn /= tests
        rospy.logwarn("TP :" + str(tp))
        rospy.logwarn("TN :" + str(tn))
        rospy.logwarn("FP :" + str(fp))
        rospy.logwarn("FN :" + str(fn))
        rospy.logwarn("Tests :" + str(tests))
        if (tp + fn) != 0.0:
            sensitivity = tp / (tp + fn)
        else:
            sensitivity = 0.0
        if (tn + fp) != 0.0:
            specificity = tn / (tn + fp)
        else:
            specificity = 0.0
        if (tn + tp + fn + fp) != 0.0:
            accuracy = (tn + tp) / (tn + tp + fn + fp)
        else:
            accuracy = 0.0

        rospy.logwarn("----------------------------------------------------------")
        rospy.logwarn(accuracy)
        rospy.logwarn(sensitivity)
        rospy.logwarn(specificity)
        stats = [tn * tests, fn * tests, fp * tests, fn * tests, tests, accuracy, sensitivity, specificity]
        pickle.dump(classifier, open(datafile + "classifier.p", 'wb'))
        pickle.dump(stats, open(datafile + "stats.p", 'wb'))
        scio.savemat(datafile + "stats.mat", {'stats': stats})

    def __init__(self, normalized=0, folds=10, datafile="", prefix="",
                 bte=0, btr=0, prep_data=prepare_data, build_class=build_single_classifier):
        # use normalized or original data
        self.normalized = normalized
        # folds for cross validation
        self.folds = folds
        self.datafile = datafile
        self.prefix = prefix
        # batch testing or not
        self.batch_test = bte
        # batch training or not
        self.batch_train = btr
        # data points
        self.full_data = []
        # data labels
        self.full_labels = []
        # transition matrix
        self.t = []
        self.class_data = []
        prep_data(self)
        self.build_class()


if __name__ == "__main__":
    rospy.init_node('single_classifier')
    rospack = rospkg.RosPack()
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

    fpath = rospack.get_path('gait_hmm_ros') + '/scripts/new_bags/datasets/' + prefix + '_'
    datafile = fpath + datafile

    if datafile == "":
        rospy.warn("No input file given, exiting")
        exit()

    if "bte" in datafile:
        batch_test = 1
    else:
        batch_test = 0

    if "btr" in datafile:
        batch_train = 1
    else:
        batch_train = 0

    x = SingleClassifier(normalized, folds, datafile, prefix, batch_test, batch_train)
