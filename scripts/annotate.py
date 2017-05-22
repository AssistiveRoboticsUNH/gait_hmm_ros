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

from cv_bridge import CvBridge, CvBridgeError


def addToChart(list, foot, lower, upper):
    data[0].append(foot.quat)
    return


DataEntry = namedtuple('DataEntry', \
                       'quatx quaty quatz quatw \
        gyrox gyroy gyroz \
        accelx accely accelz \
        compx compy compz \
        label \
        sequence')

rospy.init_node('annotate')
pref = sys.argv[1]
images = []
bridge = CvBridge()

images = pickle.load(open(pref + "_images.p", "r"))
lower_leg = pickle.load(open(pref + "_lower_leg.p", "rb"))
upper_leg = pickle.load(open(pref + "_upper_leg.p", "rb"))
foot = pickle.load(open(pref + "_foot.p", "rb"))
p_indices = pickle.load(open(pref + "_indices.p", "r"))

ano = cv2.imread("ano.png")
ano = cv2.resize(ano, (640, 480))
i = 0
ff_ = [[] for i in range(7 * 3)]
ho_ = [[] for i in range(7 * 3)]
sw_ = [[] for i in range(7 * 3)]
hs_ = [[] for i in range(7 * 3)]
if len(sys.argv) == 3:
    if sys.argv[2] == 'c':
        rospy.logwarn("Loading Annotations")
        while foot[i].label != -1:
            i += 1
    elif sys.argv[2] == 'd':
        rospy.logerr("Clearing Annotations")
        for i in range(0, len(foot)):
            foot[i] = foot[i]._replace(label=-1)
            lower_leg[i] = lower_leg[i]._replace(label=-1)
            upper_leg[i] = upper_leg[i]._replace(label=-1)
        i = 0

keys = [27, 81, 82, 83, 84, 114, 115, 99]
labels = ["FF", "HO", "SW", "HS"]
total_entries = len(images)

if sys.argv[2] == 'v':
    while (i < total_entries - 10) and (i >= 0):
        print("Frame #" + str(i) + "/" + str(total_entries))
        plt_data = []
        plt_data.append(foot[i].quatx)
        plt_data.append(foot[i].quaty)
        plt_data.append(foot[i].quatz)
        plt_data.append(foot[i].quatw)
        plt_data.append(foot[i].gyrox)
        plt_data.append(foot[i].gyroy)
        plt_data.append(foot[i].gyroz)

        plt_data.append(lower_leg[i].quatx)
        plt_data.append(lower_leg[i].quaty)
        plt_data.append(lower_leg[i].quatz)
        plt_data.append(lower_leg[i].quatw)
        plt_data.append(lower_leg[i].gyrox)
        plt_data.append(lower_leg[i].gyroy)
        plt_data.append(lower_leg[i].gyroz)

        plt_data.append(upper_leg[i].quatx)
        plt_data.append(upper_leg[i].quaty)
        plt_data.append(upper_leg[i].quatz)
        plt_data.append(upper_leg[i].quatw)
        plt_data.append(upper_leg[i].gyrox)
        plt_data.append(upper_leg[i].gyroy)
        plt_data.append(upper_leg[i].gyroz)

        k = cv2.waitKey(0)
        k &= 255

        plt.figure()
        plt.ylim(ymax=7, ymin=-7)
        plt.title(labels[foot[i].label])
        plt.bar(np.arange(len(plt_data)), plt_data)
        # plt.show(block=False)
        plt.savefig('foo.png')
        foo = cv2.imread("foo.png")
        foo = cv2.resize(foo, (640, 480))
        vis = np.concatenate((images[p_indices[i]], foo), axis=1)

        cv2.imshow("Annotation Window", vis)
        k = cv2.waitKey(0)
        k &= 255

        if k == 83:
            # RIGHT
            i += 1
        elif k == 81:
            # left
            i -= 1
        elif k == 27:
            cv2.destroyAllWindows()
            exit()

    exit()
while i < total_entries:
    print("Frame #" + str(i) + "/" + str(total_entries))
    # print images[i].shape
    # vis = np.concatenate((images[i], ano), axis=1)
    vis = np.concatenate((images[p_indices[i]], ano), axis=1)

    # cv2.imshow("Annotation Window", images[i])
    cv2.imshow("Annotation Window", vis)
    k = cv2.waitKey(0)
    print (k & 255)
    while k & 255 not in keys:
        print("Waiting for correct key")
        k = cv2.waitKey(0)
        print (k & 255)
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
        # pickle.dump(foot, open(pref+"_foot_annotated.p","wb"))
        pickle.dump(lower_leg, open(pref + "_lower_leg.p", "wb"))
        pickle.dump(upper_leg, open(pref + "_upper_leg.p", "wb"))
        pickle.dump(foot, open(pref + "_foot.p", "wb"))
        rospy.logerr("Saved")
        # i = i-1
        if i < 0:
            i = 0
    pickle.dump(lower_leg, open(pref + "_lower_leg_annotated.p", "wb"))
    pickle.dump(upper_leg, open(pref + "_upper_leg_annotated.p", "wb"))
    pickle.dump(foot, open(pref + "_foot_annotated.p", "wb"))
