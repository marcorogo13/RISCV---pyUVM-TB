from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

import sys
from pathlib import Path



class core_item(uvm_sequence_item):

  def __init__(self, name):
    super().__init__(name)
    self.instr_req = 0
    self.instr_gnt = 0
    self.instr_rvalid = 0
    self.instr_addr = 0
    self.instr_rdata = 0
    self.instr_err = 0
    self.data_req = 0
    self.data_gnt = 0
    self.data_rvalid = 0
    self.data_we = 0
    self.data_be = 0
    self.data_addr = 0
    self.data_wdata = 0
    self.data_rdata = 0
    self.data_err = 0
    self.irq_software = 0
    self.irq_timer = 0
    self.irq_external = 0
    self.irq_fast = 0
    self.irq_nm = 0
    self.irq_pending = 0
    self.debug_req = 0
    self.fetch_enable = 0
    self.core_busy = 0
  