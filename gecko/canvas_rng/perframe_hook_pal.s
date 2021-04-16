
.include "../macro.asm"

# This is just from looking at scene_change.elf objdump.
# There's probably a cleaner (safer) solution, but this works too.
.set PerFrame, 0x80196edc

_start:
	branchl	r11, PerFrame
	
