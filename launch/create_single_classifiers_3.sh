#!/usr/bin/env bash
roscore
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_prox_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_ir_prox_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_com_fsr_ir_prox_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_prox_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_ir_prox_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_com_fsr_ir_prox_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_btr_bte_rf_m_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_btr_bte_rf_m_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_btr_bte_rf_m_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_btr_bte_rf_m_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_prox_btr_bte_rf_m_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_fsr_ir_prox_btr_bte_rf_m_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=$1 _datafile:=quat_gyro_accel_com_fsr_ir_prox_btr_bte_rf_m_
