import sys
import os

def print_usage():
    print(f"Usage: {sys.argv[0]} input_file")
    sys.exit(1)

if len(sys.argv) < 2:
    print_usage()

input_file = sys.argv[1]
output_file = "coverage_report.txt"

# Initialize variables
file_name = ""
total_lines = 0
covered_lines = 0

# Remove output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

def print_coverage():
    if total_lines > 0:
        percentage = (covered_lines / total_lines) * 100
        with open(output_file, 'a') as f:
            f.write(f"{file_name}: {percentage:.2f}%\n")

with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("SF:"):
            if file_name:
                print_coverage()
            # Extract the new file name and reset counters
            file_name = os.path.basename(line[3:]).rsplit('.', 1)[0]
            total_lines = 0
            covered_lines = 0
        elif line.startswith("DA:"):
            total_lines += 1
            count = int(line.split(',')[1])
            if count > 0:
                covered_lines += 1
        elif line == "end_of_record":
            print_coverage()
            file_name = ""
