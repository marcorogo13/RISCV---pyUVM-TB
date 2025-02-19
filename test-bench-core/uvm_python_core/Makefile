

export HOME_DIR := $(shell pwd)

export PATH := $(RISCV)/bin:$(PATH)
export PATH := $(VERILATOR)/bin:$(PATH)


print_riscv:
	@echo $(RISCV)
	@echo $(PATH)

.PHONY: compile_sw_test
compile_sw_test: 
	cd ../sw && \
	make clean && \
	make && \
	cp test.vmem ../uvm_python_core/instr_mem.vmem && \
	riscv32-unknown-elf-objdump -d test.elf > ../uvm_python_core/test.dump

.PHONY: run_spike_and_copy
run_spike_and_copy: compile_sw_test
	$(HOME_DIR)/../../../spike_install/bin/spike -m0xf000:0x1000000,0x00100000:0x4000 --isa=RV32imc -d --log-commits $(HOME_DIR)/../sw/test.elf 2> spike.log
	cat spike.log | grep -E "[0-9]+\s+0x[0-9a-f]+\s+\(0x[0-9a-f]+\)\s+mem\s+0x[0-9a-f]+\s+0x[0-9a-f]+" | awk '{print $$5, $$6}'| sed -e 's/0x//g'  > mem_write.log
	# $(HOME_DIR)/....//spike/spike.sh $(HOME_DIR)/../sw/test.elf


.PHONY: run_sim
run_sim: compile_sw_test run_spike_and_copy
	fusesoc --cores-root ../../ run --no-export --target=sim cocotb:tb_only:cve2_core:1.0.0

	cd build/cocotb_tb_only_cve2_core_1.0.0/sim && \
	verilator_coverage --annotate annotated --write-info coverage.info coverage.dat && \
	cp coverage.info ../../../coverage_reports/coverage.info && \
	cp fsm_coverage_report.txt ../../../coverage_reports/fsm_coverage_report.txt && \
	cp func_coverage_report.txt ../../../coverage_reports/func_coverage_report.txt


.PHONY: coverage_sim
coverage_sim: run_sim
	cd coverage_reports && \
	python3 ../scripts/parse_coverage.py coverage.info && \
	cat fsm_coverage_report.txt >> coverage_report.txt && \
	cat func_coverage_report.txt >> coverage_report.txt && \
	python3 avg_cov.py > avg_cov.txt

.PHONY: clean
clean: 
	rm -rf build
	rm -rf instr_mem.vmem
	rm -rf test.dump
	rm -rf *.log
	rm -rf output.txt