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

DataEntry = namedtuple('DataEntry',\
        'quatx quaty quatz quatw \
        gyrox gyroy gyroz \
        accelx accely accelz \
        compx compy compz \
        label \
        sequence')

rospy.init_node('auto_annotate')
pref = rospy.get_param('~prefix', "none")
auto = rospy.get_param('~auto', "False")
rospack = rospkg.RosPack()
path = rospack.get_path('gait_hmm_ros')+'/scripts/'
pref = path + pref

matfile = rospy.get_param('~matfile', "none")
if matfile != "none":
    matfile_data = sio.loadmat(path+matfile)

joint_names = ['rf', 'rll', 'rul', 'lf', 'lll', 'lua', 'lul', 'm', 'ch', 'rs', 'rua', 'rla',\
             'rw', 'ls', 'lua', 'lla', 'lw']

imu_names = ['~rf', '~rll', '~rul', '~lf', '~lll', '~lua', '~lul', '~m', '~ch', '~rs', '~rua', '~rla',\
             '~rw', '~ls', '~lua', '~lla', '~lw']

joint_names_full = ['Right Foot', 'Right Lower Leg', 'Right Upper Leg',\
                    'Left Foot', 'Left Lower Leg', 'Left Upper Leg',\
                    'Mid', 'Chest', \
                    'Right Shoulder', 'Right Upper Arm', 'Right Lower Arm', 'Right Wrist',\
                    'Left Shoulder', 'Left Upper Arm', 'Left Lower Arm', 'Left Wrist']

imu_pickled_data = [[] for i in range(0, len(imu_names))]
imu_enable = [0 for i in range(0, len(imu_names))]
bridge = CvBridge()

ano = cv2.imread(path+"ano.png")
ano = cv2.resize(ano, (640, 480))

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
    # rl_timestamps.append(abs(i - imu_timestamps[total_entries-1])/1000000000)
    rl_timestamps.append(abs(i - imu_timestamps[0])/1000000000)
    # print abs(i - imu_timestamps[total_entries-1])/1000000000

keys = [27, 81, 82, 83, 84, 114, 115, 99]
labels = ["FF", "HO", "SW", "HS"]

k = 7
lhs = matfile_data['LHS'][0][0]
lto = matfile_data['LTO'][0][0]
rhs = matfile_data['RHS'][0][0]
rto = matfile_data['RTO'][0][0]

mocap_data = []

# mocap_size = len(matfile_data['LHS'][0][0])+len(matfile_data['LTO'][0][0])+\
# len(matfile_data['RHS'][0][0])+len(matfile_data['RTO'][0][0])

mocap_size = len(lhs)+len(lto)+len(rhs)+len(rto)

# rospy.loginfo("Mocap Size : "+str(mocap_size))

mocap_labels = ['LHS', 'LTO', 'RHS', 'RTO']
mocap_indexes = [0, 0, 0, 0]
mocap_lists = [lhs, lto, rhs, rto]

# first_row = [matfile_data['LHS'][0][0][0], matfile_data['LTO'][0][0][0],\
# matfile_data['RHS'][0][0][0], matfile_data['RTO'][0][0][0]]

first_row = (lhs[0], lto[0], rhs[0], rto[0])
rospy.loginfo("First Row : " +str(first_row))
start_label = mocap_labels[first_row.index(min(first_row))]
rospy.loginfo("Start Label : "+start_label)
start_index = mocap_labels.index(start_label)
rospy.loginfo("Start Index : "+str(start_index))
# start_frame = min(matfile_data['LHS'][0], matfile_data['LHS'], matfile_data['LHS'], matfile_data['LHS'][0])
i = 0
if auto == "True":
    while i < mocap_size:
        current_index = start_index%4
        mocap_data.append((mocap_labels[current_index], mocap_lists[current_index][mocap_indexes[current_index]]))
        mocap_indexes[current_index] += 1
        start_index -= 1
        # rospy.loginfo(mocap_data[i])
        i += 1
    start_mocap = mocap_data[0][1]
    end_mocap = mocap_data[mocap_size-1][1]
# print mocap_data
i = 0
lower_index = 0
upper_index = 0
while i < total_entries:
    print rl_timestamps[i]
    if rl_timestamps[i] < mocap_data[0][1]:
        lower_bound = mocap_data[0][0]
        lower_index = 0
    else:
        while rl_timestamps[i] < mocap_data[lower_index][0] and lower_index < :
            lower_index += 1


exit()
while i < total_entries:
    # print("Frame #"+str(i)+"/"+str(total_entries))
    # print images[i].shape
    # vis = np.concatenate((images[i], ano), axis=1)
    # cv2.imshow("Annotation Window", images[i])
    # cv2.imshow("Annotation Window", vis)
    # k = cv2.waitKey(0)
    print k & 255
    while k & 255 not in keys:
        print("Waiting for correct key")
        k = cv2.waitKey(0)
        print k & 255
    print("Key : " + str(k & 255))
    # k = cv2.waitKey(0)
    k &= 255
    if k == 27:
        cv2.destroyAllWindows()
        exit()
    elif k == 81:
        # LEFT
        # print("FF")
        lower_leg[i] = lower_leg[i]._replace(label=0)
        upper_leg[i] = upper_leg[i]._replace(label=0)
        foot[i] = foot[i]._replace(label=0)
        rospy.logwarn("Label : %s", labels[foot[i].label])
        i += 1
    elif k == 82:
        # UP
        # print("HO")
        lower_leg[i] = lower_leg[i]._replace(label=1)
        upper_leg[i] = upper_leg[i]._replace(label=1)
        foot[i] = foot[i]._replace(label=1)
        rospy.logwarn("Label : %s", labels[foot[i].label])
        i += 1
    elif k == 83:
        # RIGHT
        # print("SW")
        lower_leg[i] = lower_leg[i]._replace(label=2)
        upper_leg[i] = upper_leg[i]._replace(label=2)
        foot[i] = foot[i]._replace(label=2)
        rospy.logwarn("Label : %s ", labels[foot[i].label])
        i += 1
    elif k == 84:
        # DOWN
        # print("HS")
        lower_leg[i] = lower_leg[i]._replace(label=3)
        upper_leg[i] = upper_leg[i]._replace(label=3)
        foot[i] = foot[i]._replace(label=3)
        rospy.logwarn("Label : %s ", labels[foot[i].label])
        i += 1
    elif k == 114:
        # R
        # GO BACK 10 FRAMES
        rospy.logerr("Rewind")
        i -= 10
        if i < 0:
            i = 0
    elif k == 99:
        # C
        # Skip Frame
        rospy.logwarn("Skipped Frame")
        i += 1
    elif k == 115:
        # S
        # SAVE
        # pickle.dump(lower_leg, open(pref+"_lower_leg_annotated.p","wb"))
        # pickle.dump(upper_leg, open(pref+"_upper_leg_annotated.p","wb"))
        # pickle.dump(foot, open(pref+"_foot_annotated.p","wb"))
        pickle.dump(lower_leg, open(pref+"_lower_leg.p", "wb"))
        pickle.dump(upper_leg, open(pref+"_upper_leg.p", "wb"))
        pickle.dump(foot, open(pref+"_foot.p", "wb"))
        rospy.logerr("Saved")
        # i = i-1
        if i < 0:
            i = 0
