.section .data
.section .text

.global test_function


test_function:
	# save the return address
	la x2, _stack_start
	addi x2, x2, -4
	sw x1, 0(x2)


	start_label:
	
	# --- test here ---
	SLT x11, x26, x2
	LA x8, _stack_start
	SH x12, 4(x8)
	LA x2, target_jal
	JALR x1, 0(x2)
	XOR x12, x25, x3
	DIV x12, x8, x8
	LA x16, _stack_start
	LB x12, 4(x16)
	LA x8, _stack_start
	LW x12, 4(x8)
	DIV x8, x28, x26
	LA x25, _stack_start
	SH x12, 4(x25)
	LA x8, _stack_start
	SW x12, 4(x8)
	DIVU x8, x8, x8
	LA x8, _stack_start
	SW x11, 4(x8)
	MULH x8, x8, x2
	AND x3, x8, x3
	LA x8, _stack_start
	SW x8, 4(x8)
	SLTU x3, x8, x3
	LA x8, _stack_start
	LH x8, 4(x8)
	LA x10, _stack_start
	SH x12, 4(x10)
	DIVU x12, x10, x8
	SRA x12, x8, x8
	DIVU x12, x8, x8
	MULHSU x8, x8, x8
	LA x8, _stack_start
	SB x18, 4(x8)
	BGEU x8, x2, target_branch34
	ADDI x0, x0, 0
	target_branch34:
	AND x18, x8, x2
	LA x8, _stack_start
	SH x18, 4(x8)
	SRAI x12, x8, 21
	MULH x5, x8, x8
	BEQ x28, x2, target_branch42
	ADDI x0, x0, 0
	target_branch42:
	LA x8, _stack_start
	SB x26, 4(x8)
	AND x18, x8, x3
	BGEU x8, x8, target_branch48
	ADDI x0, x0, 0
	target_branch48:
	MULH x8, x8, x8
	AND x18, x8, x3
	BGE x8, x3, target_branch53
	ADDI x0, x0, 0
	target_branch53:
	SUB x12, x8, x8
	MUL x12, x8, x8
	ADDI x30, x0, 54
	LA x2, target_jal
	JALR x1, 0(x2)
	LA x8, _stack_start
	LW x12, 4(x8)
	LA x2, target_jal
	JALR x1, 0(x2)
	LA x8, _stack_start
	LB x12, 4(x8)
	BGE x8, x2, target_branch67
	target_branch67:
	XORI x19, x8, -676
	BGEU x8, x3, target_branch70
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch70:
	LA x8, _stack_start
	SB x8, 4(x8)
	LA x8, _stack_start
	LW x23, 4(x8)
	LA x8, _stack_start
	SH x21, 4(x8)
	REM x12, x8, x8
	LA x8, _stack_start
	SH x8, 4(x8)
	LA x8, _stack_start
	SW x3, 4(x8)
	REMU x3, x26, x2
	BLT x8, x5, target_branch86
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch86:
	BLT x8, x2, target_branch92
	ADDI x0, x0, 0
	target_branch92:
	LA x8, _stack_start
	SH x3, 4(x8)
	SRAI x3, x8, 24
	LA x8, _stack_start
	SH x3, 4(x8)
	BEQ x8, x2, target_branch100
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch100:
	LA x8, _stack_start
	LW x8, 4(x8)
	SLLI x28, x10, 22
	BLTU x8, x8, target_branch107
	ADDI x0, x0, 0
	target_branch107:
	BGE x1, x8, target_branch110
	ADDI x0, x0, 0
	target_branch110:
	LA x25, _stack_start
	SH x18, 4(x25)
	LA x8, _stack_start
	SW x8, 4(x8)
	LA x8, _stack_start
	SB x18, 4(x8)
	SRLI x12, x8, 4
	LUI x8, 0
	SLL x16, x8, x3
	LA x4, _stack_start
	SW x3, 4(x4)
	AND x3, x28, x2
	BEQ x10, x29, target_branch125
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch125:
	LA x19, _stack_start
	LW x3, 4(x19)
	LA x8, _stack_start
	SH x3, 4(x8)
	LA x8, _stack_start
	LW x3, 4(x8)
	BLT x8, x2, target_branch136
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch136:
	MULHSU x8, x8, x8
	LA x8, _stack_start
	SH x18, 4(x8)
	JAL x1, target_jal
	OR x3, x8, x3
	LA x28, _stack_start
	LH x3, 4(x28)
	LA x28, _stack_start
	SH x3, 4(x28)
	LA x8, _stack_start
	LB x3, 4(x8)
	MULHU x3, x8, x2
	BLTU x19, x3, target_branch154
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch154:
	LA x8, _stack_start
	SB x3, 4(x8)
	ORI x3, x8, -1602
	BLTU x28, x3, target_branch162
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch162:
	BEQ x28, x8, target_branch166
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch166:
	OR x18, x8, x3
	LA x10, _stack_start
	SH x18, 4(x10)
	SLTU x18, x6, x8
	SRL x12, x8, x8
	BNE x16, x8, target_branch177
	ADDI x0, x0, 0
	target_branch177:
	BGEU x9, x3, target_branch180
	ADDI x0, x0, 0
	target_branch180:
	LA x8, _stack_start
	SH x12, 4(x8)
	BLT x16, x8, target_branch185
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch185:
	BNE x16, x8, target_branch191
	ADDI x0, x0, 0
	target_branch191:
	ADDI x8, x8, -1618
	ANDI x18, x21, 896
	BGEU x8, x8, target_branch196
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	ADDI x0, x0, 0
	target_branch196:
	# --- end test ---
	
	end_label:
	nop
	end:
	nop
	# jump to store all registers
	la x2, _stack_start
	addi x2, x2, -4
	la x1, store_registers
	jal x1, store_registers

	# return
	lw x1, 0(x2)
	addi x2, x2, 4
	jr x1

target_jal:
	ret
