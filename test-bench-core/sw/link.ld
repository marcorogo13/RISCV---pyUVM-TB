/* Copyright lowRISC contributors.
   Licensed under the Apache License, Version 2.0, see LICENSE for details.
   SPDX-License-Identifier: Apache-2.0 */

OUTPUT_ARCH(riscv)

MEMORY
{
/* Change this if you'd like different sizes. Arty A7-100(35) has a maximum of 607.5KB(225KB)
   BRAM space. Configuration below is for maximum BRAM capacity with Artya A7-35 while letting
   CoreMark run (.vmem of 152.8KB).
*/
    ram         : ORIGIN = 0x00100000, LENGTH = 0x30000 /* 192 kB */
    stack       : ORIGIN = 0x00130000, LENGTH = 0x8000  /* 32 kB */
}

/* Stack information variables */
_min_stack      = 0x2000;   /* 8K - minimum stack space to reserve */
_stack_len     = LENGTH(stack);
_stack_start   = ORIGIN(stack) + LENGTH(stack);


_entry_point = _vectors_start + 0x00;
ENTRY(_entry_point)

/*spike*/
tohost   = 0x20008;
fromhost = 0x00000;

SECTIONS 
{
    .vectors :
    {
        . = ALIGN(4);
		_vectors_start = .;
        KEEP(*(.vectors))
		_vectors_end = .;
    } > ram

    .text : {
        . = ALIGN(4);
        crt0.o(.text)
        main/main.o(.text)
        //*(.text)
        //*(.text.*)
    }  > ram

    .rodata : {
        . = ALIGN(4);
        /* Small RO data before large RO data */
        *(.srodata)
        *(.srodata.*)
        *(.rodata);
        *(.rodata.*)
    } > ram

    .data : {
        . = ALIGN(4);
        /* Small data before large data */
        *(.sdata)
        *(.sdata.*)
        *(.data);
        *(.data.*)
    } > ram

    .bss :
    {
        . = ALIGN(4);
        _bss_start = .;
        /* Small BSS before large BSS */
        *(.sbss)
        *(.sbss.*)
        *(.bss)
        *(.bss.*)
        *(COMMON)
        _bss_end = .;
    } > ram

    /* ensure there is enough room for stack */
    .stack (NOLOAD): {
        . = ALIGN(4);
        . = . + _min_stack ;
        . = ALIGN(4);
        stack = . ;
        _stack = . ;
    } > stack
    
}
