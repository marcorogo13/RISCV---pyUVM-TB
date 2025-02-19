from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

from core_data_item import core_data_item

class core_data_model(uvm_component):
  # mem array is a dictionary with key as address and value as data
  global DataWidth

  ### class for the transport import
  class uvm_blocking_transport_import(uvm_blocking_transport_export):
    def __init__(self, name, parent, transport_fn):
      super().__init__(name, parent)
      self.transport_fn = transport_fn

    async def transport(self, t):
      s = await self.transport_fn(t)
      return s
  ##############################################################################

  def __init__(self, name, parent):
    super().__init__(name, parent)
    self.memory = {}

    self.DataWidth = 32

  def build_phase(self):
    self.data_export = self.uvm_blocking_transport_import("data_export", self, self.transport)
    with open("instr_mem.vmem", "r") as f:
      for line in f:
        if line[0] == "@":
          # the format is @<hex value of base_address>

          base_addr = line.split()[0][1:]
          base_addr = int(base_addr, 16)

          # print(f"Base address: {hex(int(base_addr))}") 
        else:
          for word in line.split():
            self.memory[base_addr] = int(word, 16)
            base_addr += 4

  async def transport(self, data_req):
    s = core_data_item("s")
    data_address = int(data_req.data_addr.value)
    data_bytenable = int(data_req.data_be.value)
    data_writedata = int(data_req.data_wdata.value)
    data_readdata = 0

    self.verbose_test = ConfigDB().get(None, "", "VERBOSE_TEST")

    if data_req.data_we.value == 1:
      for i in range(0, int(self.DataWidth / 8)):
        if data_bytenable & (1 << i):
          wdata = (data_writedata >> (8 * i)) & 0xff
          self.memory[data_address + i] = wdata
        else:
          # Preserve existing data in memory for bytes that are not enabled
          if data_address + i in self.memory:
              wdata = self.memory[data_address + i]
          else:
              wdata = 0

    else:
      # Read operation
      for i in range(0, int(self.DataWidth / 8)):
        if data_address + i in self.memory:
          data_readdata |= (self.memory[data_address + i] << (8 * i))
        else:
          data_readdata |= (0 << (8 * i))  # Assuming zero for uninitialized memory

    if self.verbose_test:
      self.logger.info(f"Data request: data we: {data_req.data_we.value} address: {hex(data_address)}, bytenable: {hex(data_bytenable)}, writedata: {hex(data_writedata)}, readdata: {hex(data_readdata)}")

    s.data_rdata = data_readdata
    return s
  
  def check_phase(self):
    # Print the memory content
    with open("data_content.txt", "w") as f:
      for addr in self.memory:
        f.write(f"{hex(addr)}: {hex(self.memory[addr])}\n")

