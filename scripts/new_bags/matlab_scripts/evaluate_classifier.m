function [ ret_max ] = evaluate_classifier(path, ws, k, thres, window )
%EVALUATE_CLASSIFIER 
% evaluate an anfis classifier
% and save the results
%   
    wsName = [path,ws];
    % load saved workspace for the classifier
    name = [path,'evaluated_',ws];
    workspace = load(wsName);
    assignin('base', 'k', k);
    assignin('base', 'name', ws);
    assignin('base', 'thres', thres);
    assignin('base', 'window', window);
    assignin('base', 'workspace', workspace);
    zeroes_acc = 0.0;
    ones_acc = 0.0;
    total_acc = 0.0;
    imu_entries = 0;
    ir = 0;
    prox = 0;
    fsr = 0;
    ret_max = 0;
    component_mul = 0;
    % format the input according to the measurements used
    if(size(strfind(ws, '_accel_'))~=0)
        component_mul = component_mul + 3;
    end
    if(size(strfind(ws, '_gyro_'))~=0)
        component_mul = component_mul + 3;
    end
    if(size(strfind(ws, '_rll_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(ws, '_rul_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(ws, '_rf_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(ws, '_m_'))~=0)
        imu_entries = imu_entries + component_mul;
    end
    if(size(strfind(ws, '_fsr_'))~=0)
        fsr = 3;
    end
    if(size(strfind(ws, '_ir_'))~=0)
        ir = 1;
    end
    if(size(strfind(ws, '_prox_'))~=0)
        prox = 1;
    end
    
    % k-fold validation
    if strcmp(workspace.CVO.Type,'kfold')
        for i=1 : k;
            trIdx = workspace.CVO.training(i);
            teIdx = workspace.CVO.test(i);
            tr_in = workspace.full_data(trIdx,:);
            tr_cl = workspace.full_labels(trIdx,:);
            te_in = workspace.full_data(teIdx,:);
            te_cl = workspace.full_labels(teIdx,:);
            
            [output_test,IRR,ORR,ARR] = evalfis(te_in,  workspace.an1);
            
            totalORR = [];
            totalARR = [];
            totalIRR = [];
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
                [output_test_,IRR_,ORR_,ARR_] = evalfis(te_in(indexes,:),  workspace.an1); 
                totalLol(indexes)=output_test_;
                totalORR = [totalORR, ORR_];
                totalARR = [totalARR, ARR_];
                totalIRR = [totalIRR, IRR_];
            end
        
            assignin('base', 'output_test', output_test);
            assignin('base', 'IRR', IRR);
            assignin('base', 'ORR', ORR);
            assignin('base', 'ARR', ARR);
            
            assignin('base', 'IRR_', IRR_);
            assignin('base', 'ORR_', ORR_);
            assignin('base', 'ARR_', ARR_);
            
            assignin('base', 'totalLol', totalLol);
            assignin('base', 'totalORR', totalORR);
            assignin('base', 'totalARR', totalARR);
            assignin('base', 'totalIRR', totalIRR);
            
            max_a = max(output_test,[],1);
            min_a = min(output_test,[],1);
            [row,col] = size(output_test);
            output_test_norm = ((repmat(max_a,row,1)-output_test)./repmat(max_a-min_a,row,1));
            final_array = output_test;
            output_final = output_test_norm;
            means = output_test_norm;
            correct_ones = 0;
            correct_zeroes = 0;
            correct_guesses = 0;
            
            x = size(output_test_norm);
            x = x(1);
            output_test_final = output_test_norm;
            j = 1;
                    
            while j < x
                indexes = [];
                w = 1;
                while (w <= window) && (j <= x);
                    indexes = [indexes j];
                    w = w+1;
                    j = j+1;
                end
                m = mean(output_test_norm(indexes));
                means(indexes) = m;
                if m <= thres;
                    output_test_final(indexes) = 1;
                else
                    output_test_final(indexes) = 0;
                end
            end
            
            sensor_indexes = [];
            x = size(output_test);
            x = x(1);
            for j=1 : size(output_test);
                indexes = [];
                w = 1;
                while (w <= 1) && (j <= x);
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
            
            ret = (sum(te_cl==final_array))/length(te_cl)
            if (ret > ret_max)
                ret_max = ret
            end
            
            output_test_final = output_test_final';
            assignin('base', 'output_test_final', output_test_final');
            assignin('base', 'te_cl', te_cl);
            assignin('base', 'means', means);
            for j=1 : size(output_test_norm);
                if(final_array(j) == 1)&&(te_cl(j)==1);
                    correct_ones = correct_ones + 1;
                    correct_guesses = correct_guesses + 1;
                elseif(final_array(j) == 0)&&(te_cl(j)==0);
                    correct_zeroes = correct_zeroes + 1;
                    correct_guesses = correct_guesses + 1;
                end
            end
            
            arduino_components = fsr + ir + prox
            imu_entries
            input_size = arduino_components + imu_entries
            
            correct_guesses = correct_guesses';
            correct_zeroes = correct_zeroes';
            correct_ones = correct_ones';
            assignin('base', 'correct_guesses', correct_guesses);
            assignin('base', 'correct_zeroes', correct_zeroes);
            assignin('base', 'correct_ones', correct_ones);
            assignin('base', 'output_test_norm', output_test_norm);
            assignin('base', 'final_array', final_array);
            y = size(output_final);
            y = y(1);
            correct_guesses;
            correct_guesses/y;
            total_acc = total_acc + (correct_guesses/y);
            correct_zeroes;
            correct_zeroes/sum(te_cl==0);
            zeroes_acc = zeroes_acc + correct_zeroes/sum(te_cl==0);
            correct_ones;
            correct_ones/sum(te_cl==1);
            ones_acc = ones_acc + correct_ones/sum(te_cl==1);
            assignin('base', 'ws', ws);
            correct_guesses;
            correct_guesses/y;
            total_acc = total_acc + (correct_guesses/y);
            correct_zeroes;
            correct_zeroes/sum(te_cl==0);
            zeroes_acc = zeroes_acc + correct_zeroes/sum(te_cl==0);
            correct_ones;
            correct_ones/sum(te_cl==1);
            ones_acc = ones_acc + correct_ones/sum(te_cl==1);
            assignin('base', 'ws', ws);
        end
    else
        trIdx = workspace.CVO2.training;
        teIdx = workspace.CVO2.test;
        tr_in = workspace.full_data(trIdx,:);
        tr_cl = workspace.full_labels(trIdx,:);
        te_in = workspace.te_in;
        te_cl = workspace.te_cl;
        
        [output_test,IRR,ORR,ARR] = evalfis(te_in,  workspace.an1);
        
        totalORR = [];
        totalARR = [];
        totalIRR = [];
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
            [output_test_,IRR_,ORR_,ARR_] = evalfis(te_in(indexes,:),  workspace.an1); 
            totalLol(indexes)=output_test_;
            totalORR = [totalORR, ORR_];
            totalARR = [totalARR, ARR_];
            totalIRR = [totalIRR, IRR_];
        end
        
        assignin('base', 'output_test', output_test);
        assignin('base', 'IRR', IRR);
        assignin('base', 'ORR', ORR);
        assignin('base', 'ARR', ARR);
        
        assignin('base', 'IRR_', IRR_);
        assignin('base', 'ORR_', ORR_);
        assignin('base', 'ARR_', ARR_);
        
        assignin('base', 'totalLol', totalLol);
        assignin('base', 'totalORR', totalORR);
        assignin('base', 'totalARR', totalARR);
        assignin('base', 'totalIRR', totalIRR);
        
        max_a = max(output_test,[],1);
        min_a = min(output_test,[],1);
        [row,col] = size(output_test);
        output_test_norm = ((repmat(max_a,row,1)-output_test)./repmat(max_a-min_a,row,1));
        final_array = output_test;
        output_final = output_test_norm;
        means = output_test_norm;
        correct_ones = 0;
        correct_zeroes = 0;
        correct_guesses = 0;
        
        x = size(output_test_norm);
        x = x(1);
        output_test_final = output_test_norm;
        j = 1;
        
        while j < x
            indexes = [];
            w = 1;
            while (w <= window) && (j <= x);
                indexes = [indexes j];
                w = w+1;
                j = j+1;
            end
            m = mean(output_test_norm(indexes));
            means(indexes) = m;
            if m <= thres;
                output_test_final(indexes) = 1;
            else
                output_test_final(indexes) = 0;
            end
        end
        
        sensor_indexes = [];
        x = size(output_test);
        x = x(1);
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
        
        ret = (sum(te_cl==final_array))/length(te_cl);
        if (ret > ret_max)
            ret_max = ret;
        end
        
        output_test_final = output_test_final';
        assignin('base', 'output_test_final', output_test_final');
        assignin('base', 'te_cl', te_cl);
        assignin('base', 'means', means);
        for j=1 : size(output_test_norm);
            if(final_array(j) == 1)&&(te_cl(j)==1);
                correct_ones = correct_ones + 1;
                correct_guesses = correct_guesses + 1;
            elseif(final_array(j) == 0)&&(te_cl(j)==0);
                correct_zeroes = correct_zeroes + 1;
                correct_guesses = correct_guesses + 1;
            end
        end
        
        arduino_components = fsr + ir + prox;
        imu_entries;
        input_size = arduino_components + imu_entries;
        
        correct_guesses = correct_guesses';
        correct_zeroes = correct_zeroes';
        correct_ones = correct_ones';
        assignin('base', 'correct_guesses', correct_guesses);
        assignin('base', 'correct_zeroes', correct_zeroes);
        assignin('base', 'correct_ones', correct_ones);
        assignin('base', 'output_test_norm', output_test_norm);
        assignin('base', 'final_array', final_array);
        y = size(output_final);
        y = y(1);
        correct_guesses;
        correct_guesses/y;
        total_acc = total_acc + (correct_guesses/y);
        correct_zeroes;
        correct_zeroes/sum(te_cl==0);
        zeroes_acc = zeroes_acc + correct_zeroes/sum(te_cl==0);
        correct_ones;
        correct_ones/sum(te_cl==1);
        ones_acc = ones_acc + correct_ones/sum(te_cl==1);
        assignin('base', 'ws', ws);
    end
    % save classification results
    assignin('base', 'fsr', fsr);
    assignin('base', 'ir', ir);
    assignin('base', 'prox', prox);
    assignin('base', 'arduino_components', arduino_components);
    assignin('base', 'imu_entries', imu_entries);
    assignin('base', 'input_size', imu_entries+arduino_components);
    save(name, 'workspace', 'name', 'thres', 'window', 'k', 'total_acc',...
    'ones_acc', 'zeroes_acc', 'output_test', 'output_test_norm',...
    'output_test_final','output_final',...
    'final_array','te_in', 'te_cl', 'IRR','ORR', 'ARR','totalLol',...
    'IRR_', 'ORR_', 'ARR_',...
    'arduino_components', 'imu_entries', 'input_size');
    
    sum(totalLol==output_test);
    format long g;
end

