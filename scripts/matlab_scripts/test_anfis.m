function test_anfis(ws, thres, window)
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
    zeroes_acc = 0.0;
    ones_acc = 0.0;
    total_acc = 0.0;
    %output_list
    for i=1 : k;
        trIdx = CVO.training(i);
        teIdx = CVO.test(i);
        tr_in = full_data(trIdx,:);
        tr_cl = full_class(trIdx,:);
        te_in = full_data(teIdx,:);
        te_cl = full_class(teIdx,:);
        
        [output_test,IRR,ORR,ARR] = evalfis(te_in, an1);
        assignin('base', 'output_test', output_test);
        assignin('base', 'IRR', IRR);
        assignin('base', 'ORR', ORR);
        assignin('base', 'ARR', ARR);
        
        max_a = max(output_test,[],1);
        min_a = min(output_test,[],1);
        [row,col] = size(output_test);
        output_test_norm = ((repmat(max_a,row,1)-output_test)./repmat(max_a-min_a,row,1));
        output_final = output_test_norm;
        means = output_test_norm;
        correct_ones = 0;
        correct_zeroes = 0;
        correct_guesses = 0;
        for j=1 : size(output_test_norm);
            indexes = [];
            w = 1;
            x = size(output_test_norm);
            x = x(1);
            while (w <= window) && (j <= x);
                indexes = [indexes j];
                w = w+1;
                j = j+1;
               
            end
            w = 0;
            m = mean(output_test_norm(indexes));
            means(indexes) = m;
            if m <= thres;
                output_test_final(indexes) = 1;
            else
                output_test_final(indexes) = 0;
            end
        end
        output_test_final = output_test_final';
        assignin('base', 'output_test_final', output_test_final');
        assignin('base', 'te_cl', te_cl);
        %plot(output_test,'DisplayName','output_test');
        %hold on;plot(output_test_final,'DisplayName','output_test_final');
        %plot(te_cl,'DisplayName','te_cl');
        %hold on;
       
        for j=1 : size(output_test_norm);
            if(output_test_final(j) == 1)&&(te_cl(j)==1);
                correct_ones = correct_ones + 1;
                correct_guesses = correct_guesses + 1;
            elseif(output_test_final(j) == 0)&&(te_cl(j)==0);
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
        %sleep(1000000000000000000000)
        assignin('base', 'ws', ws);
    end
    total_acc/k
    ones_acc/k
    zeroes_acc/k
    assignin('base', 'total_acc', total_acc/k)
    assignin('base', 'ones_acc', ones_acc/k)
    assignin('base', 'zeroes_acc', zeroes_acc/k)
    save(name, 'workspace', 'name', 'thres', 'window', 'k', 'total_acc', 'ones_acc', 'zeroes_acc')
end
