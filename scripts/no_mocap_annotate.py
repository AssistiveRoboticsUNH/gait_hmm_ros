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
import scipy.io as sio
from collections import namedtuple
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime

rospy.init_node('nomocap_annotate')
pref = rospy.get_param('~prefix', "none")
rospack = rospkg.RosPack()
path = rospack.get_path('gait_hmm_ros') + '/scripts/'
pref = path + pref

joint_names = iparam.imu_names
imu_names = iparam.imu_param_names
joint_names_full = iparam.imu_names_full
imu_pickled_data = []

rospy.logwarn("Loading timestamps from " + pref + "_timestamps.p")
imu_timestamps = pickle.load(open(pref + "_timestamps.p", "rb"))
rospy.logwarn("Loading images from " + pref + "_images.p")
images = pickle.load(open(pref + "_images.p", "rb"))
rospy.logwarn("Loading indices from " + pref + "_indices.p")
indices = pickle.load(open(pref + "_indices.p", "rb"))
rl_timestamps = []

while i < total_entries:
    fsr_bk =

