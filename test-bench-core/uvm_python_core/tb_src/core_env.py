from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

import sys
from pathlib import Path

from core_agent import core_agent
from core_scoreboard import core_scoreboard
from core_predictor import core_predictor
from core_fsm_coverage import core_fsm_coverage
from core_func_coverage import core_func_coverage

class core_env(uvm_env):

  def __init__(self, name, parent):
    super().__init__(name, parent)
  
  def build_phase(self):
    self.core_agent = core_agent.create("core_agent", self)
    self.core_scoreboard = core_scoreboard.create("core_scoreboard", self)
    self.core_predictor = core_predictor.create("core_predictor", self)
    self.core_fsm_coverage = core_fsm_coverage.create("core_fsm_coverage", self)
    self.core_func_coverage = core_func_coverage.create("core_func_coverage", self)
  
  def connect_phase(self):
    self.core_agent.core_monitor.ap.connect(self.core_scoreboard.dut_export)
    self.core_predictor.ap.connect(self.core_scoreboard.ref_export) 
    self.core_agent.core_monitor.ap_fsm_cov.connect(self.core_fsm_coverage.analysis_export)
    self.core_agent.core_monitor.ap_func_cov.connect(self.core_func_coverage.analysis_export)