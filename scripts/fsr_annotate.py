#!/usr/bin/env python
import roslib
import rospy
import rospkg
import pickle
import time
import math
import string
import sys
import cv2
import os.path
import imu_callbacks as iparam
import geometry_msgs.msg
import std_msgs.msg
import sensor_msgs.msg
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from collections import namedtuple
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime

DataEntry = namedtuple('DataEntry',
                       'quatx quaty quatz quatw \
                        gyrox gyroy gyroz \
                        accelx accely accelz \
                        compx compy compz \
                        label \
                        sequence')


def classify(arduino_reading):
    if (arduino_reading[4] == 1 and arduino_reading[5] == 1 and arduino_reading[6] == 1) or \
            (arduino_reading[4] == 1 and arduino_reading[5] == 0 and arduino_reading[6] == 1):
        print('stance')
        return 'stance'
    elif arduino_reading[4] == 0:
        print('swing')
        return 'swing'
    elif arduino_reading[4] == 1 and arduino_reading[5] == 0 and arduino_reading[6] == 0:
        print('stance')
        return 'stance'
    else:
        print('stance')
        return 'stance'

rospy.init_node('auto_annotate')
pref = rospy.get_param('~prefix', "none")
auto = rospy.get_param('~auto', "False")
rospack = rospkg.RosPack()
path = rospack.get_path('gait_hmm_ros') + '/scripts/'
pref = path + pref

matfile = rospy.get_param('~matfile', "none")
if matfile != "none":
    matfile_data = sio.loadmat(path + matfile)

leg = rospy.get_param("~leg", "left")

joint_names = iparam.imu_names


imu_names = iparam.imu_param_names


joint_names_full = iparam.imu_names_full


imu_pickled_data = []
arduino_pickled_data = []
gait_classification = []

total_entries = 0
total_sensors = len(imu_names)

#####################
# Load enabled IMUS #
#####################
for name in joint_names:
    fullname = pref + "_" + name + ".mat"
    if os.path.isfile(fullname):
        rospy.logwarn("Loading " + fullname)
        # x = pickle.load(open(fullname, "rb"))
        x = sio.loadmat(fullname)[name]
        # print x
        print (len(x))
        imu_pickled_data.append(x)
        total_entries = len(x)
    else:
        imu_pickled_data.append([])

rospy.logwarn("Loading timestamps from " + pref + "_timestamps.mat")
# imu_timestamps = pickle.load(open(pref + "_timestamps.mat", "rb"))
imu_timestamps = sio.loadmat(pref + "_timestamps.mat")['timestamps']
print (imu_timestamps)
rospy.logwarn("Loading arduino data from " + pref + "_arduino.mat")
arduino_pickled_data = sio.loadmat(pref + "_arduino.mat")['arduino']

rospy.logwarn("Loading arduino indices from " + pref + "_ar_index.mat")
arduino_indices = sio.loadmat(pref + "_ar_index.mat")['ar_ind']

rl_timestamps = []

#############################################
# Transform ROS timestamps to duration from #
# start of recording                        #
#############################################
for i in imu_timestamps:
    rl_timestamps.append(abs(i - imu_timestamps[0]) / 1000000000)

mocap_data = []
class_pickle = []
mocap_labels = ['LHS', 'LTO', 'RHS', 'RTO']
mocap_indexes = [0, 0, 0, 0]
phase_labels_a = ['swing', 'stance']
phase_indices_a = [0, 1]
phase_labels_b = ['lswing', 'lstance', 'rswing', 'rstance']

for i in range(0, total_entries):
    g = classify(arduino_pickled_data[i])
    class_pickle.append(phase_labels_a.index(g))

rospy.logwarn(str(len(class_pickle)) + " entries annotated")
rospy.logwarn("Dumping labels to " + pref + "_labels_annotated.mat")
sio.savemat(pref + "_labels_annotated.mat", mdict={'labels': class_pickle})
