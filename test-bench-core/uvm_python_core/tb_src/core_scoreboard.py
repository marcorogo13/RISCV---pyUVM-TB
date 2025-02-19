from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm
from pyuvm import ConfigDB
import sys
from pathlib import Path


class core_scoreboard(uvm_component):
  
  def __init__(self, name, parent):
    super().__init__(name, parent)
  
  def build_phase(self):
    self.dut_fifo = uvm_tlm_analysis_fifo("dut_fifo", self)
    self.ref_fifo = uvm_tlm_analysis_fifo("ref_fifo", self)
    self.dut_gp = uvm_get_port("dut_gp", self)
    self.ref_gp = uvm_get_port("ref_gp", self)
    self.dut_export = self.dut_fifo.analysis_export
    self.ref_export = self.ref_fifo.analysis_export


  def connect_phase(self):
    self.dut_gp.connect(self.dut_fifo.get_export)
    self.ref_gp.connect(self.ref_fifo.get_export)



  def check_phase(self):
    
    passed = True

    while self.dut_gp.can_get():
      dut_success, dut_data = self.dut_gp.try_get()
      ref_success, ref_data = self.ref_gp.try_get()

      # need to apply the mask to the from the DUT
      dut_wdata = 0
      for i in range (0,4):# range is 
        temp = 0
        if (int(dut_data.data_be.value)) & (1 << i):
          temp = (int(dut_data.data_wdata.value) >> (8 * i)) & 0xff
        else:
          temp = 0
        dut_wdata = (temp << (8 * i)) | dut_wdata  
          
      if dut_wdata == ref_data.data_wdata and dut_data.data_addr == ref_data.data_addr:

        self.logger.info(f"Scoreboard: check_phase: {passed}")
  
        self.verbose_test = ConfigDB().get(None, "", "VERBOSE_TEST")     
        if self.verbose_test:
          print(f"DUT: {hex(int(dut_wdata))} @{hex(int(dut_data.data_addr))}")
          print(f"REF: {hex(int(ref_data.data_wdata))} @{hex(int(ref_data.data_addr))}")
     
      else:
        passed = False
        self.logger.error(f"Scoreboard: check_phase: {passed}")
        print(f"DUT: {hex(int(dut_wdata))} @{hex(int(dut_data.data_addr))}")
        print(f"REF: {hex(int(ref_data.data_wdata))} @{hex(int(ref_data.data_addr))}")
        print(f"DUT full data: {hex(int(dut_data.data_wdata.value))}")
      assert passed
    

