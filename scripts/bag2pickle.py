#!/usr/bin/env python
import roslib
import rospy
import tf
import tf2_ros
import rosbag
import rospkg
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
import scipy.io as sio
from threespace_ros.msg import dataVec
from collections import namedtuple
from cv_bridge import CvBridge, CvBridgeError

DataEntry = namedtuple('DataEntry', 'quatx quaty quatz quatw \
        gyrox gyroy gyroz \
        accelx accely accelz \
        compx compy compz \
        label \
        sequence')
rospy.init_node('bag2pickle')
pref = rospy.get_param('~prefix', "none")
if pref == "none":
    rospy.logerr("No input file given, exiting")
    exit()

rospack = rospkg.RosPack()
bag = rosbag.Bag(rospack.get_path('gait_hmm_ros')+'/scripts/'+pref+'.bag')

matfile = rospy.get_param('~matfile', "none")
if matfile != "none":
    matfile_data = sio.loadmat(matfile)

joint_names = ['rf', 'rll', 'rul', 'lf', 'lll', 'lua', 'lul', 'm', 'ch', 'rs', 'rua', 'rla',\
             'rw', 'ls', 'lua', 'lla', 'lw']

imu_names = ['~rf', '~rll', '~rul', '~lf', '~lll', '~lua', '~lul', '~m', '~ch', '~rs', '~rua', '~rla',\
             '~rw', '~ls', '~lua', '~lla', '~lw']

imu_vectors = [[] for i in range(0, len(imu_names))]
imu_pickle_data = [[] for i in range(0, len(imu_names))]
imu_timestamps = [[] for i in range(0, len(imu_names))]
imu_indices = [[] for i in range(0, len(imu_names))]
imu_enable = [0 for i in range(0, len(imu_names))]
imu_topics = ["" for i in range(0, len(imu_names))]
images = []
image_timestamps = []
image_indexes = []
timestamps = []
for i in range(0, len(imu_names)):
    imu_topics[i] = rospy.get_param(imu_names[i], imu_enable[i])

print imu_topics
for topic, msg, t in bag.read_messages():
    # rospy.logerr(t)
    print t.to_nsec()
    if topic == "/usb_cam/image_raw":
        # rospy.logerr(msg.header.stamp)
        # rospy.logerr("/usb_cam/image_raw")
        images.append(msg)
        image_timestamps.append(t.to_nsec())
    else:
        index = imu_topics.index(topic[1:])
        # rospy.logerr(topic+" --> "+imu_names[index])
        # rospy.logerr(msg.header.stamp)
        imu_vectors[index].append(msg)
        imu_timestamps[index].append(t.to_nsec())

min_ = sys.maxint
min_index = 0

for i in range(0, len(imu_vectors)):
    if len(imu_vectors[i]) != 0:
        if len(imu_vectors[i]) < min_:
            min_ = len(imu_vectors[i])
            min_index = i
# print min_
# print len(images)
# print len(imu_timestamps[3])


# print image_timestamps
# print imu_timestamps[3]

# for topic, msg, t in bag.read_messages():
for i in range(0, min_):
    ts = int(imu_timestamps[min_index][i])
    # print ts
    indexes = []
    for j in range(0, len(imu_vectors)):
        # t = imu_timestamps[j].index(min(imu_timestamps[j], key=lambda x: abs(x-ts)))
        if(len(imu_timestamps[j])) != 0:
            t = min(imu_timestamps[j], key=lambda x: abs(x-ts))
            # print t
            imu_indices[j].append(t)
        else:
            imu_indices[j].append(-1)
    # image_indexes.append(images.index(images[(min(image_timestamps, key=lambda x: abs(x-ts)))]))
    image_indexes.append(image_timestamps.index((min(image_timestamps, key=lambda x: abs(x-ts)))))
    rospy.logerr(str(i)+"/"+str(len(imu_vectors[min_index]))+":"+str(ts)+" --> "+str(t))
for j in range(0, len(imu_vectors)):
    print len(imu_indices[j])
print len(image_indexes)

# min_ = min(map(len, imu_vectors))
states = ['ff', 'hs', 'sw', 'ho']
bridge = CvBridge()

for i in range(0, min_):
    for j in range(0, len(imu_vectors)):
        imu_pickle_data[j].append(imu_vectors[j][i])
    # _ll = lhdv[i]
    # _ul = rhdv[i]
    # _ft = luadv[i]
    # index = int(ratio*i)
    # rospy.loginfo("%d/%d  %d/%d",i, total_entries,index, len(img))
    # im = img[int(index)]
    # cv_image = bridge.imgmsg_to_cv2(im, desired_encoding="passthrough")
    # ul = DataEntry(_ul.quat.quaternion.x, _ul.quat.quaternion.y,\
        # _ul.quat.quaternion.z, _ul.quat.quaternion.w, \
        # _ul.gyroX, _ul.gyroY, _ul.gyroZ,\
        # _ul.accX, _ul.accY, _ul.accZ,\
        # _ul.comX, _ul.comY, _ul.comZ,\
        # -1,
        # i)
    # upper_leg.append(ul)
    # ll = DataEntry(_ll.quat.quaternion.x, _ll.quat.quaternion.y, \
        # _ll.quat.quaternion.z, _ll.quat.quaternion.w, \
        # _ll.gyroX, _ll.gyroY, _ll.gyroZ, \
        # _ll.accX, _ll.accY, _ll.accZ,\
        # _ll.comX, _ll.comY, _ll.comZ,\
        # -1,
        # i)
    # lower_leg.append(ll)
    #ft = DataEntry(_ft.quat.quaternion.x, _ft.quat.quaternion.y, \
        # _ft.quat.quaternion.z, _ft.quat.quaternion.w, \
        # _ft.gyroX, _ft.gyroY, _ft.gyroZ, \
        # _ft.accX, _ft.accY, _ft.accZ,\
        # _ft.comX, _ft.comY, _ft.comZ,\
        # -1,\
        # i)
    # print ft.label
    # foot.append(ft)
    # try:
    #    cvim = bridge.imgmsg_to_cv2(im, "bgr8")
    #    recim.append(cvim)
    # except CvBridgeError as e:
    #    print(e)

print len(imu_pickle_data[3])
print len(foot)
print len(lower_leg)
print len(upper_leg)
pickle.dump(foot, open(pref+"_foot.p", "wb"))
pickle.dump(lower_leg, open(pref+"_lower_leg.p", "wb"))
pickle.dump(upper_leg, open(pref+"_upper_leg.p", "wb"))
pickle.dump(recim, open(pref+"_images.p", "wb"))
