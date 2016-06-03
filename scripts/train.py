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
import entry_data as ed
from sklearn.mixture import GMM
from collections import namedtuple
from threespace_ros.msg import dataVec
from matplotlib import pyplot as plt
from entry_data import DataEntry


rospy.init_node('hmm_trainer')
alphabet = ['HO','FF','HS','SW']

data = []
if(len(sys.argv)<2):
    exit()
else:
    prefix=sys.argv[1]
#print prefix+"_foot.p"
data = pickle.load(open(prefix+"_foot.p","rb"))
#print data
ho_data = ed.classData(label = 0)
ff_data = ed.classData(label = 1)
hs_data = ed.classData(label = 2)
sw_data = ed.classData(label = 3)
invalid_data = ed.classData(label = -1)
for entry in data:
    #rospy.logwarn("%f %f %f %d %d",entry.gyrox, entry.gyroy, entry.gyroz, entry.label, entry.sequence)
    if entry.label == 0:
        ho_data.add(entry)
    elif entry.label == 1:
        ff_data.add(entry)
    elif entry.label == 2:
        hs_data.add(entry)
    elif entry.label == 3 :
        sw_data.add(entry)
    else:
        invalid_data.add(entry)
#ho_data.calcParams()
#ff_data.calcParams()
#hs_data.calcParams()
#sw_data.calcOarams()
#print invalid_data.gyrox.data
invalid_data.calcParams()
print invalid_data.quatx.max
print invalid_data.quatx.min
print invalid_data.quatx.mean
print invalid_data.quatx.stdev
print invalid_data.quatx.variance
#print invalid_data.quatx.data

