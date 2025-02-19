from custom_stdout import custom_print


# log files 

ERROR_LOG = "error.log"


def clean_log_files():
  open(ERROR_LOG, "w").close()
  





# exception classes

class missing_file(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
      
class spike_timeout_expired(Exception):
  def __init__(self, message, stdout_output, stderr_output):
    self.message = message
    self.stdout_output = stdout_output
    self.stderr_output = stderr_output
    super().__init__(self.message)

class test_failed(Exception):
  def __init__(self, message, stdout_output, stderr_output):
    self.message = message
    self.stderr_output = stderr_output
    self.stdout_output = stdout_output
    super().__init__(self.message)

class none_instruction(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)

class timeout_expired(Exception):
  def __init__(self, message, stdout_output, stderr_output):
    self.message = message
    self.stdout_output = stdout_output
    self.stderr_output = stderr_output
    super().__init__(self.message)

class invalid_instruction(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)

class compilation_failed(Exception):
  def __init__(self, message, stdout_output, stderr_output):
    self.message = message
    self.stdout_output = stdout_output
    self.stderr_output = stderr_output
    super().__init__(self.message)

class verilator_failed(Exception):
  def __init__(self, message, stdout_output, stderr_output):
    self.message = message
    self.stdout_output = stdout_output
    self.stderr_output = stderr_output
    super().__init__(self.message)


# handler functions

def handle_test_failed(exc, action, text = "TEST FAILED"):
  custom_print(f"{exc.message}", "FAIL")
  with open(ERROR_LOG, "a") as error_file:
    error_file.write(f"{text}\n")
    error_file.write("STDOUT\n")
    error_file.write(exc.stdout_output)
    error_file.write("\n\n\nSTDERR\n")
    error_file.write(exc.stderr_output)
    error_file.write("\n\n\n")
    error_file.write("ACTION\n")
    if type(action) == list:
      for instr in action:
          error_file.write(f"{instr}\n")
    else:
      error_file.write(f"{action}\n")
    error_file.write("\n\n\n")
  

def handle_timeout_expired(exc, action):
    custom_print(f"{exc.message}", "FAIL")
    with open(ERROR_LOG, "a") as error_file:
        error_file.write("TIMEOUT\n")
        error_file.write("STDOUT\n")
        if stdout_string is not None:
          stdout_string = exc.stdout_output.decode("utf-8")
        else:
          stdout_string = "None"
        error_file.write(stdout_string)
        error_file.write("\n\n\nSTDERR\n")
        if stderr_string is not None:
          stderr_string = exc.stderr_output.decode("utf-8")
        else:
          stderr_string = "None"
        error_file.write(stderr_string)
        error_file.write("\n\n\n")
        error_file.write("ACTION\n")
        if type(action) == list:
           for instr in action:
               error_file.write(f"{instr}\n")
        else:
            error_file.write(f"{action}\n")
        error_file.write("\n\n\n")

