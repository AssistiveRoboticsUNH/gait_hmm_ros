#!/usr/bin/env python
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import time
import math
import UnfairCasino
from threespace_ros.msg import dataVec
from ghmm import*
from UnfairCasino import train_seq


rospy.init_node('hmm_trainer')
alphabet = ['ff','ho','sw','hs']
sigma = IntegerRange(1, 7)
A = [[0.9, 0.1], [0.3, 0.7]]
efair = [1.0/6]*6
eloaded = [3.0 / 13, 3.0 / 13, 2.0 / 13, 2.0 / 13, 2.0 / 13, 1.0 / 13]
B = [efair, eloaded]
pi = [0.5] * 2
m = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
print m 
print '*'
