#!/usr/bin/env python
import roslib
import rospy
import rospkg
import pickle
import matplotlib.pyplot as plt
import scipy.io as sio
from bisect import bisect_left


# get phase of walking from mocap annotations
def two_phase_assign(lower, upper, leg='right'):
    if lower == 'LTO':
        if upper == 'LTO' or upper == 'LHS':
            return 'stance'
    elif lower == 'LHS':
        if upper == 'LHS' or upper == 'RTO':
            return 'stance'
    elif lower == 'RTO':
        if upper == 'RHS' or upper == 'RTO':
            return 'swing'
    elif lower == 'RHS':
        if upper == 'RHS' or upper == 'LTO':
            return 'stance'
    print("NO VALID ASSIGNMENT, EXITING")
    exit()


def align(target, array):
    ret = []
    tar_ind = [float(i) / float(len(target)) for i in range(0, len(target))]
    arr_ind = [float(i) / float(len(array)) for i in range(0, len(array))]
    for i in range(0, len(tar_ind) - 1):
        pos = bisect_left(arr_ind, tar_ind[i])
        if pos == 0:
            ret.append(array[0])
            ret.append(0)
            continue
        if pos == len(arr_ind):
            ret.append(array[pos - 1])
            continue
        before = array[pos - 1]
        after = array[pos]
        if after - tar_ind[i] < tar_ind[i] - before:
            ret.append(after)
        else:
            ret.append(before)

    print (ret[len(ret) - 1])
    print (array[len(array) - 1])
    print (target[len(target) - 1])
    print (len(ret))
    print("-----------------------")
    return ret


class Annotator:
    def __init__(self, matfile, pref, label_fun=two_phase_assign):

        self.annotate = label_fun
        # Load the sensor timestamps
        imu_timestamps = sio.loadmat(pref + "_timestamps.mat")
        imu_timestamps = imu_timestamps.get('timestamps')[0]
        total_entries = len(imu_timestamps)
        rospy.logwarn("Loaded " + str(total_entries) + " timestamps from " + pref + "_timestamps.mat")
        # print total_entries
        rl_timestamps = []
        #############################################
        # Transform ROS timestamps to duration from #
        # start of recording                        #
        #############################################
        for i in imu_timestamps:
            rl_timestamps.append(abs(i - imu_timestamps[0]) / 1000000000)

        mocap_data = []
        labels = []
        mocap_labels = ['LHS', 'LTO', 'RHS', 'RTO']
        mocap_indexes = [0, 0, 0, 0]
        two_phase_labels = ['swing', 'stance']

        lhs = matfile_data.get('LHS')[0][0]
        lto = matfile_data.get('LTO')[0][0]
        rhs = matfile_data.get('RHS')[0][0]
        rto = matfile_data.get('RTO')[0][0]
        step_width = matfile.get('StrideWidth')[0][0][:, 0]
        step_width_or = step_width
        step_width = align(imu_timestamps, step_width)
        step_length = matfile.get('RStepLength')[0][0][:, 0]
        step_length_or = step_length
        step_length = align(imu_timestamps, step_length)
        foot_clearance = matfile.get('R5thToePosition')[0][0][:, 2]
        foot_clearance_or = foot_clearance
        foot_clearance = align(imu_timestamps, foot_clearance)
        ap_trunk_sway = matfile.get('COMmovement')[0][0][:, 0]
        ap_trunk_sway = ap_trunk_sway[1:-1]  # remove first and last elements that ara NaN
        ap_trunk_sway_or = ap_trunk_sway
        ap_trunk_sway = align(imu_timestamps, ap_trunk_sway)
        ml_trunk_sway = matfile.get('COMmovement')[0][0][:, 1]
        ml_trunk_sway = ml_trunk_sway[1:-1]  # remove first and last elements that ara NaN
        ml_trunk_sway_or = ml_trunk_sway
        ml_trunk_sway = align(imu_timestamps, ml_trunk_sway)

        mocap_lists = [lhs, lto, rhs, rto]

        mocap_size = len(lhs) + len(lto) + len(rhs) + len(rto)
        print (mocap_size)
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
        i = 0
        while i < mocap_size:
            current_index = start_index % 4
            mocap_data.append((mocap_labels[current_index], mocap_lists[current_index][mocap_indexes[current_index]]))
            mocap_indexes[current_index] += 1
            start_index -= 1
            i += 1
        start_mocap = mocap_data[0][1]
        end_mocap = mocap_data[mocap_size - 1][1]
        rospy.logwarn(start_mocap)
        rospy.logwarn(end_mocap)

        ###############################################
        # FOR EACH ROS IMU TIMESTAMP                  #
        # TRY TO FIND WHICH MOCAP EVENT IT IS BETWEEN #
        # AND ASSIGN CORRESPONDING LABEL              #
        ###############################################
        lower_index = 0
        upper_index = 0
        i = 0
        while i < total_entries:
            rospy.loginfo("#" + str(i) + ": Lower Index :" + str(lower_index) + ", Upper Index :" + str(upper_index))
            if rl_timestamps[i] < mocap_data[0][1]:
                rospy.logwarn(str(rl_timestamps[i]) + " is smaller than " +
                              str(mocap_data[0][0]) +
                              str(mocap_data[0][1])[0:10] + "]")
            elif rl_timestamps[i] > mocap_data[len(mocap_data) - 1][1]:
                rospy.logwarn(str(rl_timestamps[i]) + " is greater than " +
                              str(mocap_data[len(mocap_data) - 1][0]) + " " +
                              str(mocap_data[len(mocap_data) - 1][1])[0:10] + "]")
            else:
                while rl_timestamps[i] > mocap_data[lower_index][1] and lower_index < len(mocap_data) - 1:
                    lower_index += 1
                lower_index -= 1
                upper_index = lower_index + 1
                while rl_timestamps[i] > mocap_data[upper_index][1] and upper_index < len(mocap_data) - 1:
                    upper_index += 1
                rospy.logwarn(str(rl_timestamps[i]) + " is between " + str(lower_index) + " : " +
                              str(mocap_data[lower_index][0]) +
                              str(mocap_data[lower_index][1])[0:10] + "] and " +
                              str(upper_index) + " : " +
                              str(mocap_data[upper_index][0]) + " " +
                              str(mocap_data[upper_index][1])[0:10] + "]")

            # APPEND THE LABEL TO THE ANNOTATION LIST
            labels.append(two_phase_labels.index(self.annotate(mocap_data[lower_index][0], mocap_data[upper_index][0])))

            # FIND THE INDEX OF THE MOCAP DATA WHICH IS CLOSES TO THE CURRENT
            # RECORDED ELEMENT AND APPEND THAT TO THE ARRAY
            i += 1

        letter_labels = [two_phase_labels[i] for i in labels]
        rospy.logwarn("Dumping " + str(len(labels)) + " labels to " + pref + "_labels_annotated.mat")
        sio.savemat(pref + "_labels_annotated.mat", mdict={'labels': labels})
        rospy.logwarn("Dumping " + str(len(letter_labels)) + " labels to " + pref + "_labels_annotated_let.mat")
        sio.savemat(pref + "_labels_annotated_let.mat", mdict={'labels': letter_labels})

        rospy.logwarn("Dumping " + str(len(foot_clearance)) + " entries for foot clearance to "
                      + pref + "_foot_clearance.mat")
        sio.savemat(pref + "_foot_clearance.mat", mdict={'foot_clearance': foot_clearance})
        rospy.logwarn("Dumping " + str(len(foot_clearance_or)) + " entries for foot clearanceto "
                      + pref + "_foot_clearance_or.mat")
        sio.savemat(pref + "_foot_clearance_or.mat", mdict={'foot_clearance': foot_clearance_or})

        rospy.logwarn("Dumping " + str(len(step_width)) + " entries for step width to " + pref + "_step_width.mat")
        sio.savemat(pref + "_step_width.mat", mdict={'step_width': step_width})
        rospy.logwarn("Dumping " + str(len(step_width_or)) + " entries for step width to "
                      + pref + "_step_width_or.mat")
        sio.savemat(pref + "_step_width_or.mat", mdict={'step_width': step_width_or})

        rospy.logwarn("Dumping " + str(len(step_length)) + " entries for step length to " + pref + "_step_length.mat")
        sio.savemat(pref + "_step_length.mat", mdict={'step_length': step_length})
        rospy.logwarn("Dumping " + str(len(step_length_or)) + " entries for step length to "
                      + pref + "_step_length_or.mat")
        sio.savemat(pref + "_step_length_or.mat", mdict={'step_length': step_length_or})

        rospy.logwarn("Dumping " + str(len(ap_trunk_sway)) + " entries for anterior posterior trunk sway to "
                      + pref + "_ap_trunk_sway.mat")
        sio.savemat(pref + "_ap_trunk_sway.mat", mdict={'ap_trunk_sway': ap_trunk_sway})
        rospy.logwarn("Dumping " + str(len(ap_trunk_sway_or)) + " entries for anterior posterior trunk sway to "
                      + pref + "_ap_trunk_sway_or.mat")
        sio.savemat(pref + "_ap_trunk_sway_or.mat", mdict={'ap_trunk_sway': ap_trunk_sway_or})

        rospy.logwarn("Dumping " + str(len(ml_trunk_sway)) + " entries for medio-lateral trunk sway to " +
                      pref + "_ml_trunk_sway.mat")
        sio.savemat(pref + "_ml_trunk_sway.mat", mdict={'ml_trunk_sway': ml_trunk_sway})
        rospy.logwarn("Dumping " + str(len(ml_trunk_sway_or)) + " entries for medio-lateral trunk sway to " +
                      pref + "_ml_trunk_sway_or.mat")
        sio.savemat(pref + "_ml_trunk_sway_or.mat", mdict={'ml_trunk_sway': ml_trunk_sway_or})

        f, axarr = plt.subplots(2, 3)
        axarr[0, 0].plot(ml_trunk_sway)
        axarr[0, 0].set_title('ml_trunk_sway')

        axarr[0, 1].plot(ap_trunk_sway)
        axarr[0, 1].set_title('ap_trunk_sway')

        axarr[0, 2].plot(labels)
        axarr[0, 2].set_title('labels')

        axarr[1, 0].plot(foot_clearance)
        axarr[1, 0].set_title('foot_clearance')

        axarr[1, 1].plot(step_width)
        axarr[1, 1].set_title('step_width')

        axarr[1, 2].plot(step_length)
        axarr[1, 2].set_title('step_length')

        plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
        plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

        pickle.dump(f, open(pref + '_figure.p', 'wb'))
        plt.savefig(pref + '_figure.png')

        f, axarr2 = plt.subplots(2, 3)
        axarr2[0, 0].plot(ml_trunk_sway_or)
        axarr2[0, 0].set_title('ml_trunk_sway_or')

        axarr2[0, 1].plot(ap_trunk_sway_or)
        axarr2[0, 1].set_title('ap_trunk_sway_or')

        axarr2[1, 0].plot(foot_clearance_or)
        axarr[1, 0].set_title('foot_clearance_or')

        axarr2[1, 1].plot(step_width_or)
        axarr2[1, 1].set_title('step_width_or')

        axarr2[1, 2].plot(step_length_or)
        axarr2[1, 2].set_title('step_length_or')

        plt.setp([a.get_xticklabels() for a in axarr2[0, :]], visible=False)
        plt.setp([a.get_yticklabels() for a in axarr2[:, 1]], visible=False)

        pickle.dump(f, open(pref + '_figure_or.p', 'wb'))
        plt.savefig(pref + '_figure_or.png')

        exit()


if __name__ == "__main__":
    rospy.init_node('auto_annotate')
    #######################
    #    READ FILE NAME   #
    #######################
    rospy.init_node('auto_annotate')
    pref = rospy.get_param('~prefix', "none")
    auto = rospy.get_param('~auto', "False")
    rospack = rospkg.RosPack()
    path = rospack.get_path('gait_hmm_ros') + '/scripts/'
    pref = path + pref

    matfile = rospy.get_param('~matfile', "none")
    if matfile != "none":
        matfile_data = sio.loadmat(path + matfile)
    else:
        rospy.logerr("No matfile found, exiting")
        rospy.shutdown()
        exit()

    Annotator(matfile_data, pref)
