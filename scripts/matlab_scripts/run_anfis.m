tic
fsr_anfis(1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 'fsr_mocap_anfis_with_ir_prox_chk', 0, 10, 1)
toc
clear all
tic
fsr_anfis(1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 'fsr_mocap_anfis_without_ir_prox_chk', 0, 10, 1)
toc
clear all
tic
fsr_anfis(1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 'fsr_anfis_with_ir_prox_chk', 0, 10, 0)
toc
clear all
tic
fsr_anfis(1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 'fsr_anfis_without_ir_prox_chk', 0, 10, 0)
toc
clear all

tic
fsr_anfis_combined(1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 'fsr_anfis_mocap_combined_ir_prox_chk', 0, 10, 1)
toc
clear all
tic
fsr_anfis_combined(1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 'fsr_anfis_mocap_combined_without_ir_prox_chk', 0, 10, 1)
toc
clear all
tic
fsr_anfis_combined(1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 'fsr_anfis_combined_ir_prox_chk', 0, 10, 0)
toc
clear all
tic
fsr_anfis_combined(1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 'fsr_anfis_combined_without_ir_prox_chk', 0, 10, 0)
toc
clear all

tic
fsr_anfis_with_clearance(1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 'fsr_mocap_anfis_with_clearance_ir_prox_chk', 0, 10, 1)
toc
clear all
tic
fsr_anfis_with_clearance(1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 'fsr_mocap_anfis_with_clearance_without_ir_prox_chk', 0, 10, 1)
toc
clear all
tic
fsr_anfis_with_clearance(1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 'fsr_anfis_with_clearance_ir_prox_chk', 0, 10, 0)
toc
clear all
tic
fsr_anfis_with_clearance(1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 'fsr_anfis_with_clearance_without_ir_prox_chk', 0, 10, 0)
toc
clear all



