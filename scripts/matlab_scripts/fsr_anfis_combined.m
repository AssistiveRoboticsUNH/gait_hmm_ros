function anfisfunction(use_rf, use_rll, use_rul, use_m, use_quat, use_gyro, use_accel, ...
use_com, use_ir, use_prox, use_fsr, name, gran, k, mocap)
    sensor_data_tr = [];
    sensor_data_te = [];
    rf_tr = [];
    rf_te = [];
    rll_tr = [];
    rll_te = [];
    rul_tr = [];
    rul_te = [];
    m_tr = [];
    m_te = [];
    arduino_tr = [];
    arduino_te = [];
    arg_list = [use_rf, use_rll, use_rul, use_m, use_quat, use_gyro, use_accel, ...
    use_com, use_ir, use_prox, use_fsr, gran, k, mocap]
    name = [name '.mat']
    assignin('base', 'arg_list', arg_list);
    
    if ispc
        home = [getenv('HOMEDRIVE') getenv('HOMEPATH')];
    else
        home = getenv('HOME');
    end
    assignin('base', 'home', home);
    input_names = {}
    
    if use_rf == 1
        a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_rf.mat');
        a = a.rf;
        b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_rf.mat');
        b = b.rf;
        c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_rf.mat');
        c = c.rf;
        d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_rf.mat');
        d = d.rf;
        e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_rf.mat');
        e = e.rf;
        x = vertcat(a, b, c);
        
        rf_tr = [];
        %use quaternion
         if use_quat == 1
            rf_tr = [rf_tr x(:,1:4)];
            input_names{end+1}='rf_quat';
        end
        %use gyro
        if use_gyro == 1
            rf_tr = [rf_tr x(:,5:7)];
            input_names{end+1}='rf_gyro';
        end
        %use accel
        if use_accel == 1
            rf_tr = [rf_tr x(:,8:10)];
            input_names{end+1}='rf_accel';
        end
        %use comp
        if use_com == 1
            rf_tr = [rf_tr x(:,11:13)];
            input_names{end+1}='rf_com';
        end
        
        x = vertcat(d, e);
        %x = e;
        x = x(:,1:end-2);
        rf_te = [];
        %use quaternion
        if use_quat == 1
            rf_te = [rf_te x(:,1:4)];
        end
        %use gyro
        if use_gyro == 1
            rf_te = [rf_te x(:,5:7)];
        end
        %use accel
        if use_accel == 1
            rf_te = [rf_te x(:,8:10)];
        end
        %use comp
        if use_com == 1
            rf_te = [rf_te x(:,11:13)];
        end
        
        sensor_data_tr = horzcat(sensor_data_tr, rf_tr);
        sensor_data_te = horzcat(sensor_data_te, rf_te);
        
        size(sensor_data_tr);
        size(sensor_data_te);
        
        assignin('base', 'rf_tr', rf_tr);
        assignin('base', 'rf_te', rf_te);
    end
    
    if use_rll == 1
        a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_rll.mat');
        a = a.rll;
        b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_rll.mat');
        b = b.rll;
        c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_rll.mat');
        c = c.rll;
        d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_rll.mat');
        d = d.rll;
        e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_rll.mat');
        e = e.rll;
        x = vertcat(a, b, c);
        x = x(:,1:end-2);
        rll_tr = [];
        %use quaternion
        if use_quat == 1
            rll_tr = [rll_tr x(:,1:4)];
            input_names{end+1}='rll_quat';
        end
        %use gyro
        if use_gyro == 1
            rll_tr = [rll_tr x(:,5:7)];
            input_names{end+1}='rll_gyro';
        end
        %use accel
        if use_accel == 1
            rll_tr = [rll_tr x(:,8:10)];
            input_names{end+1}='rll_accel';
        end
        %use comp
        if use_com == 1
            rll_tr = [rll_tr x(:,11:13)];
            input_names{end+1}='rll_com';
        end

        x = vertcat(d, e);
        %x = e;
        x = x(:,1:end-2);
        rll_te = [];
        %use quaternion
        if use_quat == 1
            rll_te = [rll_te x(:,1:4)];
        end
        %use gyro
        if use_gyro == 1
            rll_te = [rll_te x(:,5:7)];
        end
        %use accel
        if use_accel == 1
            rll_te = [rll_te x(:,8:10)];
        end
        %use comp
        if use_com == 1
            rll_te = [rll_te x(:,11:13)];
        end
        
        sensor_data_tr = horzcat(sensor_data_tr, rll_tr);
        sensor_data_te = horzcat(sensor_data_te, rll_te);
        
        size(sensor_data_tr)
        size(sensor_data_te)
        
        assignin('base', 'rll_tr', rll_tr);
        assignin('base', 'rll_te', rll_te);
    end
    
    if use_rul == 1
        a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_rul.mat');
        a = a.rul;
        b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_rul.mat');
        b = b.rul;
        c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_rul.mat');
        c = c.rul;
        d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_rul.mat');
        d = d.rul;
        e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_rul.mat');
        e = e.rul;
        x = vertcat(a, b, c);
        x = x(:,1:end-2);
        rul_tr = [];
        %use quaternion
        if use_quat == 1
            rul_tr = [rul_tr x(:,1:4)];
            input_names{end+1}='rul_quat';
        end
        %use gyro
        if use_gyro == 1
            rul_tr = [rul_tr x(:,5:7)];
            input_names{end+1}='rul_gyro';
        end
        %use accel
        if use_accel == 1
            rul_tr = [rul_tr x(:,8:10)];
            input_names{end+1}='rul_accel';
        end
        %use comp
        if use_com == 1
            rul_tr = [rul_tr x(:,11:13)];
            input_names{end+1}='rul_com';
        end

        x = vertcat(d, e);
        %x = e;
        x = x(:,1:end-2);
        rul_te = [];
        %use quaternion
        if use_quat == 1
            rul_te = [rul_te x(:,1:4)];
        end
        %use gyro
        if use_gyro == 1
            rul_te = [rul_te x(:,5:7)];
        end
        %use accel
        if use_accel == 1
            rul_te = [rul_te x(:,8:10)];
        end
        %use comp
        if use_com == 1
            rul_te = [rul_te x(:,11:13)];
        end
        
        sensor_data_tr = horzcat(sensor_data_tr, rul_tr);
        sensor_data_te = horzcat(sensor_data_te, rul_te);
        
        assignin('base', 'rul_tr', rul_tr);
        assignin('base', 'rul_te', rul_te);
    end
    
    if use_m == 1
        a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_m.mat');
        a = a.m;
        b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_m.mat');
        b = b.m;
        c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_m.mat');
        c = c.m;
        d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_m.mat');
        d = d.m;
        e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_m.mat');
        e = e.m;
        x = vertcat(a, b, c);
        x = x(:,1:end-2);
        m_tr = [];
        %use quaternion
        if use_quat == 1
            m_tr = [m_tr x(:,1:4)];
            input_names{end+1}='m_quat'
        end
        %use gyro
        if use_gyro == 1
            m_tr = [m_tr x(:,5:7)];
            input_names{end+1}='m_gyro'
        end
        %use accel
        if use_accel == 1
            m_tr = [m_tr x(:,8:10)];
            input_names{end+1}='m_accel'
        end
        %use comp
        if use_com == 1
            m_tr = [m_tr x(:,11:13)];
            input_names{end+1}='m_com'
        end

        x = vertcat(d, e);
        %x = e;
        x = x(:,1:end-2);
        m_te = [];
        %use quaternion
        if use_quat == 1
            m_te = [m_te x(:,1:4)];
        end
        %use gyro
        if use_gyro == 1
            m_te = [m_te x(:,5:7)];
        end
        %use accel
        if use_accel == 1
            m_te = [m_te x(:,8:10)];
        end
        %use comp
        if use_com == 1
            m_te = [m_te x(:,11:13)];
        end
        
        sensor_data_tr = horzcat(sensor_data_tr, m_tr);
        sensor_data_te = horzcat(sensor_data_te, m_te);
        
        size(sensor_data_tr)
        size(sensor_data_te)
        
        assignin('base', 'm_tr', m_tr);
        assignin('base', 'm_te', m_te);
        
    end
    
    a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_arduino.mat');
    a = a.arduino;
    b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_arduino.mat');
    b = b.arduino;
    c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_arduino.mat');
    c = c.arduino;
    d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_arduino.mat');
    d = d.arduino;
    e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_arduino.mat');
    e = e.arduino;
    x = vertcat(a, b, c);
    x = x(:,4:end);
    arduino_tr = [];
    % use fsrs
    if use_fsr == 1
        arduino_tr = [arduino_tr x(:, 1:3)];
        input_names{end+1}='fsr';
    end
    % use ir
    if use_ir == 1
        arduino_tr = [arduino_tr x(:, 4)];
        input_names{end+1}='ir';
    end
    %use prox
    if use_prox == 1
        arduino_tr = [arduino_tr x(:, 5)];
        input_names{end+1}='prox';
    end

    x = vertcat(d, e);
    %x = e;
    x = x(:,4:end);
    arduino_te = [];
    % use fsrs
    if use_fsr == 1
        arduino_te = [arduino_te x(:, 1:3)];
    end
    % use ir
    if use_ir == 1
        arduino_te = [arduino_te x(:, 4)];
    end
    %use prox
    if use_prox ==1
        arduino_te = [arduino_te x(:, 5)];
    end

    assignin('base', 'arduino_tr', arduino_tr);
    assignin('base', 'arduino_te', arduino_te);
        
    sensor_data_tr = horzcat(sensor_data_tr, arduino_tr);
    sensor_data_te = horzcat(sensor_data_te, arduino_te);
    
    if mocap == 1
        a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_labels_mocap_annotated.mat');
        a = a.labels;
        b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_labels_mocap_annotated.mat');
        b = b.labels;
        c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_labels_mocap_annotated.mat');
        c = c.labels;
        d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_labels_mocap_annotated.mat');
        d = d.labels;
        e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_labels_mocap_annotated.mat');
        e = e.labels;
        labels_tr = horzcat(a, b, c);
        labels_te = horzcat(d, e);
    else
        a = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas1_labels_annotated.mat');
        a = a.labels;
        b = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas2_labels_annotated.mat');
        b = b.labels;
        c = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas3_labels_annotated.mat');
        c = c.labels;
        d = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas4_labels_annotated.mat');
        d = d.labels;
        e = load('/home/lydakis-local/ros_ws/src/gait_hmm_ros/scripts/andreas5_labels_annotated.mat');
        e = e.labels;
        labels_tr = horzcat(a, b, c);
        labels_te = horzcat(d, e);
    end    
    
    %labels_te = e;

    clear a
    clear b
    clear c
    clear d
    clear e
    clear x
    
    size(sensor_data_tr);
    size(sensor_data_te);
    
    sensor_data_tr = horzcat(sensor_data_tr, double(labels_tr)');
    sensor_data_te = horzcat(sensor_data_te, double(labels_te)');
    
    size(sensor_data_tr);
    size(sensor_data_te);
    
    
    assignin('base', 'labels_tr', labels_tr);
    assignin('base', 'labels_te', labels_te);
    
    full_data = vertcat(sensor_data_tr, sensor_data_te);
    full_labels = vertcat(labels_tr', labels_te');
    
    if gran ~= 0
        full_data = full_data(1:gran:end,:)
        full_labels = full_labels(1:gran:end,:)
    end
    
    max_a = max(full_data,[],1);
    min_a = min(full_data,[],1);
    [row,col] = size(full_data);
    full_data=((repmat(max_a,row,1)-full_data)./repmat(max_a-min_a,row,1));
    
    assignin('base', 'full_data', full_data);
    assignin('base', 'full_labels', full_labels);


    d = size(sensor_data_tr);
    tr_class = ones(d(1),1);
    size(tr_class)
    assignin('base', 'tr_class', tr_class);
    
    d = size(sensor_data_te);
    te_class = zeros(d(1),1);
    size(te_class)
    assignin('base', 'te_class', te_class);
    
    full_class = vertcat(tr_class, te_class);
    assignin('base', 'full_class', full_class);
    
    radii = ones(1,d(2)+1)*0.2;
    radii(1, end) = 1;

    xBounds = zeros(2, length(full_data(1,:))+1);
    for n = 1:length(full_data(1,:))
        xBounds(1,n) = min(full_data(:,n));
        xBounds(2,n) = max(full_data(:,n));
    end
    xBounds(1,length(full_data(1,:))+1)=0;
    xBounds(2,length(full_data(1,:))+1)=1;

    dispOpt = ones(1,4);
    trnOpt = NaN
    
    if k == 0
        k = 10
    end
    
    CVO = cvpartition(full_class, 'k', k);
    assignin('base', 'CVO', CVO);
    err = zeros(CVO.NumTestSets, 1);
    trIdx = CVO.training(1);
    assignin('base', 'trIdx', trIdx);
    teIdx = CVO.test(1);
    assignin('base', 'teIdx', teIdx);
    size(trIdx==1);
    size(teIdx==1);
    
    chkIn = full_data(CVO.training(2),:);
    chkCl = full_class(CVO.test(2),:);
    
    assignin('base', 'chkIn', chkIn);
    assignin('base', 'chkCl', chkCl);

    tr_in = full_data(trIdx,:);
    tr_cl = full_class(trIdx,:);
    
    assignin('base', 'tr_in', tr_in);
    assignin('base', 'tr_cl', tr_cl);
    
    te_in = full_data(teIdx,:);
    te_cl = full_class(teIdx,:);
    
    assignin('base', 'te_in', te_in);
    assignin('base', 'te_cl', te_cl);
    
    tr_full = [tr_in tr_cl];
    te_full = [te_in te_cl];
    
    
    disp('FIS2 GEN')
    gf2 = genfis2(tr_in, tr_cl, radii, xBounds);
    assignin('base', 'gf2', gf2);

    
    disp('Anfis start ')
    
    % an1 = anfis([full_data full_class], gf2);
    
    an1 = anfis([tr_in tr_cl], gf2, trnOpt, dispOpt);
    
    %[an1,error,stepsize,chkFis,chkErr] = anfis([tr_in tr_cl], gf2, trnOpt, dispOpt, [chkIn chkCl])
    
    %res = [an1,error,stepsize,chkFis,chkErr]
    %assignin('base', 'res', res);
    
    %assignin('base', 'error', error);
    %assignin('base', 'chkFis', chkFis);
    %assignin('base', 'chkErr', chkErr);
    
    assignin('base', 'sensor_data_tr', sensor_data_tr);
    assignin('base', 'sensor_data_te', sensor_data_te);
    assignin('base', 'an1', an1);
    
    disp('evalfis start ')
    output = evalfis(te_in, an1);
    assignin('base', 'output', output);
    
    max_a = max(output,[],1);
    min_a = min(output,[],1);
    [row,col] = size(output);
    output_norm=((repmat(max_a,row,1)-output)./repmat(max_a-min_a,row,1));
    
    assignin('base', 'output_norm', output_norm);
    assignin('base', 'input_names', input_names);
    save(name, 'gf2', 'an1', 'output','output_norm','arg_list', 'arduino_te',  'arduino_tr', 'CVO', 'full_class', 'full_data', 'full_labels', ...
    'labels_tr', 'labels_te', 'm_tr', 'm_te', 'rf_tr', 'rf_te',  'rll_tr', 'rll_te', 'rul_tr', 'rul_te', ...
    'sensor_data_tr', 'sensor_data_te', 'teIdx', 'trIdx', 'tr_in', 'tr_cl', 'te_in', 'te_cl', 'input_names')
    
end
