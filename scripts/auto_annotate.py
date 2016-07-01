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


def assign_label_a(lower, upper):
    if lower == 'LTO':
        if upper == 'LTO' or upper == 'LHS':
            return 'swing'
        else:
            return 'stance'
    if lower == 'LHS':
        if upper == 'LHS' or upper == 'RTO' or upper == 'RHS':
            return 'stance'
        else:
            return 'swing'
    if lower == 'RTO':
        if upper == 'RTO' or upper == 'RTS' or upper == 'LTO':
            return 'swing'
        else:
            return 'stance'
    if lower == 'RHS':
        if upper == 'RHS' or upper == 'LTO':
            return 'stance'
        else:
            return 'swing'


# NOT SURE IF IT MAKES SENSE to have different phase for left and right
# aren't they always mirrored ?

# def assign_label_b(lower, upper):
#     if lower == 'LTO':
#         if upper == 'LTO':
#             return ['lswing', 'rstance']
#         elif upper == 'LHS':
#             return ['lswing', 'rstance']
#         elif upper == 'RTO':
#             return ['lswing', 'rstance']
#         elif upper == 'RHS':
#             return ['lswing', 'rstance']
#     if lower == 'LHS':
#         if upper == 'LHS':
#         elif upper == 'RTO':
#         elif upper == 'RHS':
#         elif upper == 'LTO':
#     if lower == 'RTO':
#         if upper == 'RTO':
#         elif upper == 'RHS':
#         elif upper == 'LTO':
#         elif upper == 'LHS':
#     if lower == 'RHS':
#         if upper == 'RHS':
#         elif upper == 'LTO':
#         elif upper == 'LHS':
#         elif upper == 'RTO':
#     return -1

rospy.init_node('auto_annotate')
pref = rospy.get_param('~prefix', "none")
auto = rospy.get_param('~auto', "False")
rospack = rospkg.RosPack()
path = rospack.get_path('gait_hmm_ros')+'/scripts/'
pref = path + pref

matfile = rospy.get_param('~matfile', "none")
if matfile != "none":
    matfile_data = sio.loadmat(path+matfile)

joint_names = ['rf', 'rll', 'rul', 'lf', 'lll', 'lua', 'lul', 'm', 'ch', 'rs', 'rua', 'rla',
               'rw', 'ls', 'lua', 'lla', 'lw']

imu_names = ['~rf', '~rll', '~rul', '~lf', '~lll', '~lua', '~lul', '~m', '~ch', '~rs', '~rua', '~rla',
             '~rw', '~ls', '~lua', '~lla', '~lw']

joint_names_full = ['Right Foot', 'Right Lower Leg', 'Right Upper Leg',
                    'Left Foot', 'Left Lower Leg', 'Left Upper Leg',
                    'Mid', 'Chest',
                    'Right Shoulder', 'Right Upper Arm', 'Right Lower Arm', 'Right Wrist',
                    'Left Shoulder', 'Left Upper Arm', 'Left Lower Arm', 'Left Wrist']

imu_pickled_data = []

bridge = CvBridge()

ano = cv2.imread(path+"ano.png")
ano = cv2.resize(ano, (640, 480))
total_entries = 0
total_sensors = len(imu_names)

for name in joint_names:
    fullname = pref+"_"+name+".p"
    if os.path.isfile(fullname):
        rospy.logwarn("Loading "+fullname)
        x = pickle.load(open(fullname, "rb"))
        print len(x)
        imu_pickled_data.append(x)
        total_entries = len(x)
    else:
        imu_pickled_data.append([])

imu_timestamps = pickle.load(open(pref+"_timestamps.p", "rb"))
rl_timestamps = []
for i in imu_timestamps:
    rl_timestamps.append(abs(i - imu_timestamps[0])/1000000000)

lhs = matfile_data['LHS'][0][0]
lto = matfile_data['LTO'][0][0]
rhs = matfile_data['RHS'][0][0]
rto = matfile_data['RTO'][0][0]

mocap_labels = ['LHS', 'LTO', 'RHS', 'RTO']
mocap_indexes = [0, 0, 0, 0]
mocap_lists = [lhs, lto, rhs, rto]
phase_labels_a = ['swing', 'stance']
phase_indices_a = [0, 1]
phase_labels_b = ['lswing', 'lstance', 'rswing', 'rstance']
mocap_data = []

mocap_size = len(lhs)+len(lto)+len(rhs)+len(rto)

first_row = (lhs[0], lto[0], rhs[0], rto[0])
rospy.loginfo("First Row : " + str(first_row))
start_label = mocap_labels[first_row.index(min(first_row))]
rospy.loginfo("Start Label : " + start_label)
start_index = mocap_labels.index(start_label)
rospy.loginfo("Start Index : " + str(start_index))
# start_frame = min(matfile_data['LHS'][0], matfile_data['LHS'], matfile_data['LHS'], matfile_data['LHS'][0])
i = 0
if auto == "True":
    while i < mocap_size:
        current_index = start_index % 4
        mocap_data.append((mocap_labels[current_index], mocap_lists[current_index][mocap_indexes[current_index]]))
        mocap_indexes[current_index] += 1
        start_index -= 1
        # rospy.loginfo(mocap_data[i])
        i += 1
    start_mocap = mocap_data[0][1]
    end_mocap = mocap_data[mocap_size-1][1]

i = 0
lower_index = 0
upper_index = 0
while i < total_entries:
    # rospy.loginfo("#"+str(i)+": Lower Index :"+str(lower_index)+", Upper Index :"+str(upper_index))
    if rl_timestamps[i] < mocap_data[0][1]:
        lower_bound = mocap_data[0][0]
        rospy.logwarn(str(rl_timestamps[i])+" is smaller than " +
                      str(mocap_data[0][0]) +
                      str(mocap_data[0][1])[0:10] + "]")
    elif rl_timestamps[i] > mocap_data[len(mocap_data)-1][1]:
        rospy.logwarn(str(rl_timestamps[i])+" is greater than " +
                      str(mocap_data[len(mocap_data)-1][0]) +
                      str(mocap_data[len(mocap_data)-1][1])[0:10] + "]")
    else:
        while rl_timestamps[i] > mocap_data[lower_index][1] and lower_index < len(mocap_data)-1:
            lower_index += 1
        lower_index -= 1
        upper_index = lower_index+1
        while rl_timestamps[i] > mocap_data[upper_index][1] and upper_index < len(mocap_data)-1:
            upper_index += 1
        rospy.logwarn(str(rl_timestamps[i])+" is between " + str(lower_index)+" : " +
                      str(mocap_data[lower_index][0]) +
                      str(mocap_data[lower_index][1])[0:10] + "] and " +
                      str(upper_index)+" : " +
                      str(mocap_data[upper_index][0]) +
                      str(mocap_data[upper_index][1])[0:10] + "]")

    for j in range(0, total_sensors):
            if len(imu_pickled_data[j]) != 0:
                imu_pickled_data[j][i] = imu_pickled_data[j][i]._replace(label=phase_labels_a.index(
                    assign_label_a(str(mocap_data[lower_index][0]), str(mocap_data[upper_index][0]))))
    i += 1
# for i in range(0, len(mocap_data)):
#        rospy.loginfo(str(mocap_data[i][0])+":"+str(mocap_data[i][1]))
# for i in range(0, total_entries):
#     for j in range(0, total_sensors):
#         if len(imu_pickled_data[j]) != 0:
#             rospy.logwarn(str(imu_pickled_data[j][i].label))

for i in range(0, total_sensors):
    if len(imu_pickled_data[i]) != 0:
        rospy.logwarn("Dumping "+joint_names[i]+" to " + pref+"_"+joint_names[i] + "_annotated.p")
        pickle.dump(imu_pickled_data[i], open(pref+"_"+joint_names[i] + "_annotated.p", "wb"))
