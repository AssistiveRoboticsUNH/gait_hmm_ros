#!/usr/bin/env python

# Software License Agreement (BSD License)
#
#  Copyright (c) 2011, UC Regents
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   * Redistributions of source code must#!/usr/bin/env python
import roslib
import rospy
import tf
import tf2_ros
import rosbag
import rospkg
import sys
import scipy.io as sio
import imu_callbacks as iparam
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from sklearn import preprocessing
import pandas
from pandas import rolling_median
from sklearn import svm
from sklearn.covariance import EllipticEnvelope


def remove_outliers_bis(arr, k):
    mask = np.ones((arr.shape[0],), dtype=np.bool)
    mu, sigma = np.mean(arr, axis=0), np.std(arr, axis=0, ddof=1)
    print mu
    for j in range(arr.shape[1]):
        col = arr[:, j]
        for m in range(arr.shape[0]):
            if np.abs((arr[m][j] - mu[j]) / sigma[j]) > k:
                print 'lol'
                arr[m][j] = mu[j]
    print arr.shape
    print mask.shape
    return arr


def bag2mat(bag):
    matfile = rospy.get_param('~matfile', "none")
    if matfile != "none":
        matfile_data = sio.loadmat(matfile)

    joint_names = iparam.imu_names

    joint_names_full = iparam.imu_names_full

    imu_names = iparam.imu_names

    imu_vectors = [[] for i in range(0, len(imu_names))]
    imu_pickle_data = [[] for i in range(0, len(imu_names))]
    imu_timestamps = [[] for i in range(0, len(imu_names))]
    imu_indices = [[] for i in range(0, len(imu_names))]
    imu_enable = [0 for i in range(0, len(imu_names))]
    imu_topics = ["" for i in range(0, len(imu_names))]

    images = []
    image_timestamps = []
    pickle_timestamps = []
    arduino_messages = []
    arduino_timestamps = []
    arduino_indices = []
    arduino_pickle_data = []

    for i in range(0, len(imu_names)):
        imu_topics[i] = rospy.get_param('/'+imu_names[i], imu_enable[i])
        if imu_topics[i] != 0:
            rospy.logwarn(joint_names_full[i]+" topic : "+imu_topics[i])

    for topic, msg, t in bag.read_messages():
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
        if len(imu_vectors[i]) != 0:
            rospy.logwarn(str(len(imu_vectors[i]))+" frames in "+imu_names[i])
        if len(imu_vectors[i]) != 0:
            if len(imu_vectors[i]) < min_:
                min_ = len(imu_vectors[i])
                min_index = i

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
        # image_indices.append(image_timestamps.index((min(image_timestamps, key=lambda x: abs(x-ts)))))
        arduino_indices.append(arduino_timestamps.index((min(arduino_timestamps, key=lambda x: abs(x-ts)))))


    for i in range(0, min_):
        for j in range(0, len(imu_vectors)):
            if len(imu_vectors[j]) != 0:
                # print imu_indices[j]
                # print imu_indices[j][i]
                data_ = imu_vectors[j][imu_indices[j][i]]
                imu_pickle_data[j].append([data_.quat.quaternion.x, data_.quat.quaternion.y,
                                           data_.quat.quaternion.z, data_.quat.quaternion.w,
                                           data_.gyroX, data_.gyroY, data_.gyroZ,
                                           data_.accX, data_.accY, data_.accZ,
                                           data_.comX, data_.comY, data_.comZ,
                                           # -1,
                                           # i
                                           ])

        ard = arduino_messages[arduino_indices[i]]
        arduino_pickle_data.append([ard.header.stamp.secs, ard.header.stamp.nsecs, ard.fsrbk, ard.fsrfl,
                                    ard.fsrfr, ard.ir, ard.prox])

    ard_1 = np.array(arduino_pickle_data)[:, [0, 1]]
    ard_2 = np.array(arduino_pickle_data)[:, 2:]

    print len(ard_2)
    print len(ard_2[0])
    print len(ard_2.T[0])

    ard_2 = remove_outliers_bis(ard_2, 3)

    arduino_pickle_data = np.concatenate((ard_1, ard_2), axis=1)

    mins = np.min(ard_2, axis=0)
    maxs = np.max(ard_2, axis=0)
    rng = maxs - mins
    ard_2 = 1.0 - (((1.0 - 0.0) * (maxs - ard_2)) / rng)

    arduino_normalized = np.concatenate((ard_1, ard_2), axis=1)
    # print arduino_normalized.shape
    # rospy.logerr(str(len(image_indices))+" images")
    # rospy.logerr(str(len(arduino_indices))+" arduino readings")
    rospy.logwarn(str(min_)+" total frames")

    full_data = []
    full_normalized = []

    for j in range(0, len(imu_vectors)):
        if len(imu_pickle_data[j]) != 0:
            name = pref + "_" + joint_names[j] + ".mat"
            rospy.logwarn("dumping " + imu_names[j] + " with " + str(len(imu_pickle_data[j])) + " entries to " + name)
            # pickle.dump(imu_pickle_data[j], open(name, "wb"))
            sio.savemat(name, mdict={joint_names[j]: imu_pickle_data[j]})
            # sio.savemat(name, imu_pickle_data[j])
            if full_data == []:
                full_data = imu_pickle_data[j]
            else:
                full_data = np.hstack((full_data, imu_pickle_data[j]))
            # full_data.append(imu_pickle_data[j])
            name = pref + "_" + joint_names[j] + "_normalized.mat"

            mins = np.min(imu_pickle_data[j], axis=0)
            maxs = np.max(imu_pickle_data[j], axis=0)
            rng = maxs - mins
            normalized = 1.0 - (((1.0 - 0.0) * (maxs - imu_pickle_data[j])) / rng)

            # normalized = preprocessing.normalize(imu_pickle_data[j], norm='l1')
            if full_normalized == []:
                full_normalized = normalized
            else:
                full_normalized = np.hstack((full_normalized, normalized))
            # full_normalized = full_normalized.append(normalized)
            rospy.logwarn("dumping normalized " + imu_names[j] + " with " + str(len(normalized)) + " entries to " + name)
            sio.savemat(name, mdict={joint_names[j]+"_normalized": normalized})
            rospy.logwarn(np.array(imu_pickle_data[j]).shape)
            rospy.logwarn(np.array(normalized).shape)
            rospy.logwarn('-------------------------------------------------------------')

    rospy.logwarn("dumping full normalized with " + str(len(full_normalized)) + " entries to " + pref + "_full_normalized.mat")
    sio.savemat(pref + "_full_normalized.mat", mdict={"data": full_normalized})
    rospy.logwarn(np.array(full_normalized).shape)
    rospy.logwarn('-------------------------------------------------------------')
    rospy.logwarn("dumping full data with " + str(len(full_data)) + " entries to " + pref + "_full_data.mat")
    sio.savemat(pref + "_full_data.mat", mdict={"data": full_data})
    rospy.logwarn(np.array(full_data).shape)
    rospy.logwarn('-------------------------------------------------------------')
    rospy.logwarn("dumping timestamps to " + pref + "_timestamps.mat")
    sio.savemat(pref + "_timestamps.mat", mdict={"timestamps": pickle_timestamps})
    rospy.logwarn('-------------------------------------------------------------')
    # rospy.logwarn("dumping image indices to " + pref + "_im_index.mat")
    # sio.savemat(pref + "_im_index.mat", mdict={"im_ind": image_indices})
    rospy.logwarn("dumping arduino indices to " + pref + "_ar_index.mat")
    sio.savemat(pref + "_ar_index.mat", mdict={"ar_ind": arduino_indices})
    rospy.logwarn('-------------------------------------------------------------')
    rospy.logwarn("dumping " + str(len(arduino_pickle_data)) + " arduino readings to " + pref + "_arduino.mat")
    sio.savemat(pref + "_arduino.mat", mdict={'arduino': arduino_pickle_data})
    rospy.logwarn(np.array(arduino_pickle_data).shape)
    rospy.logwarn('-------------------------------------------------------------')
    rospy.logwarn("dumping " + str(len(arduino_normalized)) + " normalized arduino readings to " + pref + "_arduino_normalized.mat")
    sio.savemat(pref + "_arduino_normalized.mat", mdict={'arduino': arduino_normalized})
    rospy.logwarn(np.array(arduino_normalized).shape)

if __name__ == "__main__":
    rospy.init_node('bag2mat')
    #######################
    #    READ FILE NAME   #
    #######################
    pref = rospy.get_param('~prefix', "none")
    if pref == "none":
        rospy.logerr("No input file given, exiting")
        exit()
    rospack = rospkg.RosPack()

    pref = rospack.get_path('gait_hmm_ros') + '/scripts/' + pref

    bag = rosbag.Bag(pref + '.bag')

    matfile = rospy.get_param('~matfile', "none")
    if matfile != "none":
        matfile_data = sio.loadmat(matfile)

    bag2mat(bag)
