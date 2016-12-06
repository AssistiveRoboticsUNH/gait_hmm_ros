function [ ret_maxx, max_name ] = evaluate_classifier_loop( subject, phase )
%EVALUATE_CLASSIFIER_LOOP Summary of this function goes here
%   Detailed explanation goes here
    f = dir(['~/full_data/trained_wss/',subject,'/GyroOnly/',phase,'/']);
    normLabelsFile = ''; 
    labelsFile = '';
    dataFiles = {};
    workspaces = {};
    thres = 0.3;
    window = 5;
    ret_maxx = 0.0;
    max_name = '';
    for file = f'
        file.name;
        if(size(strfind(file.name, subject))~=0)&(size(strfind(file.name, 'workspace'))~=0)&(size(strfind(file.name, 'evaluated'))==0)
            workspaces = [workspaces; file.name];
        end
    end
    for ws = workspaces'
        rett = evaluate_classifier(['~/full_data/trained_wss/',subject,'/GyroOnly/',phase,'/'], ws{1}, 10, thres, window);
        if (rett > ret_maxx)
            ret_maxx = rett;
            max_name = ['~/full_data/trained_wss/',subject,'/GyroOnly/',phase,'/', ws{1}];
        end
    end
    
    f = dir(['~/full_data/trained_wss/',subject,'/GyroAccel/',phase,'/']);
    normLabelsFile = ''; 
    labelsFile = '';
    dataFiles = {};
    workspaces = {};
    thres = 0.3;
    window = 5;
    for file = f'
        file.name;
        if(size(strfind(file.name, subject))~=0)&(size(strfind(file.name, 'workspace'))~=0)&(size(strfind(file.name, 'evaluated'))==0)
            workspaces = [workspaces; file.name];
        end
    end
    for ws = workspaces'
        rett = evaluate_classifier(['~/full_data/trained_wss/',subject,'/GyroAccel/',phase,'/'], ws{1}, 10, thres, window);
        if (rett > ret_maxx)
            ret_maxx = rett;
            max_name = ['~/full_data/trained_wss/',subject,'/GyroAccel/',phase,'/', ws{1}];
        end
    end
    
    ret_maxx
    max_name
    
    %~/full_data/trained_wss/subject3/GyroAccel/normal/subject3_gyro_accel_fsr_prox_btr_bte_rf_rul_m_full_data_normalized_workspace.mat
end

