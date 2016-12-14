# gait_hmm_ros

ROS node that uses hidden markov models to classify a human's gait phase as swing or stance based on IMU data,
foot pressure sensors, infrared and proximity data requires ROS indigo and the [pomegranate](https://github.com/jmschrei/pomegranate) library. 
Included are the data for 3 subjects, with 5 intervals per subject where:
- Interval 1(and 2 for subject1 (not used)): normal walking
- Interval 2: low foot clearance 
- Interval 3: small step width
- Interval 4: excessive trunk sway
- Interval 5: all of the previous combined in a random manner

(Code not documented is deprecated/not used)

#Nodes
##Record data
~~~~
./launch/record.sh \<output_bagfile_name\> \<duration_in_minutes\>
~~~~

## Convert rosbags to useable form saving data, normalized data and timestamps in .matfiles:
Run:

For Single subject:
~~~~
  roslaunch bag2mat.launch prefix:=\<path_to_folder/subject_name_recordingnumber\> file=/<path_to_parameter_file/>
~~~~
The parameter file contains the topics for each imu, see /scripts/new_bags/sub1.yaml

For all subejcts:
~~~~
  ./launch/bag2matnewbags.sh
~~~~
This will create a number of .mat files for each input file containing each component recorded.


## Annotation:
To annotate the data file with mocap data is required in a format similar to the files found in 
/scripts/\<subject_number\>.zip, that are in the follwoing format:

COMmovement: X-anterior-posterior trunk sway; Y-medio-lateral trunk sway.

Annotate a single subject:
~~~~
rosrun gait_hmm_ros auto_annotate.py _prefix:=new_bags/subject1_1 _matfile:=new_bags/subject_one/subject01_normal
~~~~

Annotate every subject
~~~~
./launch/annotatenewbags.sh
~~~~
This will create a file named like your input file with the addition of "_labels" in the end. It will contain the gait phase
label for every timestamp created in the previous cript.

## Data set creation:
Create different sets of data containing or excluding the sensors you want to use, based on /scripts/new_bags/\<subject\>_full_data.mat created 
with the previous scripts.
~~~~
./batch_create_combos_\<sub1,sub2,sub3,gyro\>
~~~~
Uses the /launch/create_data.launch script which accepts the following parameters:
- batch_train: 0/1 whether to train classifier in batches or with single inputs
- batch_test: 0/1 whether to test classifier in batches or with single inputs
- use_quat: 0/1 whether to use the quaternion data when training the classifier
- use_gyro: 0/1 whether to use the gyroscope data when training the classifier
- use_accel: 0/1 whether to use the accelerometer data when training the classifier
- use_com: 0/1 whether to use the compass data when training the classifier
- use_ir: 0/1 whether to use the IR data when training the classifier
- use_prox: 0/1 whether to use the proximity data when training the classifier
- use_fsr: 0/1 whether to use the FSR data when training the classifier
- rf: topic for foot IMU, empty to not use
- rl: topic for lower leg IMU, empty to not use
- rul: topic for upper leg IMU, empty to not use
- m: topic for lower back IMU, empty to not use

##Train classifiers:
Train Single Classifier
~~~~
rosrun gait_hmm_ros create_single_classifier.py _folds:=\<number of training folds\> _norm:=\<1 or 0, use normalized data or not\>
_datafile:=\<first component of datafile to use se /launch/create_single_classifiers_1.sh for the format\>
~~~~

Train Multpile Classifiers:
~~~~
./launch/create_single_classifiers_(1-4).sh
~~~~
The classifiers will be saved as pickled python objects in /scripts/trained_classifiers/
