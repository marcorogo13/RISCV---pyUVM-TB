
import random
import argparse



# actions from the instr agent
# RANDOM_INSTR = 0
LOGIC = 0
SHIFT_LEFT = 1
SHIFT_RIGHT = 2
ADD_SUB = 3
MUL = 4
DIV = 5
REM = 6
LOAD = 7
STORE = 8
JUMP = 9
BRANCH_EQ_NE = 10
BRANCH_LT = 11
BRANCH_GE = 12
LOAD_IMM = 13
ILLEGAL_INSTR = 14

# actions from the rd agent

RANDOM_RD = 32
# for the others just 1 = x1...

# actions from the rs1 agent
RANDOM_RS1 = 32


# actions from the rs2 agent
RANDOM_RS2 = 32

# actions from the imm agent
ZERO_IMM = 0
ALL_ONES_IMM = 1
SMALL_IMM = 2
BIG_IMM = 3
RANDOM_IMM = 4


# max value for immediate values 
I_S_B_MIN_IMM = -2048
I_S_B_MAX_IMM = 2047
U_J_MIN_IMM = 0
U_J_MAX_IMM = 1048575




R_type_bin = {
  'ADD',
  'SUB',
  'SLL',
  'SLT',
  'SLTU',
  'SRA',
  'XOR',
  'SRL',
  'OR',
  'AND'
}

I_type_bin = {
  'ADDI',
  'XORI',
  'ORI',
  'ANDI',
  'SLLI',
  'SRLI',
  'SRAI',
  'SLTI',
  'SLTI(U)'
}

RM_type_bin = {
  'MUL',
  'MULH',
  'MULHSU',
  'MULHU',
  'DIV',
  'DIVU',
  'REM',
  'REMU'
}

S_type_bin = {
  'SB',
  'SH',
  'SW'
}

B_type_bin = {
  'BEQ',
  'BNE',
  'BLT',
  'BGE',
  'BLTU',
  'BGEU'
}

U_type_bin = {
  'LUI',
  'AUIPC'
}

J_type_bin = {
  'JAL',
  'JALR'
}

C_type_bin = {
  'C.LW',
  'C.SW',
  'C.ADDI4SPPN',
  'C.J',
  'C.JAL',
  'C.LI',
  'C.ADDI16SP',
  'C.LUI',
  'C.ADDI',
  'C.NOP',
  'C.SRLI',
  'C.SRAI',
  'C.ANDI',
  'C.AND',
  'C.OR',
  'C.XOR',
  'C.SUB',
  'C.SLLI',
  'C.LWSP',
  'C.SWSP',
  'C.JR',
  'C.ADD',
  'C.EBREAK',
  'C.JALR'
}


### particular bins ###


LOGIC_bin = {
  'AND',
  'OR',
  'XOR'
}

LOGIC_imm_bin = {
  'ANDI',
  'ORI',
  'XORI'
}

SHIFT_LEFT_bin = {
  'SLL',
  'SLT',
  'SLTU'
}

SHIFT_RIGHT_bin = {
  'SRA',
  'SRL'
}

SHIFT_LEFT_imm_bin = {
  'SLLI',
  'SLTI',
}

SHIFT_RIGHT_imm_bin = {
  'SRAI',
  'SRLI'
}


ADD_SUB_bin = {
  'ADD',
  'SUB'
}

ADD_SUB_imm_bin = {
  'ADDI'
}

MUL_bin = {
  'MUL',
  'MULH',
  'MULHSU',
  'MULHU'
}


DIV_bin = {
  'DIV',
  'DIVU'
}

REM_bin = {
  'REM',
  'REMU'
}

LOAD_bin = {
  'LW',
  'LH',
  'LB'
}

STORE_bin = {
  'SW',
  'SH',
  'SB'
}

BRANCH_EQ_NE_bin = {
  'BEQ',
  'BNE'
}

BRANCH_LT_bin = {
  'BLT',
  'BLTU'
}

BRANCH_GE_bin = {
  'BGE',
  'BGEU'
}

JUMP_type_bin = {
  'JAL',
}

JUMP_REG_type_bin = {
  'JALR',
}



### register bins ###


def generate_imm(inst_typ, imm_act):
  if imm_act == ZERO_IMM:
    return 0
  elif imm_act == ALL_ONES_IMM:
    if inst_typ in I_type_bin:
      return I_S_B_MIN_IMM
    elif inst_typ in U_type_bin:
      return U_J_MIN_IMM
  elif imm_act == SMALL_IMM:
    if inst_typ in I_type_bin:
      return random.choice(list(range(0, 128)))
    elif inst_typ in U_type_bin:
      return random.choice(list(range(0, 128)))
  elif imm_act == BIG_IMM:
    if inst_typ in I_type_bin:
      return random.choice(list(range(-2048,-512)))
    elif inst_typ in U_type_bin:
      return random.choice(list(range(128, 1048575)))
  elif imm_act == RANDOM_IMM:
    if inst_typ in I_type_bin:
      return random.choice(list(range(I_S_B_MIN_IMM, I_S_B_MAX_IMM)))
    elif inst_typ in U_type_bin:
      return random.choice(list(range(0, U_J_MAX_IMM)))


def generate_rd(rd_act):
  if rd_act == RANDOM_RD:
    return random.choice(list(range(1, 32)))
  else:
    return rd_act

def generate_rs1(rs1_act):
  if rs1_act == RANDOM_RS1:
    return random.choice(list(range(1, 32)))
  else:
    return rs1_act

def generate_rs2(rs2_act):
  if rs2_act == RANDOM_RS2:
    return random.choice(list(range(1, 32)))
  else:
    return rs2_act



class R_type_instruction:
  def __init__(self, instr, rd_act, rs1_act, rs2_act):
    self.instr = instr
    if rd_act is not None:
      self.rd = generate_rd(rd_act)
    else:
      self.rd = generate_rd(RANDOM_RD)
    if rs1_act is not None:
      self.rs1 = generate_rs1(rs1_act)
    else:
      self.rs1 = generate_rs1(RANDOM_RS1)
    if rs2_act is not None:
      self.rs2 = generate_rs2(rs2_act)
    else:
      self.rs2 = generate_rs2(RANDOM_RS2)
  

  def __str__(self):
    return f"{self.instr} x{self.rd}, x{self.rs1}, x{self.rs2}"

class I_type_instruction:
  def __init__(self, instr, rd_act, rs1_act, imm_act, force_imm):
    self.instr = instr
    self.rd = generate_rd(rd_act)
    self.rs1 = generate_rs1(rs1_act)
    if force_imm is not None:
      self.imm = force_imm
    else:
      self.imm = generate_imm(instr, imm_act)
  
  def __str__(self):
    return f"{self.instr} x{self.rd}, x{self.rs1}, {self.imm}"


class RM_type_instruction:
  def __init__(self, instr, rd_act, rs1_act, rs2_act):
    self.instr = instr
    self.rd = generate_rd(rd_act)
    self.rs1 = generate_rs1(rs1_act)
    self.rs2 = generate_rs2(rs2_act)

  def __str__(self):
    return f"{self.instr} x{self.rd}, x{self.rs1}, x{self.rs2}"


class S_type_instruction:
  def __init__(self, instr, rd_act, rs1_act, imm_act, force_imm):
    self.instr = instr
    self.rd = generate_rs2(rd_act) 
    self.rs1 = generate_rs1(rs1_act)
    if force_imm is not None:
      self.imm = force_imm
    else:
      self.imm = generate_imm(instr, imm_act)

  def __str__(self):
    return f"{self.instr} x{self.rd}, {self.imm}(x{self.rs1})"



class B_type_instruction:
  def __init__(self, instr, rs1_act, rs2_act, instr_count):
    self.instr = instr
    self.rs1 = generate_rs1(rs1_act)
    self.rs2 = generate_rs2(rs2_act)
    self.instr_count = instr_count

  def __str__(self):
    return f"{self.instr} x{self.rs1}, x{self.rs2}, target_branch{self.instr_count}"

class U_type_instruction:
  def __init__(self, instr, rd_act, imm_act):
    self.instr = instr
    self.rd = generate_rd(rd_act)
    self.imm = generate_imm(instr, imm_act)

  def __str__(self):
    return f"{self.instr} x{self.rd}, {self.imm}"


class J_type_instruction:
  def __init__(self, instr, rd_act, rs1_act, force_imm):
    if instr == 'JAL':
      self.instr = instr
      self.rd = generate_rd(rd_act)
      self.rs1 = generate_rs1(rs1_act)
    else:
      self.instr = instr
      self.rd = generate_rd(rd_act)
      self.imm = force_imm
      self.rs1 = generate_rs1(rs1_act)

  def __str__(self):
    if self.instr == 'JAL':
      if self.rd != 0:
        return f"{self.instr} x{self.rd}, target_jal"
      elif self.rd == 0:
        self.instr = 'J'
        return f"{self.instr} target"
    elif self.instr == 'JALR':
      return f"{self.instr} x{self.rd}, {self.imm}(x{self.rs1})"
    else:
      print("Error in J_type_instruction __str__")


def generate_instruction(instruction_type, rd_act, rs1_act, rs2_act, imm_act, choose_imm, instr_count):
  # if instruction_type == RANDOM_INSTR:
  #   instruction_type = random.choice(list(range(1, 8)))

  if instruction_type == LOAD_IMM:
    # LUI or LI (addi)
    choices = ['LUI', 'ADDI']
    instr = random.choice(choices)
    if instr == 'LUI':
      return U_type_instruction(instr, rd_act, imm_act)
    elif instr == 'ADDI':
      return I_type_instruction(instr, rd_act, 0, imm_act, None)
    else:
      print("Error in LOAD_IMM")
      return None

  if instruction_type == LOGIC:
    if choose_imm == 0:
      instr = random.choice(list(LOGIC_bin))
      return R_type_instruction(instr, rd_act, rs1_act, rs2_act)
    elif choose_imm == 1:
      instr = random.choice(list(LOGIC_imm_bin))
      return I_type_instruction(instr, rd_act, rs1_act, imm_act, None)
  elif instruction_type == SHIFT_LEFT:
    if choose_imm == 0:
      instr = random.choice(list(SHIFT_LEFT_bin))
      return R_type_instruction(instr, rd_act, rs1_act, rs2_act)
    elif choose_imm == 1:
      instr = random.choice(list(SHIFT_LEFT_imm_bin))
      force_imm = random.choice(list(range(0, 32)))
      return I_type_instruction(instr, rd_act, rs1_act, imm_act, force_imm)
  elif instruction_type == SHIFT_RIGHT:
    if choose_imm == 0:
      instr = random.choice(list(SHIFT_RIGHT_bin))
      return R_type_instruction(instr, rd_act, rs1_act, rs2_act)
    elif choose_imm == 1:
      instr = random.choice(list(SHIFT_RIGHT_imm_bin))
      force_imm = random.choice(list(range(0, 32)))
      return I_type_instruction(instr, rd_act, rs1_act, imm_act, force_imm)
  elif instruction_type == ADD_SUB:
    if choose_imm == 0:
      instr = random.choice(list(ADD_SUB_bin))
      return R_type_instruction(instr, rd_act, rs1_act, rs2_act)
    elif choose_imm == 1:
      instr = random.choice(list(ADD_SUB_imm_bin))
      return I_type_instruction(instr, rd_act, rs1_act, imm_act, None)
  elif instruction_type == MUL:
    instr = random.choice(list(MUL_bin))
    return RM_type_instruction(instr, rd_act, rs1_act, rs2_act)
  elif instruction_type == DIV:
    instr = random.choice(list(DIV_bin))
    return RM_type_instruction(instr, rd_act, rs1_act, rs2_act)
  elif instruction_type == REM:
    instr = random.choice(list(REM_bin))
    return RM_type_instruction(instr, rd_act, rs1_act, rs2_act)
  elif instruction_type == LOAD:
    return_instrs = []
    rs1 = generate_rd(rs1_act)
    if rs1 == 0:
      rs1 = 1
    la_instr = f"LA x{rs1}, _stack_start"
    return_instrs.append(la_instr)
    s_instr = random.choice(list(LOAD_bin))
    s_instr = S_type_instruction(instr=s_instr, rd_act = rd_act, rs1_act=rs1, imm_act=imm_act, force_imm=4)
    return_instrs.append(s_instr)
    return return_instrs
  elif instruction_type == STORE:
    return_instrs = []
    rs1 = generate_rd(rs1_act)
    if rs1 == 0:
      rs1 = 1
    la_instr = f"LA x{rs1}, _stack_start"
    return_instrs.append(la_instr)
    s_instr = random.choice(list(STORE_bin))
    s_instr = S_type_instruction(instr=s_instr, rd_act = rd_act, rs1_act=rs1, imm_act=imm_act, force_imm=4)
    return_instrs.append(s_instr)
    return return_instrs
  elif instruction_type == JUMP:
    instr = random.choice(list(J_type_bin))
    if instr == 'JAL' and rd_act == 0:
      return_instrs = []
      jal_instr = J_type_instruction(instr, rd_act, rs1_act, imm_act)
      return_instrs.append(jal_instr)
      for i in range(0, random.randint(0, 8)):
        nop_instr = I_type_instruction('ADDI', 0, 0, 0, None)
        return_instrs.append(nop_instr)
      return_instrs.append("target:")
      return return_instrs
    elif instr == 'JAL' and rd_act != 0:
      jal_instr = J_type_instruction(instr, 1, rs1_act, 0)
      return jal_instr
    elif instr == 'JALR':
      return_instrs = []
      la = "LA x2, target_jal"
      return_instrs.append(la)
      jalr_instr = J_type_instruction(instr, 1, 2, 0)
      return_instrs.append(jalr_instr)
      return return_instrs
  elif instruction_type == BRANCH_EQ_NE:
    return_instrs = []
    instr = random.choice(list(BRANCH_EQ_NE_bin))
    b_instr = B_type_instruction(instr, rs1_act, rs2_act, instr_count)
    return_instrs.append(b_instr)
    for i in range(0, random.randint(0, 4)):
      nop_instr = I_type_instruction('ADDI', 0, 0, 0, None)
      return_instrs.append(nop_instr)
    return_instrs.append(f"target_branch{instr_count}:")
    return return_instrs
  elif instruction_type == BRANCH_LT:
    return_instrs = []
    instr = random.choice(list(BRANCH_LT_bin))
    b_instr = B_type_instruction(instr, rs1_act, rs2_act, instr_count)
    return_instrs.append(b_instr)
    for i in range(0, random.randint(0, 4)):
      nop_instr = I_type_instruction('ADDI', 0, 0, 0, None)
      return_instrs.append(nop_instr)
    return_instrs.append(f"target_branch{instr_count}:")    
    return return_instrs
  elif instruction_type == BRANCH_GE:
    return_instrs = []
    instr = random.choice(list(BRANCH_GE_bin))
    b_instr = B_type_instruction(instr, rs1_act, rs2_act, instr_count)
    return_instrs.append(b_instr)
    for i in range(0, random.randint(0, 4)):
      nop_instr = I_type_instruction('ADDI', 0, 0, 0, None)
      return_instrs.append(nop_instr)
    return_instrs.append(f"target_branch{instr_count}:")    
    return return_instrs    

  elif instruction_type == ILLEGAL_INSTR:
    return ".word 0x00000000"



if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Instruction Generator')

  # number of instructions to generate
  parser.add_argument('--num_instr', type=int, default=10, help='Number of instructions to generate')
  # instruction type
  parser.add_argument('--instr_type', type=int, default=None, help='Instruction type')
  # illegal instruction allowed
  parser.add_argument('--illegal_instr', type=bool, default=False, help='Allow illegal instructions')

  args = parser.parse_args()

  instr_count = 0


  with open('instrs.txt', 'w') as f:
    for i in range(0, args.num_instr):
      if args.instr_type is None:
        if args.illegal_instr:
          instr = generate_instruction(random.choice(list(range(0, 15))), RANDOM_RD, RANDOM_RS1, RANDOM_RS2, RANDOM_IMM, 0, instr_count)
        else:
          instr = generate_instruction(random.choice(list(range(0, 14))), RANDOM_RD, RANDOM_RS1, RANDOM_RS2, RANDOM_IMM, random.choice(list(range(0,1))), instr_count)
      else:
        instr = generate_instruction(args.instr_type, RANDOM_RD, RANDOM_RS1, RANDOM_RS2, RANDOM_IMM, 0, instr_count)
      if type(instr) == list:
        for i in instr:
          f.write(str(i) + "\n")
      else:
        f.write(str(instr) + "\n")
      instr_count += 1