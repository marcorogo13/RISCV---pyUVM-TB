from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm
from pyuvm import ConfigDB
from cocotb.triggers import RisingEdge, FallingEdge

import sys
from pathlib import Path

from core_interface import core_interface
from core_item import core_item
from core_fsm_item import core_fsm_item

class core_monitor(uvm_component):
  def __init__(self, name, parent):
    super().__init__(name, parent)



  def build_phase(self):
    self.vif = core_interface()
    self.ap = uvm_analysis_port("ap", self)
    self.ap_fsm_cov = uvm_analysis_port("ap_cov", self)
    self.ap_func_cov = uvm_analysis_port("ap_func_cov", self)
    self.verbose_test = ConfigDB().get(None, "", "VERBOSE_TEST") 

  async def run_phase(self):
    self.raise_objection()
    
    await self.vif.wait_clock(1)
    while True:
      await self.vif.wait_clock(1)
      if self.verbose_test:
        self.logger.info(
          f"instr_req: {self.vif.dut.instr_req_o.value}, instr_addr: {hex(int(self.vif.dut.instr_addr_o))}, instr_rdata: {hex(int(self.vif.dut.instr_rdata_i))} \n" +
          f"data_req: {self.vif.dut.data_req_o.value}, data_addr: {hex(int(self.vif.dut.data_addr_o))}, data_wdata: {hex(int(self.vif.dut.data_wdata_o))}, data_be: {hex(int(self.vif.dut.data_be_o))}, data_rvalid: {self.vif.dut.data_rvalid_i.value}\n"
        )
      
      if await self.vif.read_reset():     
        fsm_itm = core_fsm_item("fsm_itm")
        fsm_itm.current_state = await self.vif.read_ctrl_fsm_cs()
        fsm_itm.next_state =  await self.vif.read_ctrl_fsm_ns()
        self.ap_fsm_cov.write(fsm_itm)

        decode_instruction = await self.vif.read_rvfi_insn()
        self.ap_func_cov.write(decode_instruction)

        if await self.vif.read_data_req() and await self.vif.read_data_we():
          seq = core_item("seq")
          seq.data_addr, seq.data_we, seq.data_wdata, seq.data_be, seq.data_rvalid, seq.data_req = await self.vif.read_data_interface()
          seq.instr_addr, seq.instr_req, seq.instr_rdata = await self.vif.read_instr_interface()
          self.ap.write(seq)

          if await self.vif.read_data_addr() == 0x20008 and await self.vif.read_data_wdata() == 1:
            self.logger.info(f"Simulation stopped as the data write to address 0x20008 with value 1")
            self.drop_objection()
            break

        


      