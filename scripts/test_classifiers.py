#!/usr/bin/env python
import rospy
import rospkg
import pickle
import numpy as np
import entry_data as ed
import imu_callbacks as iparam
import matlab.engine
from threespace_ros.msg import dataVec
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import normalize
from entry_data import DataEntry, fullEntry
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from scipy import io as scio

rospy.init_node('classifier_test')
input_names = []
device_names = []
imus_used = ""
pref = rospy.get_param('~classifier', "none")
if pref == "none":
    rospy.logerr('No classifier given, exiting ...')
    exit()

classifier = pickle.load(pref + "classifier.p");
full_data = pickle.load(pref + "full_data.p");
full_labels = pickle.load(pref + "full_labels.p");