#!/bin/bash
roslaunch gait_hmm_ros bag2mat.launch prefix:=nick1
roslaunch gait_hmm_ros bag2mat.launch prefix:=nick2
roslaunch gait_hmm_ros bag2mat.launch prefix:=nick3
roslaunch gait_hmm_ros bag2mat.launch prefix:=nick4
roslaunch gait_hmm_ros bag2mat.launch prefix:=nick5
roslaunch gait_hmm_ros fsr_annotate.launch prefix:=nick1
roslaunch gait_hmm_ros fsr_annotate.launch prefix:=nick2
roslaunch gait_hmm_ros fsr_annotate.launch prefix:=nick3
roslaunch gait_hmm_ros fsr_annotate.launch prefix:=nick4
roslaunch gait_hmm_ros fsr_annotate.launch prefix:=nick5
