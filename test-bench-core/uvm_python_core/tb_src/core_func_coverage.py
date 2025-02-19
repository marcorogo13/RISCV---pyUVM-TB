'''
Functional coverage based on the instructions fed to the core.
Not always all the extensions are used so different sets from I, M, C, J, B additionally C compressed instruction set could be used.

'''


from cocotb import *
from pyuvm import *
import cocotb
import pyuvm




### OPCODES ###
OPCODE_LOAD     = 0x03
OPCODE_MISC_MEM = 0x0F
OPCODE_OP_IMM   = 0x13
OPCODE_AUIPC    = 0x17
OPCODE_STORE    = 0x23
OPCODE_OP       = 0x33
OPCODE_LUI      = 0x37
OPCODE_BRANCH   = 0x63
OPCODE_JALR     = 0x67
OPCODE_JAL      = 0x6F
OPCODE_SYSTEM   = 0x73



### R TYPE ###
R_FUNCT_3_DICT = {
  0x00: 'ADD/SUB',
  0x01: 'SLL',
  0x02: 'SLT',
  0x03: 'SLTU',
  0x04: 'XOR',
  0x05: 'SRL/SRA',
  0x06: 'OR',
  0x07: 'AND'
}

RM_FUNCT_3_DICT = {
  0x00: 'MUL',
  0x01: 'MULH',
  0x02: 'MULHSU',
  0x03: 'MULHU',
  0x04: 'DIV',
  0x05: 'DIVU',
  0x06: 'REM',
  0x07: 'REMU'
}

ADD_SUB_FUNCT_7_DICT = {
  0x00: 'ADD',
  0x20: 'SUB'
}

SRL_SRA_FUNCT_7_DICT = {
  0x00: 'SRL',
  0x20: 'SRA'
}

### I TYPE ###
I_FUNCT_3_DICT = {
  0x00: 'ADDI',
  0x04: 'XORI',
  0x06: 'ORI',
  0x07: 'ANDI',
  0x01: 'SLLI',
  0x05: 'SRLI/SRAI',
  0x02: 'SLTI',
  0x03: 'SLTI(U)'
}




### LOAD TYPE ### (actually I type)
S_FUNCT_3_DICT = {
  0x00: 'LB',
  0x01: 'LH',
  0x02: 'LW',
  0x04: 'LB(U)',
  0x05: 'LH(U)'
}

### S TYPE ###
S_FUNCT_3_DICT = {
  0x00: 'SB',
  0x01: 'SH',
  0x02: 'SW'
}



### B TYPE ###
B_FUNCT_3_DICT = {
  0x00: 'BEQ',
  0x01: 'BNE',
  0x04: 'BLT',
  0x05: 'BGE',
  0x06: 'BLTU',
  0x07: 'BGEU'
}



###  field extraction for normal instr ###


def get_opcode(instruction):
  return instruction & 0x7F

def get_rd(instruction):
  return (instruction >> 7) & 0x1F

def get_funct3(instruction):
  return (instruction >> 12) & 0x07

def get_rs1(instruction):
  return (instruction >> 15) & 0x1F

def get_rs2(instruction):
  return (instruction >> 20) & 0x1F

def get_funct7(instruction):
  return (instruction >> 25) & 0x7F



def get_imm_i(instruction):
  imm = (instruction >> 20) & 0xFFF
  return imm

def get_imm_s(instruction):
  imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)
  return imm

def get_imm_b(instruction):
  imm = ((instruction >> 31) << 12) | (((instruction >> 7) & 0x1) << 11) | (((instruction >> 25) & 0x3F) << 5) | (((instruction >> 8) & 0xF) << 1)
  return imm

def get_imm_j(instruction):
  imm = ((instruction >> 31) << 20) | (((instruction >> 12) & 0xFF) << 12) | (((instruction >> 20) & 0x1) << 11) | ((instruction >> 21) & 0x3FF)
  return imm

def get_imm_auipc(instruction):
  imm = instruction & 0xFFFFF000







### field extraction for compressed ###


def get_c_opcode(instruction):
  return instruction & 0x03

def get_c_funct2(instruction):
  return (instruction >> 5) & 0x03

def get_c_funct3(instruction):
  return (instruction >> 13) & 0x07

def get_c_funct4(instruction):
  return (instruction >> 12) & 0x0F

def get_c_funct6(instruction):
  return (instruction >> 10) & 0x3F


def get_c_rs1(instruction):
  return (instruction >> 7) & 0x1F

def get_c_rs2(instruction):
  return (instruction >> 2) & 0x1F

def get_c_rs11(instruction):
  return (instruction >> 7) & 0x7

def get_c_rs21(instruction):
  return (instruction >> 2) & 0x7

def get_c_rd(instruction):
  return get_c_rs1(instruction)

def get_c_rd1(instruction):
  return get_c_rs21(instruction)




# Bins for instrucions covered are defined as sets and the coverage is calculated as the number of bins covered over the total number of bins

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

reg_dep_bin = {
  0,
  1,
  2,
  3,
  4,
  5,
  6
}



class core_func_coverage(uvm_subscriber):


  R_type_active = True
  I_type_active = True
  RM_type_active = True
  S_type_active = True
  B_type_active = True
  U_type_active = True
  J_type_active = True
  C_type_active = True


  instruction = None
  is_compressed = False
  decoded_instr = None
  rd = None
  funct2 = None
  funct3 = None
  funct4 = None 
  funct6 = None
  rs1 = None
  rs2 = None
  funct7 = None
  imm = None
  operation = None

  instr_type = None



  ## coverage bins ##
  R_type_hits = set()
  I_type_hits = set()
  RM_type_hits = set()
  S_type_hits = set()
  B_type_hits = set()
  U_type_hits = set()
  J_type_hits = set()
  C_type_hits = set()
  dep_hits = set()

  ### dependencies checks ###

  prev_instr = None
  prev_rd = None





  def init(self,name,parent):
    super().init(name,parent)
    self.instruction = None
    self.is_compressed = False
    self.decoded_instr = None
    self.decoded_instr_0 = None
    self.decoded_instr_1 = None
    self.rd = None
    self.funct2 = None
    self.funct3 = None
    self.funct4 = None 
    self.funct6 = None
    self.rs1 = None
    self.rs2 = None
    self.funct7 = None
    self.imm = None
    self.operation = None
    self.instr_type = None

    self.prev_instr = None
    self.prev_rd = None

    self.R_type_hits = set()
    self.I_type_hits = set()
    self.RM_type_hits = set()
    self.S_type_hits = set()
    self.B_type_hits = set()
    self.U_type_hits = set()
    self.J_type_hits = set()
    self.C_type_hits = set()




  ### actual write function that will be called from the monitor with the instruciton from the core ###    
  def write(self, instruction):
    

    self.prev_instr = self.decoded_instr
    self.prev_rd = self.rd
    
    ### default to None values if fields are not set ###
    
    self.decoded_instr = None
    self.rd = None
    self.rs1 = None
    self.rs2 = None

    # need to check if the instruction if compressed or not by looking at the two LSBs
    # if the last 2 bits are 1 the instruction is not compressed
    self.instruction = instruction
    self.compressed_bits = self.instruction & 0x3

    if self.compressed_bits == 0x3:
      is_compressed = False
      self.decode_standard()
    else:
      is_compressed = True
      self.decode_compressed()

  ### dependencies check ###
    dep = self.detect_dep()
    if dep:
      self.logger.info("Dependency detected")
      self.logger.info(f"Previous instruction ecoded as: {self.prev_instr} rd: {self.prev_rd} rs1: {self.rs1} rs2: {self.rs2}")
      self.logger.info(f"Current instruction decoded as: {self.decoded_instr} rd: {self.rd} rs1: {self.rs1} rs2: {self.rs2}")
      self.dep_hits.add(dep)
    else:
      self.dep_hits.add(dep)

    self.logger.info(f"Instruction: {hex(int(instruction))}, decoded as: {self.decoded_instr}")




  def decode_r_type(self):
    self.rd = get_rd(self.instruction)
    self.funct3 = get_funct3(self.instruction)
    self.rs1 = get_rs1(self.instruction)
    self.rs2 = get_rs2(self.instruction)
    self.funct7 = get_funct7(self.instruction)

    if self.funct7 == 0x01:
      self.decoded_instr = RM_FUNCT_3_DICT.get(self.funct3, "Unknown")
      self.RM_type_hits.add(self.decoded_instr)
    else:
      self.decoded_instr = R_FUNCT_3_DICT.get(self.funct3, "Unknown")
      if self.decoded_instr == 'SRL/SRA':
        self.decoded_instr = SRL_SRA_FUNCT_7_DICT.get(self.funct7, "Unknown")
      elif self.decoded_instr == 'ADD/SUB':
        self.decoded_instr = ADD_SUB_FUNCT_7_DICT.get(self.funct7, "Unknown")
      self.R_type_hits.add(self.decoded_instr)
    

  def decode_i_type(self):
    self.rd = get_rd(self.instruction)
    self.funct3 = get_funct3(self.instruction)
    self.funct7 = get_funct7(self.instruction)
    self.rs1 = get_rs1(self.instruction)
    self.imm = get_imm_i(self.instruction)

    self.decoded_instr = I_FUNCT_3_DICT.get(self.funct3, "Unknown")
    if self.decoded_instr == 'SRLI/SRAI':
      # imm[5:11]=0x00 means SRLI, imm[5:11]=0x20 means SRAI
      if (self.imm >> 5) & 0x3F == 0x20: 
        self.decoded_instr = 'SRAI'
      else:
        self.decoded_instr = 'SRLI'
    
    self.I_type_hits.add(self.decoded_instr)
    

  def decode_s_type(self):
    self.funct3 = get_funct3(self.instruction)
    self.rs1 = get_rs1(self.instruction)
    self.rs2 = get_rs2(self.instruction)
    self.imm = get_imm_s(self.instruction)

    self.decoded_instr = S_FUNCT_3_DICT.get(self.funct3, "Unknown")
    self.S_type_hits.add(self.decoded_instr)
    

  def decode_b_type(self):
    self.funct3 = get_funct3(self.instruction)
    self.rs1 = get_rs1(self.instruction)
    self.rs2 = get_rs2(self.instruction)
    self.imm = get_imm_b(self.instruction)

    self.decoded_instr = B_FUNCT_3_DICT.get(self.funct3, "Unknown")
    self.B_type_hits.add(self.decoded_instr)
    

  def decode_lui_type(self):
    self.rd = get_rd(self.instruction)
    self.imm = get_imm_auipc(self.instruction)
    self.decoded_instr = 'LUI'
    self.U_type_hits.add(self.decoded_instr)
    

  def decode_auipc_type(self):
    self.rd = get_rd(self.instruction)
    self.imm = get_imm_auipc(self.instruction)
    self.decoded_instr = 'AUIPC'
    self.U_type_hits.add(self.decoded_instr)
    

  def decode_j_type(self):
    self.rd = get_rd(self.instruction)
    self.imm = get_imm_j(self.instruction)
    self.decoded_instr = 'JAL'
    self.J_type_hits.add(self.decoded_instr)
    

  def decode_jr_type(self):
    self.rd = get_rd(self.instruction)
    self.imm = get_imm_j(self.instruction)
    self.decoded_instr = 'JALR'
    self.J_type_hits.add(self.decoded_instr)
    


  def decode_standard(self):
    self.opcode = get_opcode(self.instruction)

    if self.opcode == OPCODE_OP:
      return self.decode_r_type()
    elif self.opcode == OPCODE_OP_IMM:
      return self.decode_i_type()
    elif self.opcode == OPCODE_LOAD:
      return self.decode_i_type()
    elif self.opcode == OPCODE_STORE:
      return self.decode_s_type()
    elif self.opcode == OPCODE_BRANCH:
      return self.decode_b_type()
    elif self.opcode == OPCODE_LUI:
      return self.decode_lui_type()
    elif self.opcode == OPCODE_AUIPC:
      return self.decode_auipc_type()
    elif self.opcode == OPCODE_JAL:
      return self.decode_j_type()
    elif self.opcode == OPCODE_JALR:
      return self.decode_jr_type()
    elif self.opcode == OPCODE_SYSTEM:
      return self.decode_i_type()
    else:
      self.logger.info("Unknown standard instruction")
      return None




  ### compressed instructions ###

  def decode_comp_op0(self):
    if self.funct3 == 0x2:
      self.decoded_instr = 'C.LW'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rs11(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x6:
      self.decoded_instr = 'C.SW'
      self.rs1 = get_c_rs11(self.instruction)
      self.rs2 = get_c_rs21(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x0:
      self.decoded_instr = 'C.ADDI4SPPN'
      self.rd = get_c_rd1(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    else:
      print("Unknown compressed op0 instruction")
      return None
  
  def decode_comp_op1(self):
    if self.funct3 == 0x5:
      self.decoded_instr = 'C.J'
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x1:
      self.decoded_instr = 'C.JAL'
      self.rd = 1 # x1 is ra
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x2:
      self.decoded_instr = 'C.LI'
      self.rd = get_c_rd(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x3:
      if (self.instruction >> 7) & 0x5 == 0x2:
        self.decoded_instr = 'C.ADDI16SP'
        self.rd = 2 # x2 is sp
        self.rs1 = 2
        self.C_type_hits.add(self.decoded_instr)
        
      else:
        self.decoded_instr = 'C.LUI'
        self.rd = get_c_rd(self.instruction)
        self.C_type_hits.add(self.decoded_instr)
        
    elif self.funct3 == 0x0:
      self.decoded_instr = 'C.ADDI'
      self.rd = get_c_rd(self.instruction)
      self.rs1 = get_c_rd(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      self.C_type_hits.add('C.NOP')
      
    elif self.funct4 == 0x4 and self.funct2 == 0x0:
      self.decoded_instr = 'C.SRLI'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct4 == 0x4 and self.funct2 == 0x1:
      self.decoded_instr = 'C.SRAI'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct4 == 0x4 and self.funct2 == 0x2:
      self.decoded_instr = 'C.ANDI'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
      # funct 6 and funct2 need to be concated to get the 8 bit funct
    elif self.funct6 << 2 | self.funct2 == 0x8F: #0b10001111
      self.decoded_instr = 'C.AND'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.rs2 = get_c_rs21(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct6 << 2 | self.funct2 == 0x8E: #0b10001110
      self.decoded_instr = 'C.OR'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.rs2 = get_c_rs21(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct6 << 2 | self.funct2 == 0x8D: #0b10001101
      self.decoded_instr = 'C.XOR'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.rs2 = get_c_rs21(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct6 << 2 | self.funct2 == 0x8C: #0b10001100
      self.decoded_instr = 'C.SUB'
      self.rd = get_c_rd1(self.instruction)
      self.rs1 = get_c_rd1(self.instruction)
      self.rs2 = get_c_rs21(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    else: 
      print("Unknown compressed op1 instruction")
      return None

  def decode_comp_op2(self):
    if self.funct3 == 0x0:
      self.decoded_instr = 'C.SLLI'
      self.rd = get_c_rd(self.instruction)
      self.rs1 = get_c_rd(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x2:
      self.decoded_instr = 'C.LWSP'
      self.rd = get_c_rd(self.instruction)
      self.rs1 = 2 # x2 is sp
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct3 == 0x6:
      self.decoded_instr = 'C.SWSP'
      self.rs1 = 2 # x2 is sp
      self.rs2 = get_c_rs2(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct4 == 0x8:
      self.decoded_instr = 'C.JR'
      self.rs1 = get_c_rs1(self.instruction)
      self.C_type_hits.add(self.decoded_instr)
      
    elif self.funct4 == 0x9:
      if (self.instruction >> 2) & 0x5 != 0: 
        self.decoded_instr = 'C.ADD'
        self.rd = get_c_rd(self.instruction)
        self.rs1 = get_c_rd(self.instruction)
        self.rs2 = get_c_rs2(self.instruction)
        self.C_type_hits.add(self.decoded_instr)
        
      else: 
        if (self.instruction >> 7) & 0x5 == 0:
          self.decoded_instr = 'C.EBREAK'
          self.C_type_hits.add(self.decoded_instr)
          
        else:
          self.decoded_instr = 'C.JALR'
          self.rd = 1 # x1 is ra
          self.rs1 = get_c_rs1(self.instruction)
          self.C_type_hits.add(self.decoded_instr)
          
    else:
      print("Unknown compressed op2 instruction")
      return None
    
    


  def decode_compressed(self):
    self.opcode = get_c_opcode(self.instruction)
    self.funct2 = get_c_funct2(self.instruction)
    self.funct3 = get_c_funct3(self.instruction)
    self.funct4 = get_c_funct4(self.instruction)
    self.funct6 = get_c_funct6(self.instruction)

    if self.opcode == 0x00:
      self.decode_comp_op0()
    elif self.opcode == 0x01:
      self.decode_comp_op1()
    elif self.opcode == 0x02:
      self.decode_comp_op2()
    else:
      print("Unknown generic compressed instruction")
      self.decoded_instr = None



  ### check for dependencies between instructions ###
  def detect_dep(self):
   
    # check for memory dependencies
    if (self.prev_instr == 'LW' or self.prev_instr == 'LH' or self.prev_instr == 'LB' or self.prev_instr == 'LWU' or self.prev_instr == 'LHU' or self.prev_instr == 'LBU'):
      if self.prev_rd == self.rs1:
        return 3
      elif self.prev_rd == self.rs2:
        return 4
    
    if(self.prev_instr == 'C.LW' or self.prev_instr == 'C.LH' or self.prev_instr == 'C.LB' or self.prev_instr == 'C.LWU' or self.prev_instr == 'C.LHU' or self.prev_instr == 'C.LBU'):
      if self.prev_rd == self.rs1:
        return 3
      elif self.prev_rd == self.rs2:
        return 4
    
    # check for mul and div dependencies
    if (self.prev_instr == 'MUL' or self.prev_instr == 'MULH' or self.prev_instr == 'MULHSU' or self.prev_instr == 'MULHU' or self.prev_instr == 'DIV' or self.prev_instr == 'DIVU' or self.prev_instr == 'REM' or self.prev_instr == 'REMU'):
      if self.prev_rd == self.rs1:
        return 5
      elif self.prev_rd == self.rs2:
        return 6
    
    if (self.prev_instr == 'C.MUL' or self.prev_instr == 'C.MULH' or self.prev_instr == 'C.MULHSU' or self.prev_instr == 'C.MULHU' or self.prev_instr == 'C.DIV' or self.prev_instr == 'C.DIVU' or self.prev_instr == 'C.REM' or self.prev_instr == 'C.REMU'):
      if self.prev_rd == self.rs1:
        return 5
      elif self.prev_rd == self.rs2:
        return 6
    
    # other general dependencies
    if ((self.prev_rd is not None) and (self.prev_rd != 0)):
      if self.prev_rd == self.rs1:
        return 1
      elif self.prev_rd == self.rs2:
        return 2
    
    return 0






  def report_phase(self):
    R_type_cov = len(self.R_type_hits) / len(R_type_bin) * 100
    I_type_cov = len(self.I_type_hits) / len(I_type_bin) * 100
    RM_type_cov = len(self.RM_type_hits) / len(RM_type_bin) * 100
    S_type_cov = len(self.S_type_hits) / len(S_type_bin) * 100
    B_type_cov = len(self.B_type_hits) / len(B_type_bin) * 100
    U_type_cov = len(self.U_type_hits) / len(U_type_bin) * 100
    J_type_cov = len(self.J_type_hits) / len(J_type_bin) * 100
    C_type_cov = len(self.C_type_hits) / len(C_type_bin) * 100
    dep_cov = len(self.dep_hits) / len(reg_dep_bin) * 100

    if self.R_type_active:
      self.logger.info("R type coverage: %d%%", R_type_cov)

    if self.I_type_active:
      self.logger.info("I type coverage: %d%%", I_type_cov)
    if self.RM_type_active:
      self.logger.info("RM type coverage: %d%%", RM_type_cov)
    if self.S_type_active:
      self.logger.info("S type coverage: %d%%", S_type_cov)
    if self.B_type_active:
      self.logger.info("B type coverage: %d%%", B_type_cov)
    if self.U_type_active:
      self.logger.info("U type coverage: %d%%", U_type_cov)
    if self.J_type_active:
      self.logger.info("J type coverage: %d%%", J_type_cov)
    if self.C_type_active:
      self.logger.info("C type coverage: %d%%", C_type_cov)
      
    self.logger.info("Dependency coverage: %d%%", dep_cov)


    with open('func_coverage_report.txt', 'w') as f:
      if self.R_type_active:
        f.write(f"cve2_R_type: {R_type_cov:.2f}%\n")
      if self.I_type_active:
        f.write(f"cve2_I_type: {I_type_cov:.2f}%\n")
      if self.RM_type_active:
        f.write(f"cve2_RM_type: {RM_type_cov:.2f}%\n")
      if self.S_type_active:
        f.write(f"cve2_S_type: {S_type_cov:.2f}%\n")
      if self.B_type_active:
        f.write(f"cve2_B_type: {B_type_cov:.2f}%\n")
      if self.U_type_active:
        f.write(f"cve2_U_type: {U_type_cov:.2f}%\n")
      if self.J_type_active:
        f.write(f"cve2_J_type: {J_type_cov:.2f}%\n")
      if self.C_type_active:
        f.write(f"cve2_C_type: {C_type_cov:.2f}%\n")

      f.write(f"cve2_rg_dep: {dep_cov:.2f}%\n")


