#!/usr/bin/env bash
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject1_1 _matfile:=new_bags/subject_one/subject01_normal
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject1_2 _matfile:=new_bags/subject_one/subject01_narrow
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject1_3 _matfile:=new_bags/subject_one/subject01_sway
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject1_4 _matfile:=new_bags/subject_one/subject01_drag
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject1_5 _matfile:=new_bags/subject_one/subject01_combine
###############################################################################################
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject2_1 _matfile:=new_bags/subject_two/subejct02_normal
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject2_3 _matfile:=new_bags/subject_two/subejct02_narrow
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject2_4 _matfile:=new_bags/subject_two/subejct02_sway
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject2_5 _matfile:=new_bags/subject_two/subejct02_drag
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject2_6 _matfile:=new_bags/subject_two/subejct02_combine
###############################################################################################
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject3_1 _matfile:=new_bags/subject_three/subject03_normal
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject3_3 _matfile:=new_bags/subject_three/subject03_narrow
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject3_4 _matfile:=new_bags/subject_three/subject03_sway
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject3_5 _matfile:=new_bags/subject_three/subject03_drag
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject3_6 _matfile:=new_bags/subject_three/subject03_combine