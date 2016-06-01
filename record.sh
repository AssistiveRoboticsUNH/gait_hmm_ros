#!/bin/bash
sleep 15
rosbag record -O $1 -q --duration=$2m --regex /l_hand_data_vec /r_hand_data_vec /l_upper_arm_data_vec /usb_camera_info /usb_cam/image_raw 
