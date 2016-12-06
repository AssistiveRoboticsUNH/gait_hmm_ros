p = 'normal';
%p = 'phase'
set(groot,'DefaultFigureRenderer','opengl');
create_anfis_list('subject1');
%create_anfis_list('subject2');
%create_anfis_list('subject3');

build_anfis_classifier_loop('subject1');
%build_anfis_classifier_loop('subject2');
%build_anfis_classifier_loop('subject3');
