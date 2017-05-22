p = 'normal';
create_anfis_list('subject1');
create_anfis_list('subject2');
create_anfis_list('subject3');

build_anfis_classifier_loop('subject1');
build_anfis_classifier_loop('subject2');
build_anfis_classifier_loop('subject3');

gsdfgsdf
if (p=='normal')
    try 
        movefile('~/full_data/trained_wss/subject3_gyro_accel*', '~/full_data/trained_wss/subject3/GyroAccel/normal/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject3_gyro*', '~/full_data/trained_wss/subject3/GyroOnly/normal/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject2_gyro_accel*', '~/full_data/trained_wss/subject2/GyroAccel/normal/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject2_gyro*', '~/full_data/trained_wss/subject2/GyroOnly/normal/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject1_gyro_accel*', '~/full_data/trained_wss/subject1/GyroAccel/normal/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject3_gyro*', '~/full_data/trained_wss/subject3/GyroOnly/normal/')
    catch ME
        ME
    end
else
    try 
        movefile('~/full_data/trained_wss/subject3_gyro_accel/*', '~/full_data/trained_wss/subject3/GyroAccel/phase/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject3_gyro_accel/*', '~/full_data/trained_wss/subject3/GyroOnly/phase/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject2_gyro_accel/*', '~/full_data/trained_wss/subject2/GyroAccel/phase/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject2_gyro*', '~/full_data/trained_wss/subject2/GyroOnly/phase/')
    catch ME
        ME
    end

    try 
        movefile('~/full_data/trained_wss/subject1_gyro_accel/*', '~/full_data/trained_wss/subject1/GyroAccel/phase/')
    catch ME
        ME
    end
    try 
        movefile('~/full_data/trained_wss/subject3_gyro_accel/*', '~/full_data/trained_wss/subject3/GyroOnly/phase/')
    catch ME
        ME
    end
end

[retmax1, maxname1] = evaluate_classifier_loop('subject1', p)
[retmax2, maxname2] = evaluate_classifier_loop('subject2', p)
[retmax3, maxname3] = evaluate_classifier_loop('subject3', p)
