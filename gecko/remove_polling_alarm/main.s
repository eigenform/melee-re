.include "../macro.asm"

# (c2) Branch written to 0x801a4da0 (for v1.02)
__start:
	stw r0,	0(r28)
	load r12, 0x800195fc
	mtctr 12

# 0x80019860 4BFFFD9D (relative bl)
	
