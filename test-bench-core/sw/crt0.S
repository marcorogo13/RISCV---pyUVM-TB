.section .data
.align 4
dummy_data:
    .word 0x42

.section .text
_start:
    # initialize all registers to 0
    addi x1, x0, 0
    addi x2, x0, 0
    addi x3, x0, 0
    addi x4, x0, 0
    addi x5, x0, 0
    addi x6, x0, 0
    addi x7, x0, 0
    addi x8, x0, 0
    addi x9, x0, 0
    addi x10, x0, 0
    addi x11, x0, 0
    addi x12, x0, 0
    addi x13, x0, 0
    addi x14, x0, 0
    addi x15, x0, 0
    addi x16, x0, 0
    addi x17, x0, 0
    addi x18, x0, 0
    addi x19, x0, 0
    addi x20, x0, 0
    addi x21, x0, 0
    addi x22, x0, 0
    addi x23, x0, 0
    addi x24, x0, 0
    addi x25, x0, 0
    addi x26, x0, 0
    addi x27, x0, 0
    addi x28, x0, 0
    addi x29, x0, 0
    addi x30, x0, 0
    addi x31, x0, 0


    # set in vector mode
    li t0, 0x00000000
    csrw mstatus, t0

    
    # set mtvec to trap_handler
    li t2, 0x100100
    csrw mtvec, t2 

    # jump to test function 
    la x2, _stack_start


    jal x1, test_function

simulation_end:
    # end simulation
    li x5, 0x20008
    li x6, 1
    sw x6, 0(x5)
		nop
		nop
halt:
    j halt
    nop
    nop
    nop


trap_handler:
    jal x1, store_registers
    jal simulation_end


.section .vectors, "ax"
.option norvc

.org 0x00 
    j _start
.org 0x100
    .rept 15
    j trap_handler
    .endr

