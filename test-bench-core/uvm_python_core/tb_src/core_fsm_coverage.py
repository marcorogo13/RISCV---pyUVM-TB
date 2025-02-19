from cocotb import *
from pyuvm import *
import cocotb
import pyuvm
import csv


POSSIBLE_TRANSITIONS = {
  ('FIRST_FETCH', 'FIRST_FETCH'),
  ('LOAD_ERR_PRIO', 'LOAD_ERR_PRIO'),
  ('LOAD_ERR_PRIO', 'WAIT_SLEEP'),
  ('DBG_TAKEN_IF', 'DBG_TAKEN_IF'),
  ('SLEEP', 'FIRST_FETCH'),
  ('ECALL_INSN_PRIO', 'ECALL_INSN_PRIO'),
  ('FIRST_FETCH', 'DECODE'),
  ('IRQ_TAKEN', 'IRQ_TAKEN'),
  ('DECODE', 'DBG_TAKEN_IF'),
  ('LOAD_ERR_PRIO', 'DBG_TAKEN_IF'),
  ('STORE_ERR_PRIO', 'STORE_ERR_PRIO'),
  ('IRQ_TAKEN', 'DECODE'),
  ('FIRST_FETCH', 'IRQ_TAKEN'),
  ('DBG_TAKEN_ID', 'DECODE'),
  ('EBRK_INSN_PRIO', 'DBG_TAKEN_ID'),
  ('DBG_TAKEN_ID', 'DBG_TAKEN_ID'),
  ('DECODE', 'FLUSH'),
  ('WAIT_SLEEP', 'WAIT_SLEEP'),
  ('BOOT_SET', 'BOOT_SET'),
  ('SLEEP', 'SLEEP'),
  ('RESET', 'BOOT_SET'),
  ('FIRST_FETCH', 'DBG_TAKEN_IF'),
  ('DECODE', 'DECODE'),
  ('WAIT_SLEEP', 'SLEEP'),
  ('DBG_TAKEN_IF', 'DECODE'),
  ('FLUSH', 'DECODE'),
  ('RESET', 'RESET'),
  ('DEFAULT', 'RESET'),
  ('INSTR_FETCH_ERR_PRIO', 'INSTR_FETCH_ERR_PRIO'),
  ('DECODE', 'IRQ_TAKEN'),
  ('DEFAULT', 'DEFAULT'),
  ('FLUSH', 'FLUSH'),
  ('EBRK_INSN_PRIO', 'EBRK_INSN_PRIO'),
  ('ILLEGAL_INSN_PRIO', 'ILLEGAL_INSN_PRIO'),
  ('BOOT_SET', 'FIRST_FETCH')
}



class core_fsm_coverage(uvm_subscriber):

  def __init__(self,name,parent):
    super().__init__(name,parent)

  def build_phase(self):
    self.possible_transitions = POSSIBLE_TRANSITIONS
    self.cvg = set()

  def write(self, FSM_state):
    
    (crr, nxt) = FSM_state.get_touple()
    
    if((crr, nxt) not in self.possible_transitions):
      self.logger.error(f"Illegal transition: {crr} -> {nxt}")
    
    if ((crr, nxt) not in self.cvg):
      self.logger.info(f"New transition: {crr} -> {nxt}")

    self.cvg.add((crr, nxt))



    #print(f"Current state: {crr}, Next state: {nxt}")

  def report_phase(self):
    self.logger.info(f"Coverage: {len(self.cvg)} out of {len(self.possible_transitions)}")
    self.logger.info(f"Coverage percentage: {len(self.cvg) / len(self.possible_transitions) * 100:.2f}%")
    with open('fsm_coverage_report.txt', 'w') as f:
      f.write(f"cve2_fsm: {len(self.cvg) / len(self.possible_transitions) * 100:.2f}%\n")