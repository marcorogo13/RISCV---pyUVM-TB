from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm
from pyuvm import ConfigDB
from cocotb.clock import Clock
from cocotb.triggers import Timer
import os


from core_env import core_env
from core_data_model import core_data_model
from core_instr_model import core_instr_model
from core_interface import core_interface

@pyuvm.test()
class core_test(uvm_test):

  def __init__(self, name, parent):
    super().__init__(name, parent)



  def build_phase(self):

    if "VERBOSE_TEST" in os.environ:
      self.verbose = int(os.environ["VERBOSE_TEST"])
    else:
      self.verbose = 0
    # self.verbose = 1
    ConfigDB().set(None, "*", "VERBOSE_TEST", self.verbose)

    self.core_env = core_env("core_env", self)
    self.core_data_model = core_data_model("core_data_model", self)
    self.core_instr_model = core_instr_model("core_instr_model", self)
    self.vif = core_interface()
    

    
  def connect_phase(self):
    self.core_env.core_agent.core_driver.transport_data.connect(self.core_data_model.data_export)
    self.core_env.core_agent.core_driver.transport_instr.connect(self.core_instr_model.instr_export)

  async def run_phase(self):
    # wait for enough time to coplete the test
    clock = Clock(cocotb.top.clk_i, 1, units="NS")
    cocotb.start_soon(clock.start())



   
