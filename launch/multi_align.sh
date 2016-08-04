#!/bin/bash
roslaunch gait_hmm_ros align.launch prefix:=nick1 leg:=right matfile:=sub1/subj1_walk_1.mat
roslaunch gait_hmm_ros align.launch prefix:=nick2 leg:=right matfile:=sub1/subj1_walk_2.mat
roslaunch gait_hmm_ros align.launch prefix:=nick3 leg:=right matfile:=sub1/subj1_walk_3.mat
roslaunch gait_hmm_ros align.launch prefix:=nick4 leg:=right matfile:=sub1/subj1_abnormal_1.mat
roslaunch gait_hmm_ros align.launch prefix:=nick5 leg:=right matfile:=sub1/subj1_abnormal_2.mat
roslaunch gait_hmm_ros align.launch prefix:=andreas1 leg:=right matfile:=sub2/subj2_walk_1.mat
roslaunch gait_hmm_ros align.launch prefix:=andreas2 leg:=right matfile:=sub2/subj2_walk_2.mat
roslaunch gait_hmm_ros align.launch prefix:=andreas3 leg:=right matfile:=sub2/subj2_walk_3.mat
roslaunch gait_hmm_ros align.launch prefix:=andreas4 leg:=right matfile:=sub2/subj2_abnormal_1.mat
roslaunch gait_hmm_ros align.launch prefix:=andreas5 leg:=right matfile:=sub2/subj2_abnormal_2.mat