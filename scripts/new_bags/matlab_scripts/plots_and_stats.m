function [ output_args ] = plots_and_stats( subject )
    f = dir('~/full_data/trained_wss/');
    evaluated_classifiers = {};
    for file = f'
        file;
        if(size(strfind(file.name, ['evaluated_' subject]))~=0)
            evaluated_classifiers = [evaluated_classifiers; file.name];
        end
    end
    
    if(size(strfind(subject, 'subject1'))~=0)
        remove = 1973;
        class_labels = load('~/full_data/subject1_normal_labels.mat')
        class_labels = double(class_labels.norm_labels(1:end-remove));
        class_labels = class_labels';
        graph_title = 'Subject One';
    elseif (size(strfind(subject, 'subject2'))~=0)
        remove = 1805;
        class_labels = load('~/full_data/subject2_normal_labels.mat')
        class_labels = double(class_labels.norm_labels(1:end-remove));
        class_labels = class_labels';
        graph_title = 'Subject Two';
    elseif(size(strfind(subject, 'subject3'))~=0)
        remove = 2187;
        class_labels = load('~/full_data/subject3_normal_labels.mat')
        class_labels = double(class_labels.norm_labels(1:end-remove));
        class_labels = class_labels';
        graph_title = 'Subject Three';
    end
    graph_labels = [{'NG'}, {'SFC'},...
     {'SSW'}, {'ETS'}]';
    max_overall_mean_accuracy = -1;
    index = -1;
    i = 0;
    data = '';
    for classifier = evaluated_classifiers'
        classifier;
        workspace = load(classifier{1});
        accuracy_list = workspace.accuracy_list;
        CVO_list = workspace.CVO_list;
        CVO2_list = workspace.CVO2_list;
        final_result_list = workspace.final_result_list;
        output_list = workspace.output_list;
        total_lol_list = workspace.total_lol_list;
        average_total_accuracy = mean(accuracy_list);
        max_total_accuracy = max(accuracy_list);
        min_total_accuracy = min(accuracy_list);
        std_dev = std(accuracy_list);
        i = i+1;
        
        if(average_total_accuracy > max_overall_mean_accuracy)
            max_overall_mean_accuracy = average_total_accuracy;
            index = i;
        end
    end
    max_overall_mean_accuracy
    index  
    evaluated_classifiers{index};
    workspace = load(evaluated_classifiers{index});
    accuracy_list = workspace.accuracy_list;
    CVO_list = workspace.CVO_list;
    CVO2_list = workspace.CVO2_list;
    
    final_result_list = workspace.final_result_list;
    output_list = workspace.output_list;
    total_lol_list = workspace.total_lol_list;
    average_total_accuracy = mean(accuracy_list);
    [max_total_accuracy, max_index] = max(accuracy_list)
    [min_total_accuracy, min_index] = min(accuracy_list)    
    std_dev = std(accuracy_list);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    std_dev = std(accuracy_list);
    max_total_accuracy = max(accuracy_list);
    min_total_accuracy = min(accuracy_list);
    correctly_guessed_zeros = 0;
    zeros_list = {};
    ones_list = {};
    twos_list = {};
    threes_list = {};
    abnormals_list = {};
    correctly_guessed_ones = 0;
    correctly_guessed_twos = 0;
    correctly_guessed_threes = 0;
    correctly_guessed_abnormals = 0;
    sum_zeros = 0;
    sum_ones = 0;
    sum_twos = 0;
    sum_threes = 0;
    sum_abnormals = 0;
    for i=1:8
        l1 = class_labels(CVO_list{i}.test);
        l1 = l1(CVO2_list{i}.test);
        l2 = final_result_list(i);
        l2 = l2{1};
        correctly_guessed_zeros = correctly_guessed_zeros + ...
        (sum(l1==0 & l2==0));
        sum_zeros = sum_zeros + sum(l1==0);
        zeros_list{i} = (sum(l1==0 & l2==0))/sum(l1==0);
        
        correctly_guessed_ones = correctly_guessed_ones + ...
        (sum(l1==1 & l2==1));
        sum_ones = sum_ones + sum(l1==1);
        ones_list{i} = (sum(l1==1 & l2==1))/sum(l1==1);
        
        correctly_guessed_twos = correctly_guessed_twos + ...
        (sum(l1==2 & l2==2));
        sum_twos = sum_twos + sum(l1==2);
        twos_list{i} = (sum(l1==2 & l2==2))/sum(l1==2);
        
        correctly_guessed_threes = correctly_guessed_threes + ...
        (sum(l1==3 & l2==3));
        sum_threes = sum_threes + sum(l1==3);
        threes_list{i} = (sum(l1==3 & l2==3))/sum(l1==3);
        
        correctly_guessed_abnormals = correctly_guessed_abnormals + ...
        (sum(l1~=0 & l2~=0));
        sum_abnormals = sum_abnormals + sum(l1~=0);
        abnormals_list{i} = (sum(l1~=0 & l2~=0))/sum(l1~=0);
    end
    format long g
    overall_results = [
    [correctly_guessed_zeros, correctly_guessed_ones, correctly_guessed_twos,...
    correctly_guessed_threes, correctly_guessed_abnormals],
    [sum_zeros, sum_ones, sum_twos, sum_threes, sum_abnormals],
    [correctly_guessed_zeros/sum_zeros, correctly_guessed_ones/sum_ones,...
    correctly_guessed_threes/sum_threes, correctly_guessed_twos/sum_twos,...
    correctly_guessed_abnormals/sum_abnormals]
    ];
    zeros_list(:,:)
    avg_zeros = mean(cell2mat(zeros_list));
    std_zeros = std(cell2mat(zeros_list));
    avg_ones = mean(cell2mat(ones_list));
    std_ones = std(cell2mat(ones_list));
    avg_twos = mean(cell2mat(twos_list));
    std_twos = std(cell2mat(twos_list));
    avg_threes = mean(cell2mat(threes_list));
    std_threes = std(cell2mat(threes_list));
    avg_ab = mean(cell2mat(abnormals_list));
    std_ab = std(cell2mat(abnormals_list));
    average_total_accuracy
    std_dev
    overall_results_2 = [
    [avg_zeros, std_zeros],
    [avg_ones, std_ones],
    [avg_twos, std_twos],
    [avg_threes, std_threes],
    [avg_ab, std_ab]
    ]
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    labels = class_labels(CVO_list{max_index}.test);
    labels = labels(CVO2_list{max_index}.test);
    figure;
    x = final_result_list(max_index);
    x = x{1};
    y = labels;
    plot(x)
    hold on; 
    plot(y)
    hold off
    ax = gca;
    set(gca,'YTick', [0, 1, 2, 3], 'YTickLabel',graph_labels, 'box', 'off')
    ax.YLabel.String = 'Gait Type';
    ax.XLabel.String = 'Signal #';
    legend('Output Classification', 'Gait Type', 'Location', 'northwest');
    title(graph_title)
    print(['~/full_data/trained_wss/' subject],'-depsc')
end
