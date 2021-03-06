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

pref = rospack.get_path('gait_hmm_ros')+'/scripts/'+pref

bag = rosbag.Bag(pref+'.bag')
bridge = CvBridge()

matfile = rospy.get_param('~matfile', "none")
if matfile != "none":
    matfile_data = sio.loadmat(matfile)

joint_names = ['rf', 'rll', 'rul',
               'lf', 'lll', 'lul',
               'm', 'ch', 'h',
               'rs', 'rua', 'rla', 'rh',
               'ls', 'lua', 'lla', 'lh']

joint_names_full = ['Right Foot', 'Right Lower Leg', 'Right Upper Leg',
                    'Left Foot', 'Left Lower Leg', 'Left Upper Leg',
                    'Mid', 'Chest', 'Head',
                    'Right Shoulder', 'Right Upper Arm', 'Right Lower Arm', 'Right Hand',
                    'Left Shoulder', 'Left Upper Arm', 'Left Lower Arm', 'Left Hand']

imu_names = ['~rf', '~rll', '~rul',
             '~lf', '~lll', '~lul',
             '~m', '~ch', '~h',
             '~rs', '~rua', '~rla', '~rh',
             '~ls', '~lua', '~lla', '~lh']

imu_vectors = [[] for i in range(0, len(imu_names))]
imu_pickle_data = [[] for i in range(0, len(imu_names))]
imu_timestamps = [[] for i in range(0, len(imu_names))]
imu_indices = [[] for i in range(0, len(imu_names))]
imu_enable = [0 for i in range(0, len(imu_names))]
imu_topics = ["" for i in range(0, len(imu_names))]

images = []
image_timestamps = []
image_indices = []
images_pickle_data = []
timestamps = []
pickle_timestamps = []
arduino_messages = []
arduino_timestamps = []
arduino_indices = []
arduino_pickle_data = []


for i in range(0, len(imu_names)):
    imu_topics[i] = rospy.get_param(imu_names[i], imu_enable[i])
    rospy.logwarn(joint_names_full[i]+" topic : "+imu_topics[i])

for topic, msg, t in bag.read_messages():
    rospy.logerr(topic)
    if topic == "/usb_cam/image_raw":
        images.append(msg)
        image_timestamps.append(t.to_nsec())
    elif topic == "/arduino":
        arduino_messages.append(msg)
        arduino_timestamps.append(t.to_nsec())
    else:
        index = imu_topics.index(topic[1:])
        imu_vectors[index].append(msg)
        imu_timestamps[index].append(t.to_nsec())

min_ = sys.maxint
min_index = 0

for i in range(0, len(imu_vectors)):
    rospy.logwarn(str(len(imu_vectors[i]))+" Frames in "+imu_names[i])
    if len(imu_vectors[i]) != 0:
        if len(imu_vectors[i]) < min_:
            min_ = len(imu_vectors[i])
            min_index = i
# for topic, msg, t in bag.read_messages():
for i in range(0, min_):
    ts = int(imu_timestamps[min_index][i])
    # print ts
    indexes = []
    time = 0.0
    n = 0.0
    for j in range(0, len(imu_vectors)):
        # t = imu_timestamps[j].index(min(imu_timestamps[j], key=lambda x: abs(x-ts)))
        if(len(imu_vectors[j])) != 0:
            t = imu_timestamps[j].index(min(imu_timestamps[j], key=lambda x: abs(x-ts)))
            # print t
            imu_indices[j].append(t)
            time += imu_timestamps[j][t]

            n += 1.0
        else:
            imu_indices[j].append(-1)
    # image_indexes.append(images.index(images[(min(image_timestamps, key=lambda x: abs(x-ts)))]))
    pickle_timestamps.append(time/n)
    image_indices.append(image_timestamps.index((min(image_timestamps, key=lambda x: abs(x-ts)))))
    arduino_indices.append(arduino_timestamps.index((min(arduino_timestamps, key=lambda x: abs(x-ts)))))


for i in range(0, min_):
    for j in range(0, len(imu_vectors)):
        if len(imu_vectors[j]) != 0:
            # print imu_indices[j][i]
            data_ = imu_vectors[j][imu_indices[j][i]]
            p_data_ = DataEntry(data_.quat.quaternion.x, data_.quat.quaternion.y,
                                data_.quat.quaternion.z, data_.quat.quaternion.w,
                                data_.gyroX, data_.gyroY, data_.gyroZ,
                                data_.accX, data_.accY, data_.accZ,
                                data_.comX, data_.comY, data_.comZ,
                                -1,
                                i)
            # print p_data_
            imu_pickle_data[j].append(p_data_)

for j in range(0, len(imu_vectors)):
    if len(imu_pickle_data[j]) != 0:
        name = pref + "_" + joint_names[j] + ".p"
        rospy.logwarn("dumping " + imu_names[j] + " to " + name)
        pickle.dump(imu_pickle_data[j], open(name, "wb"))

rospy.logwarn("dumping timestamps to " + pref + "_timestamps.p")
pickle.dump(pickle_timestamps, open(pref + "_timestamps.p", "wb"))

rospy.logwarn("dumping images to " + pref + "_images.p")
pickle.dump(images, open(pref + "_images.p", "wb"))

rospy.logwarn("dumping arduino readings to " + pref + "_arduino.p")
pickle.dump(arduino_messages, open(pref + "_arduino.p", "wb"))

rospy.logerr(str(len(images))+" images")
rospy.logerr(str(len(arduino_messages))+" arduino readings")
rospy.logwarn(str(min_)+" total frames")
rospy.shutdown()
