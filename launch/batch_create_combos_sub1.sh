#!/bin/bash
rosparam set /subject "subject1"
rosparam set /normlabels "[1, 0, 0 ,0, 0]"
rosparam set /filenames "['new_bags/subject1_1', 'new_bags/subject1_2', 'new_bags/subject1_3',
 'new_bags/subject1_4', 'new_bags/subject1_5']"
########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=0 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=0 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=0 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1
#########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=0 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0
#########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec
##########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

##########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec
##########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec rll:=l_lower_leg_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec

roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=chest_data_vec m:=r_lower_arm_data_vec rll:=l_lower_leg_data_vec rul:=r_upper_arm_data_vec
##########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=0 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=0 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=0 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1
##########################################################################################################################################################################
roslaunch gait_hmm_ros create_data.launch prefix:=new_bags/ batch_train:=1 batch_test:=1 use_quat:=0 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0



