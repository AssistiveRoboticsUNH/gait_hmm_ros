#!/usr/bin/env python
import rospy
import rospkg
import pickle
import scipy.io as sio


def assign_label_a(lower, upper, leg):
    # if leg == left:
    if lower == 'LTO':
        if upper == 'LTO' or upper == 'LHS':
            if leg == 'right':
                return 'stance'
            else:
                return 'swing'
    elif lower == 'LHS':
        if upper == 'LHS' or upper == 'RTO':
            if leg == 'right':
                return 'stance'
            else:
                return 'swing'
    elif lower == 'RTO':
        if upper == 'RTO' or upper == 'RHS':
            if leg == 'right':
                return 'swing'
            else:
                return 'stance'
    else:
        if upper == 'RHS' or upper == 'LTO':
            if leg == 'right':
                return 'stance'
            else:
                return 'swing'


rospy.init_node('align_mocap')
rospack = rospkg.RosPack()

prefix = rospy.get_param('~prefix', "none")

path = rospack.get_path('gait_hmm_ros') + '/scripts/'

if prefix == "none":
    rospy.logerr("No data file given")
    exit()

leg = "right"

matfile = rospy.get_param('~matfile', "none")

if matfile == "none":
    rospy.logerr("No mocap data given")
    exit()
matfile_data = sio.loadmat(path + matfile)

rospack = rospkg.RosPack()

imu_timestamps = sio.loadmat(path + prefix + "_timestamps.mat")
imu_timestamps = imu_timestamps['timestamps'][0]
l = len(imu_timestamps)
rl_timestamps = []

for i in imu_timestamps:
    rl_timestamps.append(abs(i - imu_timestamps[0]) / 1000000000)

mocap_data = []
mocap_annotated = []
class_pickle = []
mocap_labels = ['LHS', 'LTO', 'RHS', 'RTO']
mocap_indexes = [0, 0, 0, 0]
phase_labels_a = ['swing', 'stance']
phase_indices_a = [0, 1]

print(imu_timestamps)

total_entries = len(imu_timestamps)
lhs = matfile_data['LHS'][0][0]
lto = matfile_data['LTO'][0][0]
rhs = matfile_data['RHS'][0][0]
rto = matfile_data['RTO'][0][0]
mocap_lists = [lhs, lto, rhs, rto]

mocap_lists = [lhs, lto, rhs, rto]

mocap_size = len(lhs) + len(lto) + len(rhs) + len(rto)

first_row = (lhs[0], lto[0], rhs[0], rto[0])
rospy.loginfo("First Row : " + str(first_row))
start_label = mocap_labels[first_row.index(min(first_row))]
rospy.loginfo("Start Label : " + start_label)
start_index = mocap_labels.index(start_label)
rospy.loginfo("Start Index : " + str(start_index))
######################################
# SCRIPT WILL TRANSFORM THE MAT FILE #
# TO AN ARRAY WITH SEQUENTIAL  GAIT  #
# EVENTS AND TIMESTAMPS              #
######################################
print (mocap_size)
print (len(lhs))
print (len(lto))
print (len(rhs))
print (len(rto))
for i in range(0, mocap_size):
    current_index = start_index % 4
    if(mocap_indexes[current_index]) < len(mocap_lists[current_index]):
        mocap_data.append((mocap_labels[current_index],
                           mocap_lists[current_index]
                           [mocap_indexes[current_index]]))
    mocap_indexes[current_index] += 1
    start_index -= 1
    i += 1

i = 0
lower_index = 0
upper_index = 0

for i in range(0, total_entries):
    if rl_timestamps[i] < mocap_data[0][1]:
        lower_bound = mocap_data[0][0]
    elif rl_timestamps[i] > mocap_data[len(mocap_data) - 1][1]:
        x = 0
    else:

        while rl_timestamps[i] > mocap_data[lower_index][1] and lower_index < len(mocap_data) - 1:
            lower_index += 1
        lower_index -= 1
        upper_index = lower_index + 1
        while rl_timestamps[i] > mocap_data[upper_index][1] and upper_index < len(mocap_data) - 1:
            upper_index += 1
    mocap_annotated.append(phase_labels_a.index(assign_label_a(str(mocap_data[lower_index][0]),
                                                               str(mocap_data[upper_index][0]), leg)))


rospy.logwarn("Dumping mocap pickle to " + path + prefix + "_mocap_pickle.p")
pickle.dump(mocap_data, open(path + prefix + "_mocap_pickle.p", "wb"))
rospy.logwarn("Dumping labels to " + path + prefix + "_labels_mocap_annotated.p")
pickle.dump(mocap_annotated, open(path + prefix + "_labels_mocap_annotated.p", "wb"))
rospy.logwarn("Dumping labels to " + path + prefix + "_labels_mocap_annotated.mat")
sio.savemat(path + prefix + "_labels_mocap_annotated.mat", mdict={'labels': mocap_annotated})
