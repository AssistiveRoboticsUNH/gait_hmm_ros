#!/usr/bin/env python
import rospy
import rospkg
import geometry_msgs.msg
from threespace_ros.msg import dataVec

imu_names = ['rf', 'rll', 'rul', 'lf', 'lll', 'lua', 'lul', 'm', 'ch', 'rs', 'rua', 'rla',
             'rw', 'ls', 'lua', 'lla', 'lw']

imu_param_names = ['~rf', '~rll', '~rul', '~lf', '~lll', '~lua', '~lul', '~m', '~ch', '~rs', '~rua', '~rla',
                   '~rw', '~ls', '~lua', '~lla', '~lw']

imu_names_full = ['Right Foot', 'Right Lower Leg', 'Right Upper Leg',
                  'Left Foot', 'Left Lower Leg', 'Left Upper Leg',
                  'Mid', 'Chest',
                  'Right Shoulder', 'Right Upper Arm', 'Right Lower Arm', 'Right Wrist',
                  'Left Shoulder', 'Left Upper Arm', 'Left Lower Arm', 'Left Wrist']

dataVectors = [dataVec for i in range(0, 13)]

imu_callbacks = []
for i in range(0, 13):
    def func(msg):
        dataVectors[i].header = msg.header
        dataVectors[i].quat = msg.quat
        dataVectors[i].gyroX = msg.gyroX
        dataVectors[i].gyroY = msg.gyroY
        dataVectors[i].gyroZ = msg.gyroZ
        dataVectors[i].accX = msg.accX
        dataVectors[i].accY = msg.accY
        dataVectors[i].accZ = msg.accZ
        dataVectors[i].comX = msg.comX
        dataVectors[i].comY = msg.comY
        dataVectors[i].comZ = msg.comZ
    imu_callbacks.append(func)

