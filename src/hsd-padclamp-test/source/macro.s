.macro __clear_vgprs
	li r0, 0
	li r3, 0
	li r4, 0
	li r5, 0
	li r7, 0
	li r7, 0
	li r8, 0
	li r9, 0
	li r10, 0
	li r11, 0
	li r12, 0
.endm

.macro load reg, address
lis \reg, \address @h
ori \reg, \reg, \address @l
.endm

