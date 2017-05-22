function [ output_args ] = create_anfis_classifier( input_file, label_file, normal_file, k )

    subject = '';
    gyro_accel = '';
    if(size(strfind(input_file, 'subject1'))~=0)
        subject = 'subject1';
        remove = 1973;
    elseif (size(strfind(input_file, 'subject2'))~=0)
        remove = 1805;
        subject = 'subject2';
    elseif(size(strfind(input_file, 'subject3'))~=0)
        remove = 2187;
        subject = 'subject3';
    end
    k = 0 ;
    assignin('base','k', k)
    workspace_file = ['~/full_data/trained_wss/',input_file]
    evaluated_name = ['~/full_data/trained_wss/evaluated_',input_file]
    input_file = ['~/full_data/',input_file];
    label_file;
    normal_file;
    full_data = load(input_file);
    full_data = full_data.data;
    
    full_data = full_data(1:end-remove, :);
    full_labels = load(label_file);
    full_labels = double(full_labels.labels(1:end-remove));
    full_labels = full_labels';
    
    normal_labels = load(normal_file);
    normal_labels = normal_labels.norm_labels(1:end-remove);
    normal_labels = normal_labels';
    binary_labels = normal_labels;
    binary_labels(binary_labels~=0) = 1;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    full_data = horzcat(full_data, full_labels);
    full_labels = double(normal_labels);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    assignin('base', 'full_data', full_data);
    assignin('base', 'full_labels', full_labels);
    assignin('base', 'normal_labels', normal_labels);
    assignin('base', 'binary_labels', binary_labels);
    
    CV02 = 0;
    val_in = 0;
    val_cl = 0;
    valIdx = 0;
    testIdxFin = 0;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    imu_entries = 0;
    ir = 0;
    prox = 0;
    fsr = 0;
    ret_max = 0;
    component_mul = 0;
    if(size(strfind(input_file, '_accel_'))~=0)
        component_mul = component_mul + 3;
    end
    if(size(strfind(input_file, '_gyro_'))~=0)
        component_mul = component_mul + 3;
    end
    if(size(strfind(input_file, '_rll_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(input_file, '_rul_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(input_file, '_rf_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(input_file, '_m_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(input_file, '_fsr_'))~=0)
        fsr = 3;
    end
    if(size(strfind(input_file, '_ir_'))~=0)
        ir = 1;
    end
    if(size(strfind(input_file, '_prox_'))~=0)
        prox = 1;
    end
    
    %%%%%%%%%%%%%%% FIS PARAMETERS %%%%%%%%%%%%%%%%%
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

    %dispOpt = ones(1,4);
    dispOpt = zeros(1,4);
    trnOpt = [100, 0.01, 0.01, 0.9, 1.1];
    %trnOpt = NaN
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    CVO_list = {};
    CVO2_list = {};
    fis_list = {};
    anfis_list = {};
    ChkFis_list = {};
    ChkErr_list = {};
    accuracy_list = [];
    error_list = {};
    step_size_list = {};
    output_list = {};
    final_result_list = {};
    total_lol_list = {};
    test_cl_list = {};
    total_ORR_list = {};
    total_IRR_lsit = {};
    total_ARR_list = {};
    total_imu_entries = 0;
    
    for i = 1:8
        %%%%%%% CREATE TRAINING PARTITION %%%%%%%%%%%%%%
        CVO = cvpartition(full_labels, 'HoldOut', 0.4);
        CVO_list{i} = CVO; 
        assignin('base', 'CVO', CVO);
        
        %err = zeros(CVO.NumTestSets, 1);
        trIdx = CVO.training;
        assignin('base', 'trIdx', trIdx);
        teIdx = CVO.test;
        assignin('base', 'teIdx', teIdx);
        
        tr_in = full_data(trIdx,:);
        tr_cl = full_labels(trIdx,:);
        
        assignin('base', 'tr_in', tr_in);
        assignin('base', 'tr_cl', tr_cl);
        
        te_in = full_data(teIdx,:);
        te_cl = full_labels(teIdx,:);
        %%%%%%%%%%%SEPARATE INTO VALIDATION AND TEST%%%%%%%%%%
        CVO2 = cvpartition(te_cl, 'HoldOut', 0.5);
        CVO2_list{i} = CVO2;
        valIdx = CVO2.training;
        testIdxFin = CVO2.test;
        
        val_in = te_in(valIdx, :);
        val_cl = te_cl(valIdx, :);
        
        te_in = te_in(testIdxFin, :);
        te_cl = te_cl(testIdxFin, :);
        
        assignin('base', 'val_in', val_in);
        assignin('base', 'val_cl', val_cl);
        %%%%%%%%%%%%% ENDS HERE %%%%%%%%%%%%%%%%%%%%%%
        
        assignin('base', 'te_in', te_in);
        assignin('base', 'te_cl', te_cl);
        
        tr_full = [tr_in tr_cl];
        te_full = [te_in te_cl];
        
        %%%%%%% SUPRESS WARNINGS %%%%%
        %warning('off','MATLAB:rankDeficientMatrix');
        warning off;
        
        %%%%%%%%% CREATE FIS %%%%%%%%%%
        disp('Creating FIS')
        gf2 = genfis2(tr_in, tr_cl, radii, xBounds);
        assignin('base', 'gf2', gf2);
        fis_list{i} = gf2;
        
        %%%%%%%% CREATE ANFIS %%%%%%%%%
        disp(['Training ANFIS #' num2str(i) ' with training set size : ' num2str(size(tr_in, 1))...
         ', validation size set : ' num2str(size(val_in, 1)) ...
         ', testing set size : ' num2str(size(te_in, 1))])
        error = 0;
        stepsize = 0;
        chkFis = 0;
        chkErr = 0;
        [an1, error, stepsize, chkFis, chkErr] = anfis([tr_in tr_cl], gf2, trnOpt, dispOpt, [val_in val_cl]);
        % an1 = anfis([tr_in tr_cl], gf2, trnOpt, dispOpt);
        
        %%%%%%%% SAVE PARAMETERS %%%%%%%%%
        anfis_list{i} = an1;
        error_list{i} = error;
        step_size_list{i} = stepsize;
        ChkFis_list{i} = chkFis;
        ChkErr_list{i} = chkErr;
        %%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        
        
        %%%%%% EVALUATE FIS %%%%%%%%%%%%%%
        
        disp('Evaluating ANFIS');
        [output_test,IRR,ORR,ARR] = evalfis(te_in, an1);
        output_list{i} = output_test;
        total_ORR = [];
        total_ARR = [];
        total_IRR = [];
        totalLol = te_cl;
        
        x = size(output_test);
        x = x(1);
        j=1;
        while j <= x;
            indexes = [];
            w = 1;
            while (w <= 1) && (j <= x);
                indexes = [indexes j];
                w = w+1;
                j = j+1;
            end
            [output_test_, IRR_, ORR_, ARR_] = evalfis(te_in(indexes,:),  an1); 
            totalLol(indexes)=output_test_;
            total_ORR = [total_ORR, ORR_];
            total_ARR = [total_ARR, ARR_];
            total_IRR = [total_IRR, IRR_];
        end
        total_ORR_list{i} = total_ORR;
        total_ARR_list{i} = total_ARR;
        total_IRR_list{i} = total_IRR;
        total_lol_list{i} = totalLol;
        
        final_array = output_test;
        x = size(output_test, 1);
        
        for j=1 : size(output_test);
            indexes = [];
            w = 1;
            while (w <= 10) && (j <= x);
                indexes = [indexes j];
                w = w+1;
                j = j+1;
            end
            m = mean(output_test(indexes));
            if(m<0.75)
                final_array(indexes) = 0;
            elseif(m<1.5)
                final_array(indexes) = 1;
            elseif(m<2.5)
                final_array(indexes) = 2;
            else
                final_array(indexes) = 3;
            end
        end
        final_result_list{i} = final_array;
        ret = (sum(te_cl==final_array))/length(te_cl);
        disp(['Accuracy : ' num2str(ret)])
        accuracy_list = [accuracy_list, ret];
        if (ret > ret_max)
            ret_max = ret;
            max_index = i;
        end
    end
    max_acc = {ret_max, max_index}
    assignin('base','max_acc', max_acc);
    assignin('base','CVO_list', CVO_list);
    assignin('base','CVO2_list', CVO2_list);
    assignin('base', 'an1', an1);
    assignin('base', 'anfis_list', anfis_list);
    assignin('base', 'fis_list', fis_list);
    assignin('base', 'error', error);
    assignin('base', 'stepsize', stepsize);
    assignin('base', 'chkFis', chkFis);
    assignin('base', 'ChkFis_list', ChkFis_list);
    assignin('base', 'chkErr', chkErr);
    assignin('base', 'ChkErr_list', ChkErr_list);
    assignin('base', 'total_ORR_list', total_ORR_list);
    assignin('base', 'total_ARR_list', total_ARR_list);
    assignin('base', 'total_IRR_list', total_IRR_list);
    assignin('base', 'total_lol_list', total_lol_list);
    assignin('base', 'accuracy_list', accuracy_list);
    assignin('base', 'output_list', output_list);
    assignin('base', 'final_result_list', final_result_list);
    assignin('base', 'ret_max', ret);
    output = evalfis(te_in, an1);
    assignin('base', 'output', output);
    
    
    save(evaluated_name,...
    'max_acc',...
    'CVO_list','CVO2_list',...
    'ChkFis_list','ChkErr_list',...
    'total_ORR_list','total_ARR_list','total_IRR_list',...
    'accuracy_list','ret_max',...
    'anfis_list','fis_list',...
    'final_result_list','output_list','total_lol_list'...
    )
    
end
