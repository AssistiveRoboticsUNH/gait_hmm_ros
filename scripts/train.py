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
from collections import namedtuple
from threespace_ros.msg import dataVec

rospy.init_node('hmm_trainer')
alphabet = ['ff','ho','sw','hs']
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
print prefix+"_foot.p"
data = pickle.load(open(prefix+"_foot.p","rb"))
print data
for entry in data:
    rospy.logwarn("%f %f %f %d %d",entry.gyrox, entry.gyroy, entry.gyroz, entry.label, entry.sequence)
