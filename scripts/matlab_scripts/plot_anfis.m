files = dir('/home/lydakis-local/bu_mat')
za = [];
oa = [];
ta = [];
names = {};
index = 1;
for file = files';
    if findstr(file.name, 'accu') > 0 ;
        x = load(['/home/lydakis-local/bu_mat/' file.name]);
        za = [za x.zeroes_acc/x.k];
        oa = [oa x.ones_acc/x.k];
        ta = [ta x.total_acc/x.k];
        names{index} = file.name;
        index = index + 1;
    end
end

[mta ita] = max(ta)
[moa ioa] = max(oa)
[mza iza] = max(za)

disp('Max ta')
names{ita}
disp('ta')
ta(ita)
disp('oa')
oa(ita)
disp('za')
za(ita)

disp('Max oa')
names{ioa}
disp('ta')
ta(ioa)
disp('oa')
oa(ioa)
disp('za')
za(ioa)

disp('Max za')
names{iza}
disp('ta')
ta(iza)
disp('oa')
oa(iza)
disp('za')
za(iza)
