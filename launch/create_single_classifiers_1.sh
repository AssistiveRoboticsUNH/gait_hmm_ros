#!/usr/bin/env bash
roscore
echo $2
FILE="/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/new_bags/logs/$2.txt"
echo $FILE
#touch  FILE
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=fsr_bte_
#2>&1 | tee -a $FILE
#exit

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=fsr_prox_bte_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=fsr_ir_prox_bte_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=gyro_bte_rf

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_prox_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_ir_prox_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_com_fsr_ir_prox_bte_rf_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_bte_rf_rll_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_bte_rf_rll_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_bte_rf_rll_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_bte_rf_rll_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_prox_bte_rf_rll_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_ir_prox_bte_rf_rll_

rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_com_fsr_ir_prox_bte_rf_rll_
exit
