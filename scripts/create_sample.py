#!/usr/bin/env python
import rospy
import rospkg
import pickle
import glob
import numpy as np
from gait_hmm_ros.msg import imu_vector
from pomegranate import*
from pomegranate import HiddenMarkovModel as HMM
from pomegranate import MultivariateGaussianDistribution as MGD
from random import randint

rospy.init_node('sample_publisher')
rospack = rospkg.RosPack()
prefix = rospy.get_param('~prefix', "quat_bte_rf_rll_rul_m_")
window = rospy.get_param('~window', 10)
data_file = rospack.get_path('gait_hmm_ros') + '/scripts/trained_classifiers/'+prefix+'full_data.p'
labels_file = rospack.get_path('gait_hmm_ros') + '/scripts/trained_classifiers/'+prefix+'full_labels.p'
window = rospy.get_param('~window', 20)
pub = rospy.Publisher('data_vector', imu_vector, queue_size=10)
labels = pickle.load(open(labels_file, 'rb)'))
data = pickle.load(open(data_file, 'rb'))
vec = imu_vector()
positive_data = []
negative_data = []
for i in range(0, len(labels)):
    if labels[i] == 1:
        positive_data.append(data[i])
    else:
        negative_data.append(data[i])

# print positive_data[0]
# print negative_data[0]

# positive_means = np.mean(positive_data, axis=0)
# rospy.logwarn(positive_means.size)
# rospy.logwarn(positive_means[0].size)
# rospy.logwarn("Positive Means : \n" + str(positive_means))
# positive_vars = np.var(positive_data, axis=0)
# rospy.logwarn("Positive Vars : \n" + str(positive_vars))
# positive_std = np.std(positive_data, axis=0)
# rospy.logwarn("Positive Standard Deviations : \n" + str(positive_std))

# negative_means = np.mean(negative_data, axis=0)
# rospy.logwarn(negative_means.size)
# rospy.logwarn(negative_means[0].size)
# rospy.logwarn("Negative Means : \n" + str(negative_means))
# negative_vars = np.var(negative_data, axis=0)
# rospy.logwarn("Negative Vars : \n" + str(negative_vars))
# negative_std = np.std(negative_data, axis=0)
# rospy.logwarn("Negative Standard Deviations : \n" + str(negative_std))

positive_dis = MGD.from_samples(positive_data)
negative_dis = MGD.from_samples(negative_data)
print positive_dis.mu
print negative_dis.mu

while not rospy.is_shutdown():
    pos = []
    neg = []
    pos_num = random.randint(0, window)
    neg_num = window-pos_num
    for i in range (0, pos_num):
        vec.header.stamp = rospy.Time.now()
        vec.data = positive_dis.sample()
        pub.publish(vec)
        pos.append(vec.data)
    for i in range(0, neg_num):
        vec.header.stamp = rospy.Time.now()
        vec.data = negative_dis.sample()
        pub.publish(vec)
        neg.append(vec.data)
    # rospy.logwarn(str(pos_num)+" "+str(pos))
    # rospy.logwarn(str(neg_num)+" "+str(neg))
    # rospy.logwarn("--------------")
