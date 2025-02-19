from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

import sys
from pathlib import Path

# item used to interact with the instr memory model from the driver

class core_instr_item(uvm_sequence_item):
  def __init__(self, name):
    super().__init__(name)
    self.instr_req = 0
    self.instr_gnt = 0
    self.instr_rvalid = 0
    self.instr_addr = 0
    self.instr_rdata = 0
    self.instr_err = 0

  def __eq__(self, other):
    same = self.instr_addr == other.instr_addr and self.instr_rdata == other.instr_rdata
  
