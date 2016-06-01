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
from collections import namedtuple
from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError

DataEntry = namedtuple('DataEntry','quatx quaty quatz quatw \
            gyrox gyroy gyroz\
            accelx accely accelz\
            compx compy compz\
            label,\
            sequence')

rospy.init_node('annotate')
pref = sys.argv[1]
images = []
bridge = CvBridge()
images = pickle.load(open(pref+"_images.p", "r"))
lower_leg = pickle.load(open(pref+"_lower_leg.p","rb"))
upper_leg = pickle.load(open(pref+"_upper_leg.p","rb"))
foot = pickle.load(open(pref+"_foot.p","rb"))
ano = cv2.imread("ano.png")
ano = cv2.resize(ano, (640, 480))
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
            lower_leg[i] = lower_leg[i]._replace(label = -1)
            upper_leg[i] = upper_leg[i]._replace(label = -1)
        i = 0
#cv.NamedWindow("Annotation Window", 1)
keys =[27,81,82,83,84,114,115]
labels = ['HO', "FF", "HS", "SW"]
while i < len(images):
    print("Frame #"+str(i))
    #print images[i].shape
    vis = np.concatenate((images[i], ano), axis=1)
    #cv2.imshow("Annotation Window", images[i])
    cv2.imshow("Annotation Window", vis)
    k = cv2.waitKey(0)
    while k&255 not in keys:
        print("Waiting for correct key")
        k = cv2.waitKey(0)
    print("Key : " + str(k&255))
    #k = cv2.waitKey(0)
    k = k&255
    if k == 27:
        cv2.destroyAllWindows()
        exit()
    elif k == 81:
        #LEFT
        #print("HO")
        lower_leg[i] = lower_leg[i]._replace(label = 0)
        upper_leg[i] = upper_leg[i]._replace(label = 0)
        foot[i] = foot[i]._replace(label = 0)
        print("Label : "+ labels[foot[i].label])
        i += 1
    elif k == 82:
        #UP
        #print("FF")
        lower_leg[i] = lower_leg[i]._replace(label = 1)
        upper_leg[i] = upper_leg[i]._replace(label = 1)
        foot[i] = foot[i]._replace(label = 1)
        print("Label : "+ labels[foot[i].label])
        i += 1
    elif k == 83:
        #RIGHT
        #print("HS")
        lower_leg[i] = lower_leg[i]._replace(label = 2)
        upper_leg[i] = upper_leg[i]._replace(label = 2)
        foot[i] = foot[i]._replace(label = 2)
        print("Label : "+ labels[foot[i].label])
        i += 1
    elif k == 84:
        #DOWN
        #print("SW")
        lower_leg[i] = lower_leg[i]._replace(label = 3)
        upper_leg[i] = upper_leg[i]._replace(label = 3)
        foot[i] = foot[i]._replace(label = 3)
        print("Label : "+ labels[foot[i].label])
        i += 1
    elif k == 114:
        #GO BACK 10 FRAMES
        print("Rewind")
        i = i-10
        if i < 0:
            i = 0
    elif k == 115:
        #SAVE
        print("Save")
        #pickle.dump(lower_leg, open(pref+"_lower_leg_annotated.p","wb"))
        #pickle.dump(upper_leg, open(pref+"_upper_leg_annotated.p","wb"))
        #pickle.dump(foot, open(pref+"_foot_annotated.p","wb"))
        pickle.dump(lower_leg, open(pref+"_lower_leg.p","wb"))
        pickle.dump(upper_leg, open(pref+"_upper_leg.p","wb"))
        pickle.dump(foot, open(pref+"_foot.p","wb"))
        #i = i-1
        if i < 0:
            i=0
    pickle.dump(lower_leg, open(pref+"_lower_leg_annotated.p","wb"))
    pickle.dump(upper_leg, open(pref+"_upper_leg_annotated.p","wb"))
    pickle.dump(foot, open(pref+"_foot_annotated.p","wb"))

