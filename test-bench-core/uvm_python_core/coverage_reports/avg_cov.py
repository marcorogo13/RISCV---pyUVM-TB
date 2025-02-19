import numpy as np

ALU_WEIGHT = 7
COMPR_DECODER_WEIGHT = 7 
CONTROLLER_WEIGHT = 7
CORE_WEIGHT = 7
COUNTER_WEIGHT = 7
CS_REGISTERS_WEIGHT = 7
CSR_WEIGHT = 7
DECODER_WEIGHT = 7
FETCH_FIFO_WEIGHT = 7
ID_STAGE_WEIGHT = 7
IF_STAGE_WEIGHT = 7
LOAD_STORE_UNIT_WEIGHT = 7
MULTDIV_FAST_WEIGHT = 7
PREFETCH_BUFFER_WEIGHT = 7
REGISTER_FILE_FF_WEIGHT = 7
FSM_WEIGHT = 8 
R_TYPE_WEIGHT = 3
I_TYPE_WEIGHT = 3
RM_TYPE_WEIGHT = 3
S_TYPE_WEIGHT = 3
B_TYPE_WEIGHT = 3
U_TYPE_WEIGHT = 3
J_TYPE_WEIGHT = 3
C_TYPE_WEIGHT = 4
RG_DEP_WEIGHT = 1


coverages = np.zeros(25)

# collect the coverage from the coverage file 
try:
  cov_file = open("coverage_report.txt", "r")
except FileNotFoundError:
  raise missing_file("The coverage file is missing")

# read the lines and convert the values to values between 0 and 1
for i, line in enumerate(cov_file):
  coverages[i] = float(line.split(":")[1].strip("%\n")) / 100

avg_coverage = np.mean(coverages)

# calculate the total reward, as a weighted mean of the different coverages
weighted_coverage = ALU_WEIGHT * coverages[0] + COMPR_DECODER_WEIGHT * coverages[1] + CONTROLLER_WEIGHT * coverages[2] + CORE_WEIGHT * coverages[3] + COUNTER_WEIGHT * coverages[4] + CS_REGISTERS_WEIGHT * coverages[5] + CSR_WEIGHT * coverages[6] + DECODER_WEIGHT * coverages[7] + FETCH_FIFO_WEIGHT * coverages[8] + ID_STAGE_WEIGHT * coverages[9] + IF_STAGE_WEIGHT * coverages[10] + LOAD_STORE_UNIT_WEIGHT * coverages[11] + MULTDIV_FAST_WEIGHT * coverages[12] + PREFETCH_BUFFER_WEIGHT * coverages[13] + REGISTER_FILE_FF_WEIGHT * coverages[14] + FSM_WEIGHT * coverages[15] + R_TYPE_WEIGHT * coverages[16] + I_TYPE_WEIGHT * coverages[17] + RM_TYPE_WEIGHT * coverages[18] + S_TYPE_WEIGHT * coverages[19] + B_TYPE_WEIGHT * coverages[20] + U_TYPE_WEIGHT * coverages[21] + J_TYPE_WEIGHT * coverages[22] + C_TYPE_WEIGHT * coverages[23] + RG_DEP_WEIGHT * coverages[24]
weighted_coverage = weighted_coverage / (ALU_WEIGHT + COMPR_DECODER_WEIGHT + CONTROLLER_WEIGHT + CORE_WEIGHT + COUNTER_WEIGHT + CS_REGISTERS_WEIGHT + CSR_WEIGHT + DECODER_WEIGHT + FETCH_FIFO_WEIGHT + ID_STAGE_WEIGHT + IF_STAGE_WEIGHT + LOAD_STORE_UNIT_WEIGHT + MULTDIV_FAST_WEIGHT + PREFETCH_BUFFER_WEIGHT + REGISTER_FILE_FF_WEIGHT + FSM_WEIGHT + R_TYPE_WEIGHT + I_TYPE_WEIGHT + RM_TYPE_WEIGHT + S_TYPE_WEIGHT + B_TYPE_WEIGHT + U_TYPE_WEIGHT + J_TYPE_WEIGHT + C_TYPE_WEIGHT + RG_DEP_WEIGHT)

print("The average coverage is: ", avg_coverage)
print("The weighted coverage is: ", weighted_coverage)