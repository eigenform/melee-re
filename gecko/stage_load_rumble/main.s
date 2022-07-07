
.include "../macro.asm"

# This should occur right after StartMelee() returns:
#	- 0x8016e94c for NTSC v1.02
#	- 0x8016df44 for NTSC v1.00
 
__start:
	li r3, 0    # Port number (starting with 0)
	li r4, 0x18 # ???
	li r5, 0x16 # ???
	li r6, 0    # ???
	branchl r7, lbRumble_ExecuteControllerRumble

	# Clobbered instruction
	lbz r0, 0x1(r31)

