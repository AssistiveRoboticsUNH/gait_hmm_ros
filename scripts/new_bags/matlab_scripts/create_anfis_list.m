function [ output_args ] = create_anfis_loop( subject )
%CREATE_ANFIS_LOOP Summary of this function goes here
%   Detailed explanation goes here
    f = dir('~/full_data/')
    normLabelsFile = ''; 
    labelsFile = '';
    dataFiles = {};
    for file = f'
        if(size(strfind(file.name, subject))~=0)&(size(strfind(file.name, '_let'))==0)
            if(size(strfind(file.name, 'full_data_normalized'))~=0)...
            &(size(strfind(file.name, '.p'))==0)&(size(strfind(file.name, 'btr'))~=0)&(size(strfind(file.name, 'workspace'))==0)...
            &(size(strfind(file.name, 'quat'))==0)&(size(strfind(file.name, 'accel'))==0)&(size(strfind(file.name, 'gyro'))~=0)
                dataFiles = [dataFiles ;file.name]
                continue;
            end
            if((size(strfind(file.name, 'labels'))~=0)&(size(strfind(file.name, '_normal_'))~=0)&(size(strfind(file.name, '.p'))==0))
                normLabelsFile = ['~/full_data/',file.name]
                continue;
            end
            if((size(strfind(file.name, 'labels'))~=0)&(size(strfind(file.name, '_norm'))==0)&(size(strfind(file.name, '.p'))==0))
                labelsFile = ['~/full_data/',file.name]
                continue;
            end
            
        end
    end
    
    for file = f'
        if(size(strfind(file.name, subject))~=0)&(size(strfind(file.name, '_let'))==0)
            if(size(strfind(file.name, 'full_data_normalized'))~=0)...
            &(size(strfind(file.name, '.p'))==0)&(size(strfind(file.name, 'btr'))~=0)&(size(strfind(file.name, 'workspace'))==0)...
            &(size(strfind(file.name, 'quat'))==0)&(size(strfind(file.name, 'accel'))~=0)&(size(strfind(file.name, 'gyro'))~=0)
                dataFiles = [dataFiles ;file.name]
                continue;
            end
            if((size(strfind(file.name, 'labels'))~=0)&(size(strfind(file.name, '_normal_'))~=0)&(size(strfind(file.name, '.p'))==0))
                normLabelsFile = ['~/full_data/',file.name]
                continue;
            end
            if((size(strfind(file.name, 'labels'))~=0)&(size(strfind(file.name, '_norm'))==0)&(size(strfind(file.name, '.p'))==0))
                labelsFile = ['~/full_data/',file.name]
                continue;
            end
            
        end
    end
    
    
    classifierList = ['~/full_data/',subject,'_classifierList.mat'];
    %for fileName = dataFiles 
    %    create_anfis_classifier( fileName, labelsFile, normalLabelsFile, 10 )
    %end
    fileData = {3}
    dataFiles
    labelsFile
    normLabelsFile
    fileData{1} = dataFiles;
    fileData{2} = labelsFile;
    fileData{3} = normLabelsFile;
    fileData{3};
    save(['~/full_data/',subject,'_classifierList.mat'], 'fileData')
end

