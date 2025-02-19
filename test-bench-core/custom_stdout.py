class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'



def custom_print(message, color):
  # print the message in the color specified using the bcolor 
  print(f"{bcolors.__dict__[color]}{message}{bcolors.ENDC}")