#!/usr/bin/env python
import rospy
import rospkg
import pickle
import imu_callbacks as iparam
import numpy as np
from pomegranate import*
import scipy.io as sio
from sklearn import preprocessing

rospy.init_node('create_data_combos')
input_names = []
device_names = []
imus_used = ""
joint_names = []
dup_list = []
pref = rospy.get_param('~prefix', "none")
use_quat = rospy.get_param('~use_quat', 0)
if use_quat == 1:
    input_names.append("quat")
    imus_used += "quat_"
use_gyro = rospy.get_param('~use_gyro', 0)
if use_gyro == 1:
    input_names.append("gyro")
    imus_used += "gyro_"
use_accel = rospy.get_param('~use_accel', 0)
if use_accel == 1:
    input_names.append("accel")
    imus_used += "accel_"
use_com = rospy.get_param('~use_com', 0)
if use_com == 1:
    input_names.append("com")
    imus_used += "com_"
use_fsr = rospy.get_param('~use_fsr', 0)
if use_fsr == 1:
    input_names.append("fsr")
    imus_used += "fsr_"
use_ir = rospy.get_param('~use_ir', 0)
if use_ir == 1:
    input_names.append("ir")
    imus_used += "ir_"
use_prox = rospy.get_param('~use_prox', 0)
if use_prox == 1:
    input_names.append("prox")
    imus_used += "prox_"
folds = rospy.get_param('~folds', 10)
batch_train = rospy.get_param('~batch_train', 1)
if batch_train == 1:
    imus_used += "btr_"
batch_test = rospy.get_param('~batch_test', 1)
if batch_test == 1:
    imus_used += "bte_"

rf = rospy.get_param('~rf', "")
if rf != "":
    joint_names.append("rf")
    dup_list.append(rf)

rll = rospy.get_param('~rll', "")
if rll != "":
    joint_names.append("rll")
    dup_list.append(rll)

rul = rospy.get_param('~rul', "")
if rul != "":
    joint_names.append("rul")
    dup_list.append(rul)

m = rospy.get_param('~m', "")
if m != "":
    joint_names.append("m")
    dup_list.append(m)

if len(dup_list) != len(set(dup_list)):
    rospy.logerr("Topic naming error detected, check for doubles")
    exit()

rospack = rospkg.RosPack()
fpath = rospack.get_path('gait_hmm_ros') + '/scripts/'
rospy.loginfo("Path :"+fpath)
rospy.loginfo("Use quat: "+str(use_quat))
rospy.loginfo("Use gyro: "+str(use_gyro))
rospy.loginfo("Use accel: "+str(use_accel))
rospy.loginfo("Use com: "+str(use_com))
rospy.loginfo("Use fsr: "+str(use_fsr))
rospy.loginfo("Use ir: "+str(use_ir))
rospy.loginfo("Use prox: "+str(use_prox))
rospy.loginfo("Batch train: "+str(batch_train))
rospy.loginfo("Batch test: "+str(batch_test))
rospy.loginfo("Right Foot Topic: "+rf)
rospy.loginfo("Right Lower Leg Topic: "+rll)
rospy.loginfo("Right Upper Leg Foot Topic: "+rul)
rospy.loginfo("Waist Foot Topic: "+m)

imu_names = iparam.imu_param_names

total_sensors = len(imu_names)
total_entries = 0

max_acc = 0.0
full_step_width = []
full_step_width_or = []
full_step_length = []
full_step_length_or = []
full_ml_trunk_sway = []
full_ml_trunk_sway_or = []
full_ap_trunk_sway = []
full_ap_trunk_sway_or = []
full_foot_clearance = []
full_foot_clearance_or = []
full_labels = []
full_labels_let = []
full_data = []
full_labels = []
full_normlabels = []

names = rospy.get_param('/filenames', "")
norm_labels = rospy.get_param('/normlabels', "")
rospy.logwarn(names)
if names == "":
    rospy.logerr("No files given, exiting")
    exit()
subject = rospy.get_param('/subject', "")
#####################
# Load enabled IMUS #
#####################
print names
for filename in names:
    print filename
    labelindex = names.index(filename)
    sensor_data = []
    pref = fpath + filename
    print joint_names
    for name in joint_names:
        full_name = pref + "_" + name + ".mat"
        rospy.logwarn(full_name)
        if os.path.isfile(full_name):
            if ("_" + name + "_") not in imus_used:
                imus_used += (name + "_")
            # rospy.logwarn("Loading" + full_name)
            x = sio.loadmat(full_name)
            x = x.get(name)
            total_entries = len(x)
            data_entry = []
            for i in range(0, len(x)):
                entry = []
                if use_quat == 1:
                    entry = np.concatenate((entry, x[i, 0:4]), axis=0)
                if use_gyro == 1:
                    entry = np.concatenate((entry, x[i, 4:7]), axis=0)
                if use_accel == 1:
                    entry = np.concatenate((entry, x[i, 7:10]), axis=0)
                if use_com == 1:
                    entry = np.concatenate((entry, x[i, 10:13]), axis=0)
                # rospy.logwarn(len(entry))
                data_entry.append(entry)
            if sensor_data == []:
                sensor_data = data_entry
            else:
                sensor_data = np.concatenate((sensor_data, data_entry), axis=1)
        else:
            rospy.logerr("Data file not found : "+full_name)
            exit()


    x = []
    arduino = sio.loadmat(pref + "_arduino.mat")
    arduino = arduino.get("arduino")
    arduino_data = []

    for i in range(0, len(arduino)):
        entry = []
        # print arduino[i, 2:]
        if use_fsr == 1:
            # print (arduino[i, 3:6])
            entry = np.concatenate((entry, arduino[i, 2:5]), axis=0)
        if use_ir == 1:
            # print(arduino[i, 7])
            entry = np.concatenate((entry, arduino[i, 5:6]), axis=0)
        if use_prox == 1:
            entry = np.concatenate((entry, arduino[i, 6:7]), axis=0)
        arduino_data.append(entry)

    if sensor_data!=[]:
        sensor_data = np.concatenate((sensor_data, arduino_data), axis=1)
    else:
        sensor_data = arduino_data

    if full_data == []:
        full_data = sensor_data
    else:
        full_data = np.concatenate((full_data, sensor_data), axis=0)

    # FOOT CLEARANCE
    foot_clearance = sio.loadmat(pref + "_foot_clearance.mat")
    foot_clearance = foot_clearance.get("foot_clearance")[0]
    # print foot_clearance
    if full_foot_clearance == []:
        full_foot_clearance = foot_clearance
    else:
        full_foot_clearance = np.hstack((full_foot_clearance, foot_clearance))

    foot_clearance_or = sio.loadmat(pref + "_foot_clearance_or.mat")
    foot_clearance_or = foot_clearance_or.get('foot_clearance')[0]
    # print foot_clearance_or
    if full_foot_clearance_or == []:
        full_foot_clearance_or = foot_clearance_or
    else:
        full_foot_clearance_or = np.hstack((full_foot_clearance_or, foot_clearance_or))

    # STEP WIDTH
    step_width = sio.loadmat(pref + "_step_width.mat")
    step_width = step_width.get('step_width')[0]
    # print step_width
    if full_step_width == []:
        full_step_width = step_width
    else:
        full_step_width = np.hstack((full_step_width, step_width))

    step_width_or = sio.loadmat(pref + "_step_width_or.mat")
    step_width_or = step_width_or.get('step_width')[0]
    # print step_width_or
    if full_step_width_or == []:
        full_step_width_or = step_width_or
    else:
        full_step_width_or = np.hstack((full_step_width_or, step_width_or))

    # STEP LENGTH
    step_length = sio.loadmat(pref + "_step_length.mat")
    step_length = step_length.get('step_length')[0]
    # print step_length
    if full_step_length == []:
        full_step_length = step_length
    else:
        full_step_length = np.hstack((full_step_length, step_length))

    step_length_or = sio.loadmat(pref + "_step_length_or.mat")
    step_length_or = step_length_or.get('step_length')[0]
    # print step_length_or
    if full_step_length_or == []:
        full_step_length_or = step_length_or
    else:
        full_step_length_or = np.hstack((full_step_length_or, step_length_or))

    # AP TRUNK SWAY
    ap_trunk_sway = sio.loadmat(pref + "_ap_trunk_sway.mat")
    ap_trunk_sway = ap_trunk_sway.get('ap_trunk_sway')[0]
    # print ap_trunk_sway
    if full_ap_trunk_sway == []:
        full_ap_trunk_sway = ap_trunk_sway
    else:
        full_ap_trunk_sway = np.hstack((full_ap_trunk_sway, ap_trunk_sway))

    ap_trunk_sway_or = sio.loadmat(pref + "_ap_trunk_sway_or.mat")
    ap_trunk_sway_or = ap_trunk_sway_or.get('ap_trunk_sway')[0]
    # print ap_trunk_sway_or
    if full_ap_trunk_sway_or == []:
        full_ap_trunk_sway_or = ap_trunk_sway_or
    else:
        full_ap_trunk_sway_or = np.hstack((full_ap_trunk_sway_or, ap_trunk_sway_or))

    # ML TRUNK SWAY
    ml_trunk_sway = sio.loadmat(pref + "_ml_trunk_sway.mat")
    ml_trunk_sway = ml_trunk_sway.get('ml_trunk_sway')[0]
    # print ml_trunk_sway_or
    if full_ml_trunk_sway == []:
        full_ml_trunk_sway = ml_trunk_sway
    else:
        full_ml_trunk_sway = np.hstack((full_ml_trunk_sway, ml_trunk_sway))

    ml_trunk_sway_or = sio.loadmat(pref + "_ml_trunk_sway_or.mat")
    ml_trunk_sway_or = ml_trunk_sway_or.get('ml_trunk_sway')[0]
    # print ml_trunk_sway_or
    if full_ml_trunk_sway_or == []:
        full_ml_trunk_sway_or = ml_trunk_sway_or
    else:
        full_ml_trunk_sway_or = np.hstack((full_ml_trunk_sway_or, ml_trunk_sway_or))

    # LABELS
    labels = sio.loadmat(pref + "_labels_annotated.mat")
    labels = labels.get('labels')[0]
    # print labels
    if full_labels == []:
        full_labels = labels
    else:
        full_labels = np.hstack((full_labels, labels))

    labels_let = sio.loadmat(pref + "_labels_annotated_let.mat")
    labels_let = labels_let.get('labels')
    # print labels_let
    if full_labels_let == []:
        full_labels_let = labels_let
    else:
        full_labels_let = np.hstack((full_labels_let, labels_let))
    # gait type
    if names.index(filename) == 0:
        full_normlabels = [0 for i in range(0, len(arduino))]
        continue
    elif names.index(filename) == 1:
        normal = [1 for i in range(0, len(arduino))]
        full_normlabels = np.hstack((full_normlabels, normal))
        continue
    elif names.index(filename) == 2:
        normal = [2 for i in range(0, len(arduino))]
        full_normlabels = np.hstack((full_normlabels, normal))
        continue
    elif names.index(filename) == 3:
        normal = [3 for i in range(0, len(arduino))]
        full_normlabels = np.hstack((full_normlabels, normal))
        continue
    elif names.index(filename) == 4:
        normal = [4 for i in range(0, len(arduino))]
        full_normlabels = np.hstack((full_normlabels, normal))
        continue
    else:
        rospy.logerr("SOMETHING IS WRONG WITH THE FILENAMES, EXITING")
        rospy.shutdown()
        exit()

print full_normlabels
rospy.logwarn(np.array(full_data).shape)
rospy.logwarn(np.array(full_normlabels).shape)
rospy.logwarn(np.array(full_labels).shape)
rospy.logwarn(np.array(full_labels_let).shape)
rospy.logwarn(np.array(full_foot_clearance).shape)
rospy.logwarn(np.array(full_step_width).shape)
rospy.logwarn(np.array(full_step_length).shape)
rospy.logwarn(np.array(full_ap_trunk_sway).shape)
rospy.logwarn(np.array(full_ml_trunk_sway).shape)
rospy.logwarn(np.array(full_foot_clearance_or).shape)
rospy.logwarn(np.array(full_step_width_or).shape)
rospy.logwarn(np.array(full_step_length_or).shape)
rospy.logwarn(np.array(full_ap_trunk_sway_or).shape)
rospy.logwarn(np.array(full_ml_trunk_sway_or).shape)
rospy.logwarn(imus_used)
rospy.logwarn(input_names)
rospy.logwarn(names)

labels = []
sensor_data = []

# normalized_data = preprocessing.normalize(full_data, norm='l1', axis=0)
# normalized_data = (full_data - full_data.min(0))/full_data.ptp(0)
# normalized_data = full_data/full_data.max(axis=0)

mins = np.min(full_data, axis=0)
maxs = np.max(full_data, axis=0)
rng = maxs - mins
normalized_data = 1.0 - (((1.0 - 0.0) * (maxs - full_data)) / rng)

print(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data.mat")
pickle.dump(full_data, open(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data.p", 'wb'))
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data.mat", mdict={"data": full_data})

pickle.dump(normalized_data, open(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data_normalized.p", 'wb'))
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data_normalized.mat",
            mdict={"data": normalized_data})

pickle.dump(full_normlabels, open(fpath+"/new_bags/datasets/"+subject+"_normal_labels.p", 'wb'))
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_normal_labels.mat", mdict={"norm_labels": full_normlabels})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_foot_clearance.mat", mdict={"foot_clearance": full_foot_clearance})
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_foot_clearance_or.mat",
            mdict={"foot_clearance": full_foot_clearance_or})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_step_width.mat", mdict={"step_width": full_step_width})
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_step_width_or.mat", mdict={"step_width": full_step_width_or})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_step_length.mat", mdict={"step_length": full_step_length})
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_step_length_or.mat", mdict={"step_length": full_step_length_or})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_ml_trunk_sway.mat", mdict={"ml_trunk_sway": full_ml_trunk_sway})
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_ml_trunk_sway_or.mat", mdict={"ml_trunk_sway": full_ml_trunk_sway_or})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_ap_trunk_sway.mat", mdict={"ap_trunk_sway": full_ap_trunk_sway})
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_ap_trunk_sway_or.mat", mdict={"ap_trunk_sway": full_ap_trunk_sway_or})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_labels.mat", mdict={"labels": full_labels})
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_labels_let.mat", mdict={"labels": full_labels_let})

sio.savemat(fpath+"/new_bags/datasets/"+subject+"_norm_labels.mat", mdict={"norm_labels": norm_labels})
