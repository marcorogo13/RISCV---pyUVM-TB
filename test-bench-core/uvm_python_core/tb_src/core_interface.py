from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
import sys
from pathlib import Path


  # signals of the CORE dut:
  # // Clock and Reset
  #   logic                         clk_i;
  #   logic                         rst_ni;

  #   logic                         test_en_i;

  #   logic [31:0]                  hart_id_i;
  #   logic [31:0]                  boot_addr_i;
    
  #    // Instruction memory interface
  #   logic                         instr_req_o;
  #   logic                         instr_gnt_i;
  #   logic                         instr_rvalid_i;
  #   logic [31:0]                  instr_addr_o;
  #   logic [31:0]                  instr_rdata_i;
  #   logic                         instr_err_i;

  #   // Data memory interface
  #   logic                         data_req_o;
  #   logic                         data_gnt_i;
  #   logic                         data_rvalid_i;
  #   logic                         data_we_o;
  #   logic [3:0]                   data_be_o;
  #   logic [31:0]                  data_addr_o;
  #   logic [31:0]                  data_wdata_o;
  #   logic [31:0]                  data_rdata_i;
  #   logic                         data_err_i;

  #   // Interrupt inputs
  #   logic                         irq_software_i;
  #   logic                         irq_timer_i;
  #   logic                         irq_external_i;
  #   logic [15:0]                  irq_fast_i;
  #   logic                         irq_nm_i;       // non-maskeable interrupt
  #   logic                         irq_pending_o;

  #   // Debug Interface
  #   logic                         debug_req_i;
  #   crash_dump_t                  crash_dump_o;

  #   // CPU Control Signals
  #   logic                         fetch_enable_i;
  #   logic                         core_busy_o;


class core_interface(metaclass=utility_classes.Singleton): # Singleton class, only one instance of this class is allowed

  def __init__(self):
    self.dut = cocotb.top


  async def wait_clock(self, cycles=1):
    for _ in range(cycles):
      await RisingEdge(self.dut.clk_i)
  

  async def read_data_req(self):
    return self.dut.data_req_o.value
  
  async def read_data_we(self):
    return self.dut.data_we_o.value

  async def read_data_addr(self):
    return self.dut.data_addr_o.value
  
  async def read_data_wdata(self):
    return self.dut.data_wdata_o.value

  async def read_data_interface(self):
    return self.dut.data_addr_o.value, self.dut.data_we_o.value, \
          self.dut.data_wdata_o.value, self.dut.data_be_o.value, \
          self.dut.data_rvalid_i.value, self.dut.data_req_o.value
          

  async def write_data_interface(self, data_rvalid, data_gnt, data_rdata):
    if data_rvalid is not None:
      self.dut.data_rvalid_i.value = data_rvalid
    if data_gnt is not None:
      self.dut.data_gnt_i.value = data_gnt
    if data_rdata is not None:
      self.dut.data_rdata_i.value = data_rdata


  async def read_instr_req(self):
    return self.dut.instr_req_o.value

  async def read_instr_interface(self):
    return self.dut.instr_addr_o.value, self.dut.instr_req_o.value, \
          self.dut.instr_rdata_i.value

  async def write_instr_interface(self, fetch_enable, instr_gnt, instr_rvalid, instr_rdata):
    if fetch_enable is not None:
      self.dut.fetch_enable_i.value = fetch_enable
    if instr_gnt is not None:
      self.dut.instr_gnt_i.value = instr_gnt
    if instr_rvalid is not None:
      self.dut.instr_rvalid_i.value = instr_rvalid
    if instr_rdata is not None:
      self.dut.instr_rdata_i.value = instr_rdata


  async def read_rvfi_insn(self):
    return self.dut.rvfi_insn.value

  async def read_reset(self):
    return self.dut.rst_ni.value

  async def read_ctrl_fsm_cs(self):
    return self.dut.id_stage_i.controller_i.ctrl_fsm_cs.value
  
  async def read_ctrl_fsm_ns(self):
    return self.dut.id_stage_i.controller_i.ctrl_fsm_ns.value
    
  async def reset(self):
    self.dut.rst_ni.value = 0
    self.dut.fetch_enable_i.value = 0
    self.dut.instr_rvalid_i.value = 0
    self.dut.instr_rdata_i.value = 0
    self.dut.instr_gnt_i.value = 0
    self.dut.test_en_i.value = 0
    self.dut.hart_id_i.value = 0
    self.dut.boot_addr_i.value = 0x00100000
    self.dut.irq_software_i.value = 0
    self.dut.irq_timer_i.value = 0
    self.dut.irq_external_i.value = 0
    self.dut.irq_fast_i.value = 0
    self.dut.irq_nm_i.value = 0
    self.dut.debug_req_i.value = 0
    self.dut.instr_err_i.value = 0
    self.dut.data_err_i.value = 0
    self.dut.data_rvalid_i.value = 0
    self.dut.data_rdata_i.value = 0
    self.dut.data_gnt_i.value = 0
    await self.wait_clock(10)
    self.dut.rst_ni.value = 1

  