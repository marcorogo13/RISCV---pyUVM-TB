from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.triggers import Timer
import sys
from pathlib import Path
from core_interface import core_interface
from core_data_item import core_data_item
from core_instr_item import core_instr_item

class core_driver(uvm_driver):

  def __init__(self, name, parent):
    super().__init__(name, parent)

  def build_phase(self):
    self.transport_data = uvm_blocking_transport_port("transport_data", self)
    self.transport_instr = uvm_blocking_transport_port("transport_instr", self)
    self.vif = core_interface()

  async def start_of_simulation_phase(self):
    self.vif.dut.rst_ni.value = 0
    await cocotb.start_soon(self.vif.reset())
    await self.vif.reset()


  async def run_phase(self):
    await self.start_of_simulation_phase()
    cocotb.start_soon(self.drive_data())
    cocotb.start_soon(self.drive_instr())
    await self.drive_data()
    await self.drive_instr()

  async def drive_data(self):
    await self.vif.wait_clock(1)
    while True:
      await self.vif.write_data_interface(data_rvalid=0, data_rdata=None, data_gnt=1)
      

      if await self.vif.read_data_req():
        data_req = core_data_item("data_req")        
        data_req.data_addr, data_req.data_we, data_req.data_wdata, data_req.data_be, _, _ = await self.vif.read_data_interface()
        data_resp = await self.transport_data.transport(data_req)
        if data_req.data_we.value == 0:
          await self.vif.write_data_interface(data_rvalid=1, data_rdata=data_resp.data_rdata, data_gnt=1)
        else:
          await self.vif.write_data_interface(data_rvalid=1, data_rdata=0, data_gnt=1)
      else:
        await self.vif.write_data_interface(data_rvalid=0, data_rdata=None, data_gnt=None)

      await self.vif.wait_clock(1)

  async def drive_instr(self):
    while True:
      await self.vif.write_instr_interface(fetch_enable=1, instr_gnt=1, instr_rvalid=0, instr_rdata=None)
      if await self.vif.read_instr_req():
        await self.vif.write_instr_interface(fetch_enable=1, instr_gnt=1, instr_rvalid=1, instr_rdata=0)
        instr_req = core_instr_item("instr_req")
        instr_resp = core_instr_item("instr_resp")
        instr_req.instr_addr, _, _ = await self.vif.read_instr_interface()
        instr_resp = await self.transport_instr.transport(instr_req)
        await self.vif.write_instr_interface(fetch_enable=1, instr_gnt=1, instr_rvalid=1, instr_rdata=instr_resp.instr_rdata)
      else:
        await self.vif.write_instr_interface(fetch_enable=1, instr_gnt=1, instr_rvalid=0, instr_rdata=None)
      await self.vif.wait_clock(1)
