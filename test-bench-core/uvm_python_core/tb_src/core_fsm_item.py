from cocotb import *
from pyuvm import *
import cocotb
import pyuvm

'''

  typedef enum logic [3:0] {
    RESET, BOOT_SET, WAIT_SLEEP, SLEEP, FIRST_FETCH, DECODE, FLUSH,
    IRQ_TAEKN, DBG_TAKEN_IF, DBG_TAKEN_ID
  } ctrl_fsm_e;


'''

class core_fsm_item(uvm_sequence_item):
  
  def __init__(self, name):
    super().__init__(name)
    self.current_state = 0
    self.next_state = 0

    self.translation = {
      0: "RESET",
      1: "BOOT_SET",
      2: "WAIT_SLEEP",
      3: "SLEEP",
      4: "FIRST_FETCH",
      5: "DECODE",
      6: "FLUSH",
      7: "IRQ_TAKEN",
      8: "DBG_TAKEN_IF",
      9: "DBG_TAKEN_ID"
    }

  def __eq__(self, other):
    return self.current_state == other.current_state and self.next_state == other.next_state

  def get_touple(self):
    return (self.translation[int(self.current_state)], self.translation[int(self.next_state)])