from cocotb import *
from pyuvm import *
import random
import cocotb
import pyuvm

import sys
from pathlib import Path

from core_driver import core_driver
from core_monitor import core_monitor

class core_agent(uvm_agent):

  def __init__(self, name, parent):
    super().__init__(name, parent)

  def build_phase(self):
    self.core_driver = core_driver.create("core_driver", self)
    self.core_monitor = core_monitor.create("core_monitor", self)


    