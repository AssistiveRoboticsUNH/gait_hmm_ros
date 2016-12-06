function [ output_args ] = create_anfis_classifier_phase( input_file, label_file, normal_file, k )
%CREATE_ANFIS_CLASSIFIER Summary of this function goes here
%   Detailed explanation goes here
    if(k==0)
        k=7
    end
    assignin('base','k', k)
    workspace_file = ['~/full_data/trained_wss/',input_file]
    input_file = ['~/full_data/',input_file]
    label_file
    normal_file
    full_data = load(input_file);
    full_data = full_data.data;
    
    assignin('base', 'full_data', full_data);
    full_labels = load(label_file);
    full_labels = double(full_labels.labels);
    full_labels = full_labels';
    assignin('base', 'full_labels', full_labels);
    
    normal_labels = load(normal_file);
    normal_labels = normal_labels.norm_labels;
    normal_labels = normal_labels';
    binary_labels = normal_labels;
    binary_labels(binary_labels~=0) = 1;
    
    assignin('base', 'normal_labels', normal_labels);
    assignin('base', 'binary_labels', binary_labels);
    
    CVO = cvpartition(full_labels, 'k', k);
    assignin('base', 'CVO', CVO);
    err = zeros(CVO.NumTestSets, 1);
    trIdx = CVO.training(1);
    assignin('base', 'trIdx', trIdx);
    teIdx = CVO.test(1);
    assignin('base', 'teIdx', teIdx);
    
    chkIn = full_data(CVO.training(2),:);
    chkCl = full_labels(CVO.test(2),:);
    
    assignin('base', 'chkIn', chkIn);
    assignin('base', 'chkCl', chkCl);
    
    dispOpt = ones(1,4);
    trnOpt = NaN
    
    tr_in = full_data(trIdx,:);
    tr_cl = full_labels(trIdx,:);
    
    assignin('base', 'tr_in', tr_in);
    assignin('base', 'tr_cl', tr_cl);
    
    te_in = full_data(teIdx,:);
    te_cl = full_labels(teIdx,:);
    
    assignin('base', 'te_in', te_in);
    assignin('base', 'te_cl', te_cl);
    
    tr_full = [tr_in tr_cl];
    te_full = [te_in te_cl];
    
    d = size(full_data);
    radii = ones(1,d(2)+1)*0.2;
    radii(1, end) = 1;
    assignin('base', 'radii', radii);

    xBounds = zeros(2, length(full_data(1,:))+1);
    for n = 1:length(full_data(1,:))
        xBounds(1,n) = min(full_data(:,n));
        xBounds(2,n) = max(full_data(:,n));
    end
    xBounds(1,length(full_data(1,:))+1)=0;
    xBounds(2,length(full_data(1,:))+1)=1;
    assignin('base', 'xBounds', xBounds);
    
    disp('FIS2 GEN')
    gf2 = genfis2(tr_in, tr_cl, radii, xBounds);
    assignin('base', 'gf2', gf2);

    disp('Anfis start ')
    an1 = anfis([tr_in tr_cl], gf2, trnOpt, dispOpt);
    size(chkIn)
    size(tr_in)
    assignin('base', 'an1', an1);
    
    disp('evalfis start ')
    output = evalfis(te_in, an1);
    assignin('base', 'output', output);
    
    max_a = max(output,[],1);
    min_a = min(output,[],1);
    [row,col] = size(output);
    output_norm=((repmat(max_a,row,1)-output)./repmat(max_a-min_a,row,1));
    assignin('base', 'output_norm', output_norm);
    name = [workspace_file(1:end-4), '_workspace_phase.mat']
    save(name, 'an1', 'binary_labels', 'chkCl', 'chkIn', 'CVO', 'full_data',...
    'full_labels', 'gf2', 'normal_labels', 'output', 'output_norm', ...
    'radii', 'te_cl', 'te_in', 'teIdx', 'tr_cl', 'tr_in', 'trIdx', 'xBounds', 'k')
end

