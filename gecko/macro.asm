# Global macros
# These macros are pulled from `project-slippi/slippi-ssbm-asm`.
# I would not be surprised if UnclePunch is the author.

# Use CTR to branch (updating the LR) to some address
.macro branchl reg, address
lis \reg, \address @h
ori \reg,\reg,\address @l
mtctr \reg
bctrl
.endm

# Use the CTR to branch to some address
.macro branch reg, address
lis \reg, \address @h
ori \reg,\reg,\address @l
mtctr \reg
bctr
.endm

# Easy way to write a whole address into some register
.macro load reg, address
lis \reg, \address @h
ori \reg, \reg, \address @l
.endm

# Simple way to load the address of some local symbol whose 
# address must be resolved at runtime
.macro load_rt reg, symbol
	bl \symbol
	mflr \reg
.endm

# Backup GPRs
.macro backup
mflr r0
stw r0, 0x4(r1)
stwu r1,-0xB0(r1)
stmw r20,0x8(r1)
.endm

# Restore GPRs
 .macro restore
lmw r20,0x8(r1)
lwz r0, 0xB4(r1)
addi r1,r1,0xB0
mtlr r0
.endm

.if BUILD_NTSC_100 == 1
	.set GLOBAL_P1CURSOR_PTR, 0x8049ea88
	.set GLOBAL_TEXTDATA_PTR, 0x804d4c98
	.set DevelopMode_Text_Erase, 0x80301314
	.set DevelopMode_Text_ResetCursor, 0x803011a0
	.set DevelopMode_Text_Display, 0x803014b0
	.set _HSD_MemAlloc, 0x8037d330
	.set TextData_Create, 0x80300f98 
	.set TextData_Init, 0x80300f74
	.set TextData_Unhide, 0x80301214
	.set TextData_SetBackgroundColor, 0x803012f4 
.endif

.if BUILD_NTSC_102 == 1
	.set GLOBAL_P1CURSOR_PTR, 0x804a0bc0 
	.set GLOBAL_TEXTDATA_PTR, 0x804d6e18
	.set DevelopMode_Text_Erase, 0x80302bb0
	.set DevelopMode_Text_ResetCursor, 0x80302a3c
	.set DevelopMode_Text_Display, 0x80302d4c
	.set _HSD_MemAlloc, 0x8037f1e4
	.set TextData_Create, 0x80302834
	.set TextData_Init, 0x80302810
	.set TextData_Unhide, 0x80302ab0
	.set TextData_SetBackgroundColor, 0x80302b90
	.set TextData_HueUnk2, 0x80302b64
	.set TextData_SetWidthHeight, 0x80302b10
.endif



