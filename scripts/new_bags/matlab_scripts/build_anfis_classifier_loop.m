function  build_anfis_classifier_loop( subject )
%BUILD_ANFIS_CLASSIFIER Summary of this function goes here
%   Detailed explanation goes here
    fullData = load(['~/full_data/',subject,'_classifierList.mat']);
    error = 'could not build classifier '
    dataFiles = fullData.fileData{1};
    labelsFile = fullData.fileData{2};
    normLabelsFile = fullData.fileData{3};
    for fileName = dataFiles'
        %try
            create_anfis_classifier( fileName{1}, labelsFile, normLabelsFile, 6)
            %create_anfis_classifier_phase( fileName{1}, labelsFile, normLabelsFile, 10)
        %catch
        %    [error, fileName{1}]
    end
end

