.include "../macro.asm"

# PAL hook at 0x801a5798.

# We're writing over this tournament mode function
.set OnSceneChange, 0x80196dd4

__start:
	stw	r3, -0x4d34(r13)
	branchl r12, OnSceneChange
