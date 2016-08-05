function test_anfis(ws)
    load(ws)
    k = arglist.k
    output_list
    for i=1 : k
        trIdx = CVO.training(i)
        teIdx = CVO.test(i)
        tr_in = full_data(trIdx,:);
        tr_cl = full_class(trIdx,:);
        te_in = full_data(teIdx,:);
        te_cl = full_class(teIdx,:);
        
        output = evalfis(te_in, an1);
        assignin('base', 'output_test', output_test);
        
        max_a = max(output,[],1);
        min_a = min(output,[],1);
        [row,col] = size(output);
        output_test_norm = ((repmat(max_a,row,1)-output)./repmat(max_a-min_a,row,1));
        output_final = output_test_norm;
        means = output_test_norm;
        correct_ones = 0;
        correct_zeroes = 0;
        correct_guesses = 0;
        for j=1 : size(output_test_norm)
            indexes = [];
            k = 1;
            while (k <= 10) && (j <= size(output_test_norm));
                indexes = [indexes j];
                k = k+1;
                j = j+1;
            end
            m = mean(output_test_norm(indexes));
            means(indexes) = m;
            if m >= 0.5
                output_test_final(indexes) = 1;
            else
                output_test_final(indexes) = 0;
            end
        end
        
        for j=1 : size(output_test_norm)
            if(output_test_norm(j) == 1)&&(output_test_norm(j)==1)
                correct_ones = correct_ones + 1;
                correct_guesses = correct_guesses + 1;
            elseif(output_test_norm(j) == 0)&&(output_test_norm(j)==0)
                correct_zeros = correct_zeros + 1;
                correct_guesses = correct_guesses + 1;
            end
        end
        correct_guesses
        correct_guesses/size(output_final)
        correct_zeroes
        correct_zeroes/sum(te_cl==0)
        correct_ones
        correct_ones/sum(te_cl==1)
    end
end
