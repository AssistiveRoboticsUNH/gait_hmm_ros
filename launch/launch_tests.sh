#!/bin/bash
roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec
##########################################################################################################################################################################
roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=0 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec
##########################################################################################################################################################################
roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec rll:=r_lower_arm_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec 
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec
##########################################################################################################################################################################

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=0 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=0 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=0 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=0 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=0 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=0 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec

roslaunch gait_hmm_ros launch1.launch prefix:=andreas1 batch_train:=1 batch_test:=1 use_quat:=1 use_gyro:=1 use_accel:=1 use_com:=1 use_ir:=1 use_prox:=1 use_fsr:=1 \
rf:=r_upper_arm_data_vec m:=r_hand_data_vec rll:=r_lower_arm_data_vec rul:=l_hand_data_vec




