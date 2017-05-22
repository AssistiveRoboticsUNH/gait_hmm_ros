# Gait Abnormality Detection And Classification
Receives input from IMUs and other devices and uses an ANFIS to classify
the type of gait of the user (normal gait, excessive trunk sway, small step width, low foot clearance). Requires Matlab's Fuzzy Logic Toolbox, the 3Space IMU
python API, numpy, and scipy. Tested in ROS Indigo

Sample bag files are located in scripts/new_bags/subject[number]_[trial].bag

##Launch files
* **record.sh**: waits 5 seconds and the starts recording available IMU frames
    <pre><code>sh record.sh [filename] [duration-minutes]</code></pre>
* **batch_create_combos_x.sh**: create different datasets using subsets of the available
measurements
* **create_single_classifier_x.sh**: create different classifiers using subsets of the available
measurements
* **align.launch**: used to align mocap files with data from rosbags
    <pre><code>roslaunch align.launch prefix:=[datafile] mocap:=[mocap_file]</code></pre>
* **bag2mat.launch**: used to create new matfiles from rosbags
    <pre><code>roslaunch bag2mat.launch param_file:=[param file] prefix:=[file name]</code></pre>
    param files contain the topic names for the different imus as "upper_leg_topic lower_leg_topic foot_topic"
* **auto_annotate.launch**: annotates a matfile using a given mocap file
    <pre><code>roslaunch auto_annotate.launch prefix:=[data file] prefix:=[mocap file]</code></pre>
* **create_data.launch**: creates training files using subsets of the available sensor data, edit the launch file
   to change, 1 means uses, 0 means don't use. Creates normalized and non-normalized datasets and prints out their results
   in /new_bags. Data is saved as .mat files or pickles. Also save are the label for each reading, and
   trunk sway, step length and width for mocap data.
   
   A complete data file has the following format:
   
   [upper_leg_quaternion_x][upper_leg_quaternion_y][upper_leg_quaternion_z][upper_leg_quaternion_w][upper_leg_accelerometer_x]
   [upper_leg_accelerometer_y][upper_leg_accelerometer_z][upper_leg_gyroscope_x][upper_leg_gyroscope_y][upper_leg_gyroscope_z]
   [upper_leg_magnetometer_x][upper_leg_magnetometer_y][upper_leg_magnetometer_z]
   [lower_leg_quaternion_x][lower_leg_quaternion_y][lower_leg_quaternion_z][lower_leg_quaternion_w][lower_leg_accelerometer_x]
   [lower_leg_accelerometer_y][lower_leg_accelerometer_z][lower_leg_gyroscope_x][lower_leg_gyroscope_y][lower_leg_gyroscope_z]
   [lower_leg_magnetometer_x][lower_leg_magnetometer_y][lower_leg_magnetometer_z]
   [foot_quaternion_x][foot_quaternion_y][foot_quaternion_z][foot_quaternion_w][foot_accelerometer_x]
   [foot_accelerometer_y][foot_accelerometer_z][foot_gyroscope_x][foot_gyroscope_y][foot_gyroscope_z]
   [foot_magnetometer_x][foot_magnetometer_y][foot_magnetometer_z]
   [FSR reading][IR reading][Proximity Reading]
##ROS Scripts
* **align_mocap.py**: Used to align mocap data and rosbag recordings, use with align.launch
* **arduino_listener.py**: Used to read arduino data and republish it as a ROS message
* **auto_annotate.py**: Annotates a matfile using a mocap output file (see auto_annotate.launch)
* **fsr_annotate_2.py**: annotates data using just the FSR input
* **create_data_combos.py**: creates matfiles using subset of the available measurements (see create_data.launch)
##Matlab Scripts
* **bigOlClassifierScript2**: creates and evaluates all possible classifiers
* **create_anfis_list**: reads available files in ~/full_data and creates a list of classifiers to test
* **build_anfis_classifier_loop.m**: for every classifier in the list created with create_anfis_list, build and evaluate the
 classifier
* **evaluate_anfis_classifier_loop.m**: just evaluates the classifier and saves the results
* **create_and_evaluate_classifier.m**: creates a classifier based on a given workspace, evaluates the classifier and saves the results
* **create_anfis_classifier.m**: splits data into test and training data, builds a classifier and saves the workspace
* **plots_and_stats.m**: loads a built classifier, evaluates it, and creates a graph of its performance 
###Unused/Deprecated
HMM classifiers, can be used for reference
* **create_single_classifier.py**
* **create_distributed_classifier.py**
* **dis_class_2.py**
* **distributed_classifier_2.py**
* **test_classifiers.py**
* **test_classifiers.distributed.py**
* **create_anfis_classifier_phase.m**
* **create_anfis_classifier_normal.m**
###Random
* **fsr_annotate.py: see fsr_annotate_2.py**
