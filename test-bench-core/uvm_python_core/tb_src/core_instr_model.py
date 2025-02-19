from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

import sys
from pathlib import Path
from core_instr_item import core_instr_item
#import bincopy

class core_instr_model(uvm_component):

  

### class for the transport import
  class uvm_blocking_transport_import(uvm_blocking_transport_export):
    def __init__(self, name, parent, transport_fn):
      super().__init__(name, parent)
      self.transport_fn = transport_fn

    async def transport(self, t):
      s = await self.transport_fn(t)
      return s
##############################################################################


  def build_phase(self):
    self.instr_export = self.uvm_blocking_transport_import("instr_export", self, self.transport)
    self.boot_addr = 0x00100080
    self.instr_mem = {}
    with open("instr_mem.vmem", "r") as f:
      for line in f:
        if line[0] == "@":
          # the format is @<hex value of base_address>

          base_addr = line.split()[0][1:]
          base_addr = int(base_addr, 16)

          # print(f"Base address: {hex(int(base_addr))}") 
        else:
          for word in line.split():
            self.instr_mem[base_addr] = int(word, 16)
            base_addr += 4

    # print the mem content to check
    # for addr in self.instr_mem:
    #   print(f"{hex(int(addr))}: {hex(int(self.instr_mem[addr]))}")

  
  async def transport (self, instr_req):
    instr_resp = core_instr_item("instr_resp")
    instruction_address = instr_req.instr_addr
    # actual_address = int(instruction_address) - self.boot_addr >> 2


    if ((int(instruction_address))) in self.instr_mem:
      actual_address = int(instruction_address)
      #self.logger.info(f"Actual address: {hex(int(actual_address))}")
      instr_resp.instr_rdata = self.instr_mem[actual_address]
      instr_resp.instr_addr = instr_req.instr_addr
      # self.logger.info(f"Instruction address {hex(int(instruction_address))} found in memory with data {hex(int(instr_resp.instr_rdata))}")
    else:
      self.logger.error(f"Instruction address {hex(int(instruction_address))} not found in memory")
      instr_resp.instr_rdata = 0
      instr_resp.instr_addr = instr_req.instr_addr
      

    return instr_resp
