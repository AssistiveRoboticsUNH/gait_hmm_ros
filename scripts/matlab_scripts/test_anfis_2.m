function test_anfis(ws, thres, window, batch_training, batch_size, rule_thres)
    workspace = load(ws);
    load(ws);
    assignin('base', 'workspace', workspace);
    k = arg_list(13);
    name = ws;
    t_s = num2str(thres);
    t_s = [t_s(1) t_s(3:end)];
    w_s = num2str(window);
    name = [name(1:end-4) '_accu_' t_s '_' w_s '.mat' ]
    assignin('base', 'k', k);
    assignin('base', 'name', ws);
    assignin('base', 'thres', thres);
    assignin('base', 'window', window);
    assignin('base', 'batch_training', batch_training);
    assignin('base', 'batch_size', batch_size);
    assignin('base', 'input_names', workspace.input_names);
    assignin('base', 'an1', workspace.an1);
    assignin('base', 'full_data', workspace.full_data);
    assignin('base', 'full_class', workspace.full_class);
    zeroes_acc = 0.0;
    ones_acc = 0.0;
    total_acc = 0.0;
    input_names_expanded = [];
    input_names
    full_output = [];
    full_output_norm = [];
    full_output_final = [];
    full_indexes = [];
    final_class = [];
    for i_n=1:length(input_names);
        kekers = strfind(input_names(i_n), '_quat', 'ForceCellOutput', true);
        check = isempty(kekers{1});
        if(~check)
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_x')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_y')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_z')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_w')];
            continue
        end
        kekers = strfind(input_names(i_n), 'gyro', 'ForceCellOutput', true);
        check = isempty(kekers{1});
        if(~check)
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_x')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_y')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_z')];
            continue
        end
        kekers = strfind(input_names(i_n), '_accel', 'ForceCellOutput', true);
        check = isempty(kekers{1});
        if(~check)
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_x')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_y')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_z')];
            continue
        end
        kekers = strfind(input_names(i_n), '_com', 'ForceCellOutput', true);
        check = isempty(kekers{1});
        if(~check)
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_x')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_y')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_z')];
            continue
        end
        kekers = strfind(input_names(i_n), 'fsr', 'ForceCellOutput', true);
        check = isempty(kekers{1});
        if(~check)
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_bk')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_fr')];
            input_names_expanded = [input_names_expanded ; strcat(input_names(i_n),'_fl')];
            continue
        end
        input_names_expanded = [input_names_expanded ; input_names(i_n)];
    end
    assignin('base', 'input_names_expanded', input_names_expanded);
    %output_list
    for i=1 : k;
        trIdx = CVO.training(i);
        teIdx = CVO.test(i);
        teIdx2 = find(teIdx==1);
        el = size(teIdx2,1);
        
        %for e=15:el;
        %    if(mod(el, e)==0);
        %        fprintf('Block size : %d\n', e);
        %        trIdx = randblock(trIdx, e);
        %        break;
        %    end
        %end
        
        for e=15:el;
            if(mod(el, e)==0.0);
                fprintf('Block size : %d\n', e);
                %t = find(teIdx==1)
                %teIdx2 = find(teIdx==1)
                teIdx = randblock(teIdx2, e);
                %assignin('base', 'teIdx2', double(teIdx2));
                %assignin('base', 'teIdx', double(teIdx2));
                %teIdx2 == teIdx
                %fdasfsda
                break;
            end
        end
        
        tr_in = full_data(trIdx,:);
        tr_cl = full_class(trIdx,:);
        te_in = full_data(teIdx,:);
        te_cl = full_class(teIdx,:);
        final_class = [final_class ; te_cl];
        positive = tr_in(find(tr_cl==1),:);
        negative = tr_in(find(tr_cl==0),:);
        [p_inputs_n input_size] = size(positive);
        [n_inputs_n input_size] = size(negative);
        positive_means = mean(positive, 1);
        positive_std = std(positive, 0, 1);
        negative_means = mean(negative, 1);
        negative_std = std(negative, 0, 1);
        ii=1;
        teIdx = CVO.test(i);
        el = size(find(teIdx==1), 1);
        while ii <= el;
            indexes=[];
            for ww=1 :batch_size;
                if (ww<=batch_size) && (ii<=el);
                    indexes = [indexes ii];
                    ii = ii+1;
                    ii;
                end
            end
            ii;
            indexes;
            full_indexes = [full_indexes indexes];
            %indexes
            %size(te_in)
            %te_in(indexes, :)
            b = 1
            output_test=[]
            while b <= numel(indexes)
                [output,IRR,ORR,ARR] = evalfis(te_in(indexes(b),:), an1);
                output_test = [output_test ;output];
                b=b+1;
            end
            %[output_test,IRR,ORR,ARR] = evalfis(te_in(indexes,:), an1);
            output_test
            full_output = [full_output; output_test];
            test_means = mean(te_in(indexes,:), 1);
            test_std = std(te_in(indexes), 0 ,1);
            assignin('base', 'output_test', output_test);
            assignin('base', 'IRR', IRR);
            assignin('base', 'ORR', ORR);
            assignin('base', 'ARR', ARR);
            rule_prod = prod(IRR, 2);
            [garbage rules] = size(workspace.an1.rule);
            input_names_expanded;
            inputs = numel(input_names_expanded);
            workspace.an1.rule;
            for rule=1 : rules;
                triggers=[];
                trigger_idx = [];
                if rule_prod(rule)>rule_thres;
                    for input=1 : inputs;
                        if IRR(rule, input)>rule_thres;
                            triggers=[triggers ; input_names_expanded(input)];
                            trigger_idx = [trigger_idx input];
                        end
                    end
                end
                if numel(triggers)~=0;
                    fprintf('Rule %d was triggered by inputs :', rule)
                    for t=1:numel(triggers);
                        triggers(t)
                        fprintf('with value %f, mean %f and standard deviation %f\n', test_means(t), positive_means(trigger_idx(t)), positive_std(t) );
                        %pause(10.1)
                    end
                %else
                    %fprintf('Rule %d was not triggered', rule)
                end
                %pause(0.1)
                
            end
            
            max_a = max(output_test,[],1);
            min_a = min(output_test,[],1);
            [row,col] = size(output_test);
            output_test_norm = ((repmat(max_a,row,1)-output_test)./repmat(max_a-min_a,row,1));
            full_output_norm = [full_output_norm ;output_test_norm];
            output_test_final = output_test_norm;
            means = output_test_norm;
            correct_ones = 0;
            correct_zeroes = 0;
            correct_guesses = 0;
            j = 1 ;
            while j < numel(output_test_norm);
                indexes = [];
                j;
                w = 1;
                x = size(output_test_norm);
                x = x(1);
                % w
                % x
                % window
                while (w <= window) && (j <= x);
                    indexes = [indexes j];
                    w = w+1;
                    j = j+1;
                end
                indexes;
                %m = mean(output_test_norm(indexes));
                m = mean(output_test(indexes));
                means(indexes) = m;
                %if m <= thres;
                if m > 0.8;
                    output_test_final(indexes) = 1;
                else
                    output_test_final(indexes) = 0;
                end
            end
            full_output_final = [full_output_final ; output_test_final];
            %output_test_final
            %size(te_cl(indexes))
            %size(output_test_final')
            %size(full_output_final)
            %full_output_final = [full_output_final output_test_final]
            %te_cl(indexes)
            %output_test_final = output_test_final';
            % full_output_final = [full_output_final; output_test_final]
            %assignin('base', 'output_test_final', output_test_final');
            %assignin('base', 'te_cl', te_cl);
            %plot(output_test,'DisplayName','output_test');
            %hold on;plot(output_test_final,'DisplayName','output_test_final');
            %plot(te_cl,'DisplayName','te_cl');
            %hold on;
            output_test_final;
            indexes;
            for j=1 : size(output_test_norm);
                %output_test_final(j)
                full_indexes(j);
                te_cl(full_indexes(j));
                if(output_test_final(j) == 1)&&(te_cl(full_indexes(j))==1);
                    correct_ones = correct_ones + 1;
                    correct_guesses = correct_guesses + 1;
                elseif(output_test_final(j) == 0)&&(te_cl(full_indexes(j))==0);
                    correct_zeroes = correct_zeroes + 1;
                    correct_guesses = correct_guesses + 1;
                end
            end
            correct_guesses = correct_guesses';
            correct_zeroes = correct_zeroes';
            correct_ones = correct_ones';
            assignin('base', 'correct_guesses', correct_guesses);
            assignin('base', 'correct_zeroes', correct_zeroes);
            assignin('base', 'correct_ones', correct_ones);
            y = size(output_test_final);
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
            %sleep(1000000000000000000000)
            %assignin('base', 'ws', ws);
        end
    end
    total_acc/k
    ones_acc/k
    zeroes_acc/k
    assignin('base', 'total_acc', total_acc/k);
    assignin('base', 'ones_acc', ones_acc/k);
    assignin('base', 'zeroes_acc', zeroes_acc/k);
    assignin('base', 'full_output', full_output);
    assignin('base', 'full_output_norm', full_output_norm);
    assignin('base', 'full_output_final', full_output_final);
    assignin('base', 'full_indexes', full_indexes);
    assignin('base', 'final_class', final_class);
    save(name, 'workspace', 'name', 'thres', 'window', 'k', 'total_acc',...
    'ones_acc', 'zeroes_acc', 'full_output','full_output_norm',...
    'full_output_final', 'full_indexes','full_data', 'full_class','final_class')
end
