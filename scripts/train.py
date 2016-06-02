#!/usr/bin/env python
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import time
import math
import UnfairCasino
import pickle
import sys
import operator
import numpy as np
from sklearn.mixture import GMM
from collections import namedtuple
from threespace_ros.msg import dataVec
from matplotlib import pyplot as plt


rospy.init_node('hmm_trainer')
alphabet = ['HO','FF','HS','SW']
DataEntry = namedtuple('DataEntry','\
        quatx quaty quatz quatw \
        gyrox gyroy gyroz \
        accelx accely accelz \
        compx compy compz \
        label \
        sequence')
data = []
if(len(sys.argv)<2):
    exit()
else:
    prefix=sys.argv[1]
#print prefix+"_foot.p"
data = pickle.load(open(prefix+"_foot.p","rb"))
#print data
ff_data = []
ff_parms = []
ho_data = []
ho_params = []
sw_data = []
sw_params = []
hs_data = []
hs_params = []
print max(data, key=operator.attrgetter('gyrox')).gyrox
for entry in data:
    #rospy.logwarn("%f %f %f %d %d",entry.gyrox, entry.gyroy, entry.gyroz, entry.label, entry.sequence)
    if entry.label == 0:
        ho_data.append(entry)
    elif entry.label == 1:
        ff_data.append(entry)
    elif entry.label == 2:
        hs_data.append(entry)
    elif entry.label == 3 :
        sw_data.append(entry)
ff_params.append(max(ff_data, key = operator.attrgetter('gyrox')).gyrox)
ff_params.append(min(ff_data, key = operator.attrgetter('gyrox')).gyrox)
ff_params.append(max(ff_data, key = operator.attrgetter('gyroy')).gyroy)
ff_params.append(max(ff_data, key = operator.attrgetter('gyroy')).gyroy)
ff_params.append(min(ff_data, key = operator.attrgetter('gyroz')).gyroz)
ff_params.append(min(ff_data, key = operator.attrgetter('gyroz')).gyroz)
ho_params.append(max(ho_data, key = operator.attrgetter('gyrox')).gyrox)
ho_params.append(max(ho_data, key = operator.attrgetter('gyrox')).gyrox)
ho_params.append(max(ho_data, key = operator.attrgetter('gyrox')).gyroy)
ho_params.append(min(ho_data, key = operator.attrgetter('gyrox')).gyroy)
ho_params.append(min(ho_data, key = operator.attrgetter('gyrox')).gyroz)
ho_params.append(min(h_data, key = operator.attrgetter('gyrox')).gyroz)
hs_params.append(max(hs_data, key = operator.attrgetter('gyrox')).gyrox)
hs_params.append(max(hs_data, key = operator.attrgetter('gyrox')).gyrox)
hs_params.append(max(hs_data, key = operator.attrgetter('gyrox')).gyroy)
hs_params.append(min(hs_data, key = operator.attrgetter('gyrox')).gyroy)
hs_params.append(min(hs_data, key = operator.attrgetter('gyrox')).gyroz)
hs_params.append(min(hs_data, key = operator.attrgetter('gyrox')).gyroz)
sw_params.append(max(sw_data, key = operator.attrgetter('gyrox')).gyrox)
sw_params.append(max(sw_data, key = operator.attrgetter('gyrox')).gyrox)
sw_params.append(max(sw_data, key = operator.attrgetter('gyrox')).gyroy)
sw_params.append(min(sw_data, key = operator.attrgetter('gyrox')).gyroy)
sw_params.append(min(sw_data, key = operator.attrgetter('gyrox')).gyroz)
sw_params.append(min(sw_data, key = operator.attrgetter('gyrox')).gyroz)
