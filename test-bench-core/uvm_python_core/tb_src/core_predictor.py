

from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

from core_item import core_item

class core_predictor(uvm_component):
  def __init__(self, name, parent):
    super().__init__(name, parent)

    self.f_pointer= open("mem_write.log","r")


  def build_phase(self): 
     self.ap = uvm_analysis_port("ap", self)

  async def run_phase(self):
    
    for line in self.f_pointer:
      temp_item = core_item("temp_item")
      line = line.split()
      temp_item.data_addr = int(line[0],16)
      temp_item.data_wdata = int(line[1],16)
      #self.logger.info(f"data_addr: {hex(int(temp_item.data_addr))}, data_wdata: {hex(int(temp_item.data_wdata))}")
      self.ap.write(temp_item)
      # self.logger.info(f"Predictor: data_addr: {hex(int(temp_item.data_addr))}, data_wdata: {hex(int(temp_item.data_wdata))}")




    