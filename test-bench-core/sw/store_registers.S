.section .data
.section .text
.align 4
.global store_registers
store_registers:
 # load the stack pointer
	

	# store all the registers to compare with the expected values
	sw x1, 0x004(x2)
	sw x2, 0x008(x2)
	sw x3, 0x00c(x2)
	sw x4, 0x010(x2)
	sw x5, 0x014(x2)
	sw x6, 0x018(x2)
	sw x7, 0x01c(x2)
	sw x8, 0x020(x2)
	sw x9, 0x024(x2)
	sw x10, 0x028(x2)
	sw x11, 0x02c(x2)
	sw x12, 0x030(x2)
	sw x13, 0x034(x2)
	sw x14, 0x038(x2)
	sw x15, 0x03c(x2)
	sw x16, 0x040(x2)
	sw x17, 0x044(x2)
	sw x18, 0x048(x2)
	sw x19, 0x04c(x2)
	sw x20, 0x050(x2)
	sw x21, 0x054(x2)
	sw x22, 0x058(x2)
	sw x23, 0x05c(x2)
	sw x24, 0x060(x2)
	sw x25, 0x064(x2)
	sw x26, 0x068(x2)
	sw x27, 0x06c(x2)
	sw x28, 0x070(x2)
	sw x29, 0x074(x2)	
	sw x30, 0x078(x2)
	sw x31, 0x07c(x2)

	# store the PC 
	auipc   t0, 0
	sw t0, 0x080(x2)

	ret
	nop