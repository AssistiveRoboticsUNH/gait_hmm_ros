#!/usr/bin/env python
import roslib
import rospy
import tf
import tf2_ros
import rosbag
import pickle
import geometry_msgs.msg
import sensor_msgs.msg
import std_msgs.msg
import time
import math
import string
import pickle
import sys
import cv2
from threespace_ros.msg import dataVec
from collections import namedtuple
from cv_bridge import CvBridge, CvBridgeError

DataEntry = namedtuple('DataEntry','quatx quaty quatz quatw \
        gyrox gyroy gyroz\
        accelx accely accelz\
        compx compy compz\
        label,\
        sequence')
rospy.init_node('bag2pickle')
pref = sys.argv[1]
bag = rosbag.Bag(pref+'.bag')
rh = []
rhdv = []
lh = []
lhdv = []
lua = []
luadv = []
img = []

for topic, msg, t in bag.read_messages():
    #print topic
    #if topic == "/r_hand":
    #    rospy.logwarn("#r_hand")
    #    rh.append(msg)
    if topic == "/r_hand_data_vec":
        rospy.logwarn("#r_hand_data_vec")
        rhdv.append(msg)
   # elif topic == "/l_hand":
   #     rospy.logwarn("#l_hand")
   #     lh.append(msg)
    elif topic == "/l_hand_data_vec":
        rospy.logwarn("#l_hand_data_vec")
        lhdv.append(msg)
    #elif topic == "/l_upper_arm":
    #    rospy.logwarn("#l_upper_arm")
    #    lua.append(msg)
    elif topic == "/l_upper_arm_data_vec":
        rospy.logwarn("#l_upper_arm_data_vec")
        luadv.append(msg)
    elif topic == "/usb_cam/image_raw":
        rospy.logwarn("#usb_cam_image_raw")
        img.append(msg)
    #else:
    #    rospy.logwarn("random message")
sizes = []
#print len(rh)
#sizes.append(len(rh))
#print len(rhdv)
sizes.append(len(rhdv))
#print len(lh)
#sizes.append(len(lh))
#print len(lhdv)
#print len(lua)
#print len(luadv)
sizes.append(len(luadv))
print len(img)
print min(sizes)
total_entries = min(sizes)
messages = []
states = ['ff','hs','sw','ho']
#ratio = float(total_entries)/float(len(img)-1)
ratio = float(len(img))/float(total_entries)
upper_leg = []
lower_leg = []
foot = []
recim = []
bridge = CvBridge()
for i in range(0, total_entries):
    _ll = lhdv[i]
    _ul = rhdv[i]
    _ft = luadv[i]
    index = int(ratio*i)
    #rospy.loginfo("%d/%d  %d/%d",i, total_entries,index, len(img))
    im = img[int(index)]
    #cv_image = bridge.imgmsg_to_cv2(im, desired_encoding="passthrough")
    ul = DataEntry(_ul.quat.quaternion.x, _ul.quat.quaternion.y,\
        _ul.quat.quaternion.z, _ul.quat.quaternion.w, \
        _ul.gyroX, _ul.gyroY, _ul.gyroZ,\
        _ul.accX, _ul.accY, _ul.accZ,\
        _ul.comX, _ul.comY, _ul.comZ,\
        -1,
        i)
    upper_leg.append(ul)
    ll = DataEntry(_ll.quat.quaternion.x, _ll.quat.quaternion.y, \
        _ll.quat.quaternion.z, _ll.quat.quaternion.w, \
        _ll.gyroX, _ll.gyroY, _ll.gyroZ, \
        _ll.accX, _ll.accY, _ll.accZ,\
        _ll.comX, _ll.comY, _ll.comZ,\
        -1,
        i)
    lower_leg.append(ll)
    ft = DataEntry(_ft.quat.quaternion.x, _ft.quat.quaternion.y, \
        _ft.quat.quaternion.z, _ft.quat.quaternion.w, \
        _ft.gyroX, _ft.gyroY, _ft.gyroZ, \
        _ft.accX, _ft.accY, _ft.accZ,\
        _ft.comX, _ft.comY, _ft.comZ,\
        -1,\
        i)
    foot.append(ft)
    try:
        cvim = bridge.imgmsg_to_cv2(im,"bgr8")
        recim.append(cvim)
    except CvBridgeError as e:
        print(e)
    
print len(foot)
print len(lower_leg)
print len(upper_leg)
pickle.dump(foot, open(pref+"_foot.p","wb"))
pickle.dump(lower_leg, open(pref+"_lower_leg.p","wb"))
pickle.dump(upper_leg, open(pref+"_upper_leg.p","wb"))
pickle.dump(recim, open(pref+"_images.p","wb"))
