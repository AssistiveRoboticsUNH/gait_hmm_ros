#!/usr/bin/env python
import roslib
import rospy
import pickle
import time
import math
import string
import sys
import cv2
import geometry_msgs.msg
import std_msgs.msg
import sensor_msgs.msg
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from sensor_msgs.msg import Image
from entry_data import DataEntry, fullEntry

rospy.init_node('visualise')
pref = sys.argv[1]
plt_lower_leg = pickle.load(open(pref+"_lower_leg_annotated.p", "rb"))
plt_upper_leg = pickle.load(open(pref+"_upper_leg_annotated.p", "rb"))
plt_foot = pickle.load(open(pref+"_foot_annotated.p", "rb"))
ano = cv2.imread("ano.png")
ano = cv2.resize(ano, (640, 480))

ff_ = [[] for i in range(7*3)]
ho_ = [[] for i in range(7*3)]
sw_ = [[] for i in range(7*3)]
hs_ = [[] for i in range(7*3)]
lists = [ff_, ho_, sw_, hs_]
i = 0
if(len(sys.argv)==3):
    if(sys.argv[2]=='c'):
        rospy.logwarn("Loading Annotations")
        while foot[i].label!=-1:
            i += 1
    elif(sys.argv[2]=='d'):
        rospy.logerr("Clearing Annotations")
        for i in range(0, len(foot)):
            foot[i] = foot[i]._replace(label = -1)
            lower_leg[i] = lower_leg[i]._replace(label=-1)
            upper_leg[i] = upper_leg[i]._replace(label=-1)
        i = 0
#cv.NamedWindow("Annotation Window", 1)
keys =[27, 81, 82, 83, 84, 114, 115, 99]
labels = ["FF", "HO", "SW", "HS"]
total_entries = len(plt_foot)
#plt_foot = pickle.load(open(pref+"_foot_annotated.p","rb"))

for i in range(0, len(plt_foot)):
    lists[plt_foot[i].label][0].append(plt_foot[i].quatx)
    lists[plt_foot[i].label][1].append(plt_foot[i].quaty)
    lists[plt_foot[i].label][2].append(plt_foot[i].quatz)
    lists[plt_foot[i].label][3].append(plt_foot[i].quatw)
    lists[plt_foot[i].label][4].append(plt_foot[i].gyrox)
    lists[plt_foot[i].label][5].append(plt_foot[i].gyroy)
    lists[plt_foot[i].label][6].append(plt_foot[i].gyroz)

    lists[plt_lower_leg[i].label][7].append(plt_lower_leg[i].quatx)
    lists[plt_lower_leg[i].label][8].append(plt_lower_leg[i].quaty)
    lists[plt_lower_leg[i].label][9].append(plt_lower_leg[i].quatz)
    lists[plt_lower_leg[i].label][10].append(plt_lower_leg[i].quatw)
    lists[plt_lower_leg[i].label][11].append(plt_lower_leg[i].gyrox)
    lists[plt_lower_leg[i].label][12].append(plt_lower_leg[i].gyroy)
    lists[plt_lower_leg[i].label][13].append(plt_lower_leg[i].gyroz)

    lists[plt_upper_leg[i].label][14].append(plt_upper_leg[i].quatx)
    lists[plt_upper_leg[i].label][15].append(plt_upper_leg[i].quaty)
    lists[plt_upper_leg[i].label][16].append(plt_upper_leg[i].quatz)
    lists[plt_upper_leg[i].label][17].append(plt_upper_leg[i].quatw)
    lists[plt_upper_leg[i].label][18].append(plt_upper_leg[i].gyrox)
    lists[plt_upper_leg[i].label][19].append(plt_upper_leg[i].gyroy)
    lists[plt_upper_leg[i].label][20].append(plt_upper_leg[i].gyroz)


f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
ax1.boxplot(lists[0][:])
ax1.set_title('Flat Foot')
ax2.set_title('Heel Off')
ax3.set_title('Swing')
ax4.set_title('Heel Strike')
ax2.boxplot(lists[1][:])
ax3.boxplot(lists[2][:])
ax4.boxplot(lists[3][:])

plt.show()
#print ff_[0]
exit()