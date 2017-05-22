#!/bin/bash
sleep 5
roslaunch gait_hmm_ros record.launch prefix:=$1 dur:=$2
rosnode kill /usb_cam
