from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

import sys
from pathlib import Path

# item used to interact with the memory model from the driver

class core_data_item(uvm_sequence_item):

  def __init__(self, name):
    super().__init__(name)
    self.data_req = 0
    self.data_gnt = 0
    self.data_rvalid = 0
    self.data_we = 0
    self.data_be = 0
    self.data_addr = 0
    self.data_wdata = 0
    self.data_rdata = 0
    self.data_err = 0

  def __eq__(self, other):
    same = self.data_addr == other.data_addr and self.data_rdata == other.data_rdata