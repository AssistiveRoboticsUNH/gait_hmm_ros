#!/usr/bin/env bash
roscore
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject1 _datafile:=gyro_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject1 _datafile:=gyro_btr_bte_rf_rll
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject1 _datafile:=gyro_btr_bte_rf_rul
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject1 _datafile:=gyro_btr_bte_rf_rll_rul_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject1 _datafile:=gyro_btr_bte_rf_rll_rul_m_


rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject2 _datafile:=gyro_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject2 _datafile:=gyro_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject2 _datafile:=gyro_btr_bte_rf_rul_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject2 _datafile:=gyro_btr_bte_rf_rll_rul_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject2 _datafile:=gyro_btr_bte_rf_rll_rul_m_


rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject3 _datafile:=gyro_btr_bte_rf_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject3 _datafile:=gyro_btr_bte_rf_rll_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject3 _datafile:=gyro_btr_bte_rf_rul_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject3 _datafile:=gyro_btr_bte_rf_rll_rul_
rosrun gait_hmm_ros create_single_classifier.py _folds:=10 _norm:=1 _prefix:=subject3 _datafile:=gyro_btr_bte_rf_rll_rul_m_




