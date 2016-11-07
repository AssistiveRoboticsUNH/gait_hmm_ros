#!/usr/bin/env python
import roslib
import rospy
import rospkg
import pickle
import time
import math
import string
import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.io as sio


def close_event(fullpath):
    plt.savefig(fullpath[:-4] + '.png', figsize=(15, 15), dpi=180)
    plt.close()


def classify(fsr_bk, fsr_fl, fsr_fr):
    # fsrbk fsrfl fsrfr
    # print(str(arduino_reading[4])+" "+str(arduino_reading[4]) + " " + str(arduino_reading[4]))
    if (fsr_bk > 0.5) and (fsr_fr > 0.5) and (fsr_fl > 0.5):
        return 'stance'
    if (fsr_bk > 0.5) and (fsr_fr < 0.5) and (fsr_fl < 0.5):
        return 'stance'
    # if (fsr_bk > 0) and (fsr_fr > 0) and (fsr_fl > 0):
    #     return 'stance'
    return 'swing'


def fsr_annotate(fullpath):
    state_names = ['swing', 'stance']
    labels = []
    print_ = rospy.get_param('~print', 0)
    try:
        arduino_data = (sio.loadmat(fullpath))['arduino']
    except IOError:
        rospy.logerr(fullpath)
        rospy.logerr("Could not read file, exiting")

    for entry in arduino_data:
        # rospy.logwarn(str(entry[2])+" "+str(entry[3])+" "+str(entry[4]))
        labels.append(state_names.index(classify(entry[2], entry[3], entry[4])))

    # print ard_2[ard_2!=x]
    i = 0
    while i < len(labels):
        k = 0
        batch = []
        indexes = []
        while k < 5 and i < len(labels):
            batch.append(labels[i])
            indexes.append(i)
            k += 1
            i += 1
        s = sum(batch)
        if s < 2:
            for j in indexes:
                labels[j] = 0
        else:
            for j in indexes:
                labels[j] = 1

    rospy.logwarn(fullpath[:-4]+"_annotated.mat")
    gs = gridspec.GridSpec(2, 2)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])
    ax4 = plt.subplot(gs[3])
    ax1.plot(arduino_data[:, 2])
    # ax1.plot(ard[:, 2])
    ax1.set_title('FSRBK')
    ax2.plot(arduino_data[:, 3])
    # ax2.plot(ard[:, 3])
    ax2.set_title('FSRFL')
    ax3.plot(arduino_data[:, 4])
    # ax3.plot(ard[:, 4])
    ax3.set_title('FSRFR')
    ax4.plot(labels)
    ax4.set_title('LABELS')
    if print_ == 1:
        fig = plt.figure()
        timer = fig.canvas.new_timer(interval=4000)  # creating a timer object and setting an interval of 3000 milliseconds
        timer.add_callback(close_event, fullpath)
        timer.start()
        plt.show()

if __name__ == "__main__":
    rospy.init_node('fsr_annotate_2')
    rospack = rospkg.RosPack()
    path = rospack.get_path('gait_hmm_ros') + '/scripts/'
    datafile = rospy.get_param('~datafile', "")
    if datafile == "":
        rospy.logerr(datafile)
        rospy.logerr("No file found, exiting")
        exit()
    fsr_annotate(path+datafile)
