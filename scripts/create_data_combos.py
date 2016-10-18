#!/usr/bin/env python
import rospy
import rospkg
import pickle
import imu_callbacks as iparam
from pomegranate import*
import scipy.io as sio
from sklearn import preprocessing

rospy.init_node('create_data_combos')
input_names = []
device_names = []
imus_used = ""
joint_names = []
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

rll = rospy.get_param('~rll', "")
if rll != "":
    joint_names.append("rll")

rul = rospy.get_param('~rll', "")
if rul != "":
    joint_names.append("rul")

m = rospy.get_param('~m', "")
if m != "":
    joint_names.append("m")

rospack = rospkg.RosPack()
fpath = rospack.get_path('gait_hmm_ros') + '/scripts/'
stats = []
print("Path :"+fpath)
print("Use quat: "+str(use_quat))
print("Use gyro: "+str(use_gyro))
print("Use accel: "+str(use_accel))
print("Use com: "+str(use_com))
print("Use fsr: "+str(use_fsr))
print("Use ir: "+str(use_ir))
print("Use prox: "+str(use_prox))
print("Batch train: "+str(batch_train))
print("Batch test: "+str(batch_test))
print("Right Foot Topic: "+rf)
print("Right Lower Leg Topic: "+rll)
print("Right Upper Leg Foot Topic: "+rul)
print("Waist Foot Topic: "+m)
print joint_names

imu_names = iparam.imu_param_names

total_sensors = len(imu_names)
total_entries = 0

max_acc = 0.0

full_data = []
full_labels = []
class_data = [[] for x in range(0, 2)]

# names = ['new_bags/subject1_1', 'new_bags/subject1_2', 'new_bags/subject1_3', 'new_bags/subject1_4',
#          'new_bags/subject1_5', 'new_bags/subject1_6']

names = rospy.get_param('/filenames', "")
norm_labels = rospy.get_param('/normlabels', "")
rospy.logwarn(names)
if names == "":
    rospy.logerr("No files given, exiting")
    exit()
subject = rospy.get_param('/subject', "")
normlabels = []
#####################
# Load enabled IMUS #
#####################
labels_added = 0
for filename in names:
    labels_added = 0
    labelindex = names.index(filename)
    sensor_data = []
    pref = fpath + filename
    for name in joint_names:
        full_name = pref + "_" + name + ".mat"
        # rospy.logwarn(full_name)
        if os.path.isfile(full_name):
            if name not in imus_used:
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
                if labels_added == 0:
                    normlabels.append(norm_labels[labelindex])
            labels_added = 1
            if sensor_data == []:
                sensor_data = data_entry
            else:
                sensor_data = np.concatenate((sensor_data, data_entry), axis=1)

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
        if labels_added == 0:
            normlabels.append(norm_labels[labelindex])

    if sensor_data!=[]:
        sensor_data = np.concatenate((sensor_data, arduino_data), axis=1)
    else:
        sensor_data = arduino_data

    if full_data == []:
        full_data = sensor_data
    else:
        full_data = np.concatenate((full_data, sensor_data), axis=0)

rospy.logwarn(np.array(full_data).shape)
rospy.logwarn(np.array(normlabels).shape)
rospy.logwarn(imus_used)
rospy.logwarn(input_names)
rospy.logwarn(names)

labels = []
sensor_data = []

normalized_data = preprocessing.normalize(full_data, norm='l1', axis=0)

pickle.dump(full_data, open(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data.p", 'wb'))
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data.mat", mdict={"full_data": full_data})

pickle.dump(normalized_data, open(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data_normalized.p", 'wb'))
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_"+imus_used+"full_data_normalized.mat",
            mdict={"full_data_normalized": normalized_data})

pickle.dump(normlabels, open(fpath+"/new_bags/datasets/"+subject+"_normal_labels.p", 'wb'))
sio.savemat(fpath+"/new_bags/datasets/"+subject+"_normal_labels.mat", mdict={"norm_labels": normlabels})
