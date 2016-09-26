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
from gait_hmm_ros.msg import imu_vector

first = False
idx = 0
classifier_input = []
window = 10


def callback_data(msg):
    global first, idx, classifier_input
    if not first:
        first = True
        idx %= 16
        classifier_input[idx] = msg.data
    else:
        idx %= 16
        classifier_input[idx] = msg.data
    idx += 1

rospy.init_node('online_node')
rospack = rospkg.RosPack()
pref = rospy.get_param('~classifier', "quat_bte_rf_rll_rul_m_")
window = rospy.get_param('~window', 16)
fpath = rospack.get_path('gait_hmm_ros')+'/scripts/trained_classifiers/'+pref+'classifier.p'
classifier_input = [[]]*window
sub = rospy.Subscriber('data_vector', imu_vector, callback=callback_data)
pub = rospy.Publisher('matlab_msg', imu_vector, queue_size=10)
classifier = pickle.load(open(fpath, 'rb'))
matlab_vec = imu_vector()

while not rospy.is_shutdown():
    rospy.Rate(10).sleep()
    # print classifier_input
    logp, path = classifier.viterbi(list(classifier_input))
    if ("".join(state.name for i, state in classifier.viterbi(classifier_input)[1]).count('swing'))>10:
        rospy.logwarn("Swing")
    else:
        rospy.logwarn("Stance")






