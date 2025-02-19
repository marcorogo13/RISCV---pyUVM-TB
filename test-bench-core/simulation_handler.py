import os
import subprocess
import shutil
import signal
import glob
import time 

from exceptions import *
from custom_stdout import custom_print

HOME_DIR = os.path.join(os.getcwd(), 'uvm_python_core')
RISCV = os.environ.get('RISCV', '')
VERILATOR = os.environ.get('VERILATOR', '')

os.environ['PATH'] = f"{RISCV}/bin:{os.environ['PATH']}"
os.environ['PATH'] = f"{VERILATOR}/bin:{os.environ['PATH']}"

def run_command(command, cwd=None, tout=3, Shella=True):
  """Run a shell command."""
  try:
    std = subprocess.run( command, 
                          shell=Shella,
                          cwd=cwd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True,
                          timeout=tout
                          )
    
    return (std.stdout, std.stderr)
  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)
  except subprocess.TimeoutExpired as e:
    raise timeout_expired("Timeout expired", e.stdout, e.stderr) from e


def clean():
  """Clean build files."""
  dirs_to_remove = ['build', 'instr_mem.vmem', 'test.dump']
  files_to_remove = ['*.log', 'output.txt']
  
  for d in dirs_to_remove: 
    shutil.rmtree(os.path.join(HOME_DIR, d), ignore_errors=True)
  
  for f in files_to_remove:
    for file in glob.glob(f):
      os.remove(file)
      

def compile_sw_test():
  """Compile the software test."""
  sw_dir = os.path.join(HOME_DIR, '..', 'sw')
  uvm_python_core_dir = os.path.join(HOME_DIR, '..', 'uvm_python_core')
  (stdout, stderr) = run_command('make clean', cwd=sw_dir, Shella=True)
  (stdout, stderr) = run_command('make', cwd=sw_dir, Shella=True)

  if 'Error' in stdout or 'Error' in stderr:
    raise compilation_failed("Error in the compilation", stdout, stderr)

  shutil.copy(os.path.join(sw_dir, 'test.vmem'), os.path.join(uvm_python_core_dir, 'instr_mem.vmem'))
  shutil.copy(os.path.join(sw_dir, 'test.data.vmem'), os.path.join(uvm_python_core_dir, 'data_mem.vmem'))
  run_command('riscv32-unknown-elf-objdump -d test.elf > ../uvm_python_core/test.dump', cwd=sw_dir, Shella=True)
  # get the data dump of the elf
  run_command('riscv32-unknown-elf-objdump -s -j .rodata test.elf > ../uvm_python_core/test_rodata.dump', cwd=sw_dir, Shella=True)
  run_command('riscv32-unknown-elf-objdump -s -j .data test.elf > ../uvm_python_core/test_data.dump', cwd=sw_dir, Shella=True)

def run_spike_and_copy():
  """Run spike and copy test.elf."""
  spike = os.path.join(HOME_DIR, '../../..', 'spike_install/bin', 'spike')
  test_elf = os.path.join(HOME_DIR, '..', 'sw', 'test.elf')

  spike_command = f'exec {spike} -m0xf000:0x1000000,0x00100000:0x4000 --isa=RV32imc -d --log-commits {test_elf} 2> {HOME_DIR}/spike.log'
  parse_command = 'cat spike.log | grep -E "[0-9]+\s+0x[0-9a-f]+\s+\(0x[0-9a-f]+\)\s+mem\s+0x[0-9a-f]+\s+0x[0-9a-f]+" | awk \'{print $5, $6}\'| sed -e \'s/0x//g\'  > mem_write.log'

  try:
    (stdout,stderr) = run_command(spike_command, cwd=HOME_DIR, tout=6)
    (stdout,stderr) = run_command(parse_command, cwd=HOME_DIR, tout=3)

  except subprocess.TimeoutExpired as e: 
    raise spike_timeout_expired("Spike took too long to execute", e.stdout, e.stderr) from e
  
def compile_rtl():
  """Compile the RTL files."""
  print("Compiling RTL files...")
  fusesoc_command = "fusesoc --cores-root ../../ run --no-export --build --target=sim cocotb:tb_only:cve2_core:1.0.0"
  try:
    (stdout, stderr) = run_command(fusesoc_command, cwd=HOME_DIR, tout=99)
  except subprocess.TimeoutExpired as e: raise e
  except Exception as e:
    print(f"Unexpected exception: {e}")
    exit(1)
  

def run_simulation():

  try:
    compile_sw_test()
  except Exception as e:
    print(f"Error in the GCC compilation: {e}")
    handle_test_failed(e, None, "Error in the GCC compilation")
    exit(1)
    

  try:
    run_spike_and_copy()
  except Exception as e: raise e


  try: 
    compile_rtl()
  except Exception as e: raise e


  try:
    print("RTL simulation...")
    fusesoc_command = "fusesoc --cores-root ../../ run --no-export --target=sim cocotb:tb_only:cve2_core:1.0.0"
    (stdout, stderr) = run_command(fusesoc_command, cwd=HOME_DIR, tout=10)
    print(stdout)
  except timeout_expired as e: raise e
  
  try:
    if "FAIL=0" in stdout:
      custom_print("Test Passed", "OKGREEN")
    else:
      print("Test failed")
      raise test_failed("Test Failed", stdout, stderr)
  except test_failed as e: 
    print(stderr)
    print(stdout)
    exit(1)

  
  sim_dir = os.path.join(HOME_DIR, 'build', 'cocotb_tb_only_cve2_core_1.0.0', 'sim')
  coverage_reports_dir = os.path.join(HOME_DIR, 'coverage_reports')


  run_command("verilator_coverage --annotate annotated --write-info coverage.info coverage.dat", cwd=sim_dir)
  shutil.copy(os.path.join(sim_dir, 'coverage.info'), os.path.join(coverage_reports_dir, 'coverage.info'))
  shutil.copy(os.path.join(sim_dir, 'fsm_coverage_report.txt'), os.path.join(coverage_reports_dir, 'fsm_coverage_report.txt'))
  shutil.copy(os.path.join(sim_dir, 'func_coverage_report.txt'), os.path.join(coverage_reports_dir, 'func_coverage_report.txt'))

  coverage_reports_dir = os.path.join(HOME_DIR, 'coverage_reports')
  run_command('python3 ../scripts/parse_coverage.py coverage.info', cwd=coverage_reports_dir)
  with open(os.path.join(coverage_reports_dir, 'coverage_report.txt'), 'a') as coverage_report:
    with open(os.path.join(coverage_reports_dir, 'fsm_coverage_report.txt'), 'r') as fsm_report:
      coverage_report.write(fsm_report.read())
    with open(os.path.join(coverage_reports_dir, 'func_coverage_report.txt'), 'r') as func_report:
      coverage_report.write(func_report.read())
  
  

  with open(os.path.join(coverage_reports_dir, 'coverage_report.txt'), 'r') as coverage_report:
    print(coverage_report.read())
  
  command_dir = os.path.join(HOME_DIR, "coverage_reports") 
  command = "python3 avg_cov.py"
  stdout, stderr = run_command(command, cwd=command_dir, tout=3)
  print(stdout)

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description='Run the simulation')
  parser.add_argument('task', choices=['compile_sw_test', 'run_spike_and_copy', 'run_simulation', 'clean'], help='Task to run')
  args = parser.parse_args()
  if args.task == 'run_simulation':
    run_simulation()
  elif args.task == 'compile_sw_test':
    compile_sw_test()
  elif args.task == 'run_spike_and_copy':
    run_spike_and_copy()
  elif args.task == 'clean':
    clean()
