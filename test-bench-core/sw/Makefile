# Compiler and tools
CC = /software/x-heep/riscv-ubuntu/bin/riscv32-unknown-elf-gcc
CROSS_COMPILE = $(patsubst %-gcc,%-,$(CC))
OBJCOPY ?= $(CROSS_COMPILE)objcopy
OBJDUMP ?= $(CROSS_COMPILE)objdump

# Directories and files
COMMON_DIR := .
LINKER_SCRIPT_CRT0 ?= $(COMMON_DIR)/link_crt0.ld

# Source files
CRT ?= $(COMMON_DIR)/crt0.S
TEST ?= $(COMMON_DIR)/test_function.S
STORE ?= $(COMMON_DIR)/store_registers.S
SORT ?= $(COMMON_DIR)/sort.c
TEST_C := $(COMMON_DIR)/test.c

# Compiler flags
ARCH ?= rv32imc
CFLAGS ?= -march=$(ARCH) -mabi=ilp32 -static -mcmodel=medany -Wall -g -Os -O0\
          -fvisibility=hidden -nostdlib -nostartfiles -ffreestanding

# Object files
OBJS_TEST := $(CRT:.S=.o) $(TEST:.S=.o) $(STORE:.S=.o) $(SORT:.c=.o) $(TEST_C:.c=.o)
# Output files
OUTFILES := test.elf test.vmem test.bin test.data.vmem

all: $(OUTFILES)

test.elf: $(OBJS_TEST) $(LINKER_SCRIPT_CRT0)
	$(CC) $(CFLAGS) -T $(LINKER_SCRIPT_CRT0) $(OBJS_TEST) -o $@ $(LIBS)

%.dis: %.elf
	$(OBJDUMP) -fhSD $^ > $@

%.vmem: %.bin
	$(OBJCOPY) --reverse-bytes=4 --verilog-data-width=4 -I binary -O verilog $^ $@
	# change the first line of the output file with @00100000
	sed -i '1s/^.*$$/@00100000/' $@

%.data.vmem: %.elf
	# Dump the .data and .rodata sections to separate binary files
	$(OBJCOPY) --dump-section .data=$(@:.data.vmem=.data.bin) $^
	$(OBJCOPY) --dump-section .rodata=$(@:.data.vmem=.rodata.bin) $^

	# Concatenate the .data and .rodata binary files
	cat $(@:.data.vmem=.rodata.bin) >> $(@:.data.vmem=.data.bin)

	# Convert the combined binary file to a Verilog memory file
	$(OBJCOPY) --reverse-bytes=4 --verilog-data-width=4 -I binary -O verilog $(@:.data.vmem=.data.bin) $@
	
	# Clean up the temporary binary files
	rm -f $(@:.data.vmem=.data.bin) $(@:.data.vmem=.rodata.bin)
	
	# Change the first line of the output file to start with @00140000
	sed -i '1s/^.*$$/@00140000/' $@
	
%.bin: %.elf
	$(OBJCOPY) -O binary $^ $@

%.o: %.c
	$(CC) $(CFLAGS) -MMD -c -o $@ $<

%.o: %.S
	$(CC) $(CFLAGS) -MMD -c -o $@ $<

clean:
	$(RM) -f $(OBJS_TEST) *.d

distclean: clean
	$(RM) -f $(OUTFILES)
